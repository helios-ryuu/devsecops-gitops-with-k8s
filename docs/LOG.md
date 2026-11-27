# Nhật ký triển khai (Deployment Log)

> Checklist ghi chú thực tế trong quá trình dựng hạ tầng và triển khai ứng dụng theo [ARCHITECTURE.md](./ARCHITECTURE.md) và [RUNBOOK.md](./RUNBOOK.md).

## Pha 0: Chuẩn bị Hạ tầng, Tắt Host Firewall An toàn SSH & Công cụ Quản trị
- [x] Xác nhận cổng `sshd` thực tế (`61022` trên `server-01`, `61122` trên `worker-01`, `61222` trên `worker-02`), cấu hình SSH key-only (`PasswordAuthentication no`) và kiểm tra `~/.kube/config` trên `laptop`
- [x] Tắt `ufw` / `firewalld` trên cả 3 node và xác minh `iptables` ở trạng thái `policy ACCEPT`
- [x] Cài công cụ trên `laptop` (Fedora) (`kubectl`, `helm`, `cilium`, `jq`, `wireguard-tools`) và khai báo biến `export VPS_PUBLIC_IP`
- [x] Giới hạn DHCP pool Router (`10.10.0.50–254`) & đặt Static IP LAN `10.10.0.0/24`, khóa Cloud Firewall (NSG) VPS (`61022/tcp`, `80/tcp`, `443/tcp`, `51820/udp`, `ICMP` IPv4), trỏ Cloudflare DNS & tạo Origin Certificate

<!-- Ghi chú của bạn cho Pha 0 -->


## Pha 1: Mạng WireGuard `wg0` & Chuẩn bị Host Longhorn
- [x] Cài gói phụ thuộc OS, nạp `br_netfilter` và ghi cấu hình `/etc/sysctl.d/90-k8s.conf` (`ip_forward=1`, `rp_filter=0`, `bridge-nf-call-iptables=1`) trên cả 3 node
- [x] Cài `open-iscsi`, `nfs-common` và bật `iscsid` + `iscsi_tcp` trên `worker-01` & `worker-02` (`/var/lib/longhorn`)
- [x] Sinh khóa và bật WireGuard `wg0` (`10.100.0.0/24`) cho `server`, `client-01`, `client-02`, `client-fedora`, `client-phone`; kiểm tra thông mạng 5 node, LAN `worker-01 <-> worker-02` và SSH qua `10.100.0.1..3`
- [x] Kiểm chứng `ufw`/`firewalld` tắt, `FORWARD ACCEPT`, khởi động lại các node Linux & `laptop`, xác nhận `wg0` tự phục hồi và `nmap` kiểm tra VPS Cloud NSG

<!-- Ghi chú của bạn cho Pha 1 -->


## Pha 2: Kubernetes v1.37.1 (`kubeadm`) & Cilium eBPF + Hubble UI
- [x] Tắt Swap vĩnh viễn, nạp `overlay` và cài đặt `containerd.io 2.3.6` (`SystemdCgroup = true`) + `kubelet`/`kubeadm`/`kubectl` `v1.37.1` trên cả 3 node
- [x] Tạo `/etc/kubernetes/enc/enc.yaml` (`aescbc`), chạy `kubeadm init` trên `server-01`, `kubeadm join` + gán nhãn `node.longhorn.io/create-default-disk=true` cho `worker-01`, `worker-02`
- [x] Cài đặt Cilium eBPF CNI/LB + `CiliumLoadBalancerIPPool` (`<VPS_PUBLIC_IP>/32`) + Hubble UI

<!-- Ghi chú của bạn cho Pha 2 -->


## Pha 3: Longhorn Storage, HashiCorp Vault + ESO & Traefik HA (`LoadBalancer`)
- [x] Cài đặt Longhorn (`replicas: 2`) và kiểm tra Node trên Longhorn UI (`Schedulable / Ready`, `158 Gi` khả dụng trên `worker-01` và `347 Gi` khả dụng trên `worker-02` sau 30% Reserved)
- [x] Cài đặt HashiCorp Vault (Longhorn PVC `2Gi`), khởi tạo 1 khóa (`-key-shares=1 -key-threshold=1`), sao lưu `~/vault-init-keys.txt` ngoại tuyến, `unseal`, nạp 3 bí mật KV v2 & cấu hình Kubernetes Auth (3 Least-Privilege Policies/Roles)
- [x] Cài đặt External Secrets Operator (ESO) & apply `ServiceAccount`/`SecretStore`/`ExternalSecret` Tầng 1 (`cloudflare-origin-tls`, `grafana-admin-secret`) đạt `SecretSynced`
- [x] Cài đặt Traefik HA (`replicas: 2`), `traefik-metrics` (`ClusterIP: 9100`), `TLSStore`

<!-- Ghi chú của bạn cho Pha 3 -->


## Pha 4: Monitoring Stack, Kyverno Policy, ArgoCD & Kích hoạt CI/GHCR
- [x] Cài đặt `kube-prometheus-stack` (`monitoring`) & apply `platform-core/monitoring/servicemonitors/`
- [x] Cài đặt Kyverno (`admissionController`), apply `platform-core/kyverno/policies/` và xác nhận 4 `ValidatingPolicy` sẵn sàng (`Deny`)
- [x] Cài đặt ArgoCD (`argocd`) cho GitOps Tầng 2 & bật `serviceMonitor` trên Cilium/Hubble, Longhorn và ArgoCD
- [x] Bật `Read and write permissions` cho `GITHUB_TOKEN` (GitHub Settings -> Actions -> General)
- [x] Kiểm tra `git status`, chạy `git add -A && git commit && git push -u origin main`, đợi `ci.yml` build image GHCR & `git pull --rebase origin main`

<!-- Ghi chú của bạn cho Pha 4 -->


## Pha 5: Tầng Đồ án (`project-nt548`), CI/CD & Cloudflare Zero Trust
- [x] Kiểm chứng luồng CD `ci.yml` (`workflow_call` + `RollingUpdate` khi cập nhật `app/`, rollback `git revert`) & Nightly Audit (`nightly-audit.yml`, `cron 0 0 * * *`)
- [x] Apply `project-nt548/app-prod.yaml`, xác nhận ESO đồng bộ `redis-auth-secret` từ Vault (`SecretSynced`) và kiểm tra `app-prod` (`web-deployment` `replicas: 2`, `redis-0`, `nt548.helios.id.vn`)
- [x] Trỏ DNS Cloudflare (`vps.helios.id.vn`, `nt548.helios.id.vn`, `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn`) & Cloudflare Zero Trust `K8s Admin`

<!-- Ghi chú của bạn cho Pha 5 -->


## Pha 6: Kiểm thử Hệ thống & Hoàn thiện Báo cáo
- [x] Hoàn thiện khung báo cáo `docs/REPORT.md`, cập nhật sơ đồ `diagrams/architecture.drawio` và đưa Chương 1 đến hết mục `4.3` kèm ảnh minh chứng (`diagrams/`) vào `docs/NT548-R12_Nhom-6_BaoCaoDoAn.docx`
- [ ] Chạy 5 kịch bản kiểm thử hệ thống qua `scripts/test.sh` và thu thập ảnh minh chứng mục `4.4`, `4.5` (Grafana, Hubble UI, `nmap`)
- [ ] Hoàn thiện mục `4.4`, `4.5`, Chương 5 trong file Word, thiết kế slide thuyết trình và nghiệm thu trước `05/12/2026`
