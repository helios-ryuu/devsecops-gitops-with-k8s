# KIẾN TRÚC HỆ THỐNG — PLATFORM ENGINEERING & DEVSECOPS (ĐỒ ÁN NT548)

Tài liệu mô tả kiến trúc hoàn chỉnh đã chuyển đổi và triển khai của hệ thống Kubernetes Hybrid-Cloud trên nền tảng **Kubernetes v1.37.1 (`kubeadm` + `containerd.io 2.3.6`) + WireGuard (`wg0`) + Cilium eBPF + Traefik HA + Longhorn + ArgoCD GitOps + Bitnami Sealed Secrets + Kyverno + `kube-prometheus-stack` + GitHub Actions CI/CD (DevSecOps Gates & Nightly GHCR Image Audit)**.

> Các tài liệu liên quan: [README.md](./README.md) • [RUNBOOK.md](./RUNBOOK.md) • [WBS.md](./WBS.md) • [LOG.md](./LOG.md) • [wireguard/README.md](./wireguard/README.md) • [platform-core/sealed-secrets/README.md](./platform-core/sealed-secrets/README.md)

---

## 1. Kiến trúc 2 Tầng (Tách biệt Nền tảng & Đồ án)

Hệ thống được tổ chức thành 2 tầng độc lập nhằm tái sử dụng cụm Kubernetes cho các đồ án hoặc ứng dụng tiếp theo và thu hồi tài nguyên ứng dụng sạch sẽ chỉ bằng 1 lệnh GitOps.

| Tầng | Thư mục / Thành phần | Chu kỳ vòng đời | Cơ chế quản lý |
|---|---|---|---|
| **Tầng 1: Platform Core Infrastructure** | `wireguard/`, `kubeadm-config/`, `platform-core/` (`cilium`, `sealed-secrets`, `traefik`, `longhorn`, `monitoring`, `kyverno`, `argocd`) | Dựng một lần, vận hành lâu dài cho toàn cụm | `kubeadm` + `helm` + `kubectl` *(ArgoCD chỉ quản lý Tầng 2)* |
| **Tầng 2: Project NT548 (App & DevSecOps)** | `app/`, `.github/workflows/ci.yml`, `project-nt548/` (`app-prod`, `web-deployment` `replicas: 2`, `redis` StatefulSet, `NetworkPolicy`) | Triển khai & thu hồi theo vòng đời đồ án | GitHub Actions (`ci.yml`) + [project-nt548/app-prod.yaml](./project-nt548/app-prod.yaml) (`Application`) |

> Thu hồi toàn bộ Tầng 2 sau khi bảo vệ đồ án mà không ảnh hưởng cụm nền (xóa Application trước rồi xóa Namespace để dọn sạch PVC Longhorn & Secret):
> `kubectl delete -f project-nt548/app-prod.yaml && kubectl delete namespace app-prod`

### Cấu trúc Repository chuẩn

```text
devsecops-gitops-with-k8s/
├── README.md                                 # Tổng quan đồ án, phân công thành viên & kịch bản demo
├── ARCHITECTURE.md                           # Kiến trúc 2 tầng, sơ đồ ASCII tổng thể, quy hoạch IP/RAM & kiểm chứng
├── RUNBOOK.md                                # Hướng dẫn thao tác từng bước (Pha 0 -> Pha 6)
├── WBS.md                                    # Cấu trúc phân chia công việc (WBS) & mốc thời gian
├── LOG.md                                    # Nhật ký thực thi & checklist triển khai theo pha
├── wireguard/                                # Hub-and-Spoke wg0 + hướng dẫn chuẩn bị host & khóa biên
│   ├── README.md
│   └── wg0.*.conf.example                    # server, client-01, client-02, client-fedora, client-phone
├── kubeadm-config/                           # Cấu hình kubeadm Init/Join (v1beta4) & EncryptionConfiguration
├── platform-core/                            # TẦNG 1: Hạ tầng nền tảng cụm
│   ├── cilium/                               # Cilium eBPF (kubeProxyReplacement, MTU 1340, Hubble, IP Pool)
│   ├── sealed-secrets/                       # Bitnami Sealed Secrets Controller & hướng dẫn sao lưu master key
│   ├── traefik/                              # Traefik HA (replicas: 2), TLSStore & ClusterIP metrics-service (:9100)
│   ├── longhorn/                             # Longhorn StorageClass (replicas: 2, metricsScrapeSources :9500)
│   ├── monitoring/                           # kube-prometheus-stack (Longhorn PVC) & ServiceMonitor Traefik
│   ├── kyverno/                              # Kyverno (admissionController) + 4 CEL ValidatingPolicy (policy-tier=hardened)
│   └── argocd/                               # ArgoCD values (GitOps chuyên biệt cho Tầng 2 app-prod)
├── app/                                      # TẦNG 2: Next.js 16 Standalone (UID 10001, APP_ENV/APP_VERSION, Pure-TCP Redis)
├── .github/workflows/
│   └── ci.yml                                # CI DevSecOps Gate, push GHCR, deploy app-prod & Nightly GHCR Audit (cron 00:00 UTC)
├── project-nt548/                            # TẦNG 2: GitOps Application & Manifests đồ án NT548
│   ├── app-prod.yaml                         # ArgoCD Application Tầng 2 (namespace app-prod, nhãn policy-tier=hardened)
│   ├── redis-auth-sealedsecret.example.yaml  # Mẫu SealedSecret sinh bằng kubeseal cho Redis Auth
│   └── k8s-manifests/                        # Manifest YAML thuần: web-deployment (RollingUpdate), Service, Ingress, ConfigMap, Redis, NetworkPolicy
└── scripts/
    └── demo.sh                               # Script in hướng dẫn 5 kịch bản Demo (chỉ đọc, an toàn)
```

---

## 2. Sơ đồ Kiến trúc Tổng thể (Cải tiến từ sơ đồ cũ)

Sơ đồ dưới đây mô tả trực tiếp trạng thái hệ thống mới sau khi chuyển đổi toàn bộ từ kiến trúc cũ (`K3s` + `Tailscale` + `Traefik hostPort trên VPS` + `Kustomize`) sang kiến trúc Hybrid Kubernetes chuẩn Production:

```text
          +-------------------------------+    +---------------------+     +-------------------------------------+                                                 +--------------------------+
          |    Admin Laptop / Phone       |    | End User / Browser  |---->| Cloudflare Edge (DNS/WAF/Full TLS)  |                                                 |  Developer (Local Git)   |
          |   (.10 / .11 WireGuard wg)    |    +---------------------+     +------------------+------------------+                                                 +--------------------------+
          +---------------+---------------+                                                   | HTTPS :80/:443 (Public)                                                          | git push / PR -> main
                          | UDP :51820 (Encrypted WireGuard Mesh)                             | (Không đi qua wg0 VPN)                                                           v
                          v                                                                   v                                                    +--- GitHub Repo & GHCR (ghcr.io/<owner>/<repo>) -----------+
#=== RANH GIỚI 1: WIREGUARD MESH VPN (wg0: 10.100.0.0/24, MTU 1420, UDP :51820) =====================================================#  Poll YAML  | * Git Repo: app/, project-nt548/, platform-core/, .github |
#  +--- ADMIN PEERS TRONG wg0 - NGOÀI K8S OVERLAY --------------------------------+           | (Public Internet -> eth0)            # +-----------| * Trigger CI: push/PR main (paths) & nightly cron         |---------------+
#  | client-fedora (10.100.0.10/32) | client-phone (10.100.0.11/32)               |           |                                      # | Pull GHCR | * OCI GHCR: Image :<git-sha> (cấm :latest qua Kyverno)    |<--+           |
#  | -> Chỉ đi qua wg0 tới K8s API (:6443) & SSH Key (:61022/61122/61222)         |           |                                      # |        +--+-----------------------------------------------------------+   |           |
#  | -> KHÔNG nằm trong Cilium Pod CIDR (10.42/16) hay Svc CIDR (10.43/16)        |           |                                      # |        |                                | Trigger workflow                |           |
#  +----------------------+-------------------------------------------------------+           |                                      # |        |                                v                                 |           |
#                         | API :6443 / SSH :61022                                            | eth0 <VPS_PUBLIC_IP>:80/:443         # |        |  +--- .github/workflows/ci.yml (DEVSECOPS GATE) -------------+   |           |
#                         v                                                                   v (Bypass wg0 -> Cloud NSG -> LB VIP)  # |        |  | +--- [Job 1: secret-scan] ------------------------------+ |   |           |
#  +--- RANH GIỚI 2: K8S CLUSTER (kubeadm v1.37.1) & CILIUM VXLAN OVERLAY (Pod: 10.42.0.0/16 MTU 1340 | Svc: 10.43.0.0/16) -------+  # |        |  | | Gitleaks (gitleaks-action@v3, fetch-depth: 0)         | |   |           |
#  |  +--- CLOUD VPS (6GB) - CONTROL PLANE: server-01 (wg0: 10.100.0.1 | SSH :61022 | K8s v1.37.1 | containerd 2.3.6) ---------+  |  # |        |  | | -> Quét leaked secrets/tokens trong toàn lịch sử Git  | |   |           |
#  |  |  * Cloud NSG: Mở 80/443, 61022/tcp, 51820/udp (+ICMP); Chặn tuyệt đối 6443, 9100, 10250, 8472/udp                      |  |  # |        |  | +-------------------------------------------------------+ |   |           |
#  |  |  * Control Plane: kube-apiserver (:6443, etcd aescbc), kube-scheduler, kube-controller-manager                         |  |  # |        |  |                             | (Passed)                    |   |           |
#  |  |  * Cilium eBPF (KubeProxyReplacement=true, Hubble) | CiliumLoadBalancerIPPool (<VPS_PUBLIC_IP>/32 -> VIP)              |  |  # |        |  |                             v                             |   |           |
#  |  |  * Path: User -> Cloudflare Edge -> eth0 -> Cloud NSG -> Cilium LB VIP -> VXLAN (MTU 1340) tới Traefik HA              |  |  # |        |  | +--- [Job 2: vulnerability-scan] -----------------------+ |   |           |
#  |  +------------------------------------------------------------------------------------------------------------------------+  |  # |        |  | | Trivy FS (app/) | HIGH,CRITICAL, ignore-unfixed -> 1  | |   | [skip ci] |
#  |                             | K8s Control/API (:6443 <-> kubelet)                     | VIP & Pod VXLAN Traffic              |  # |        |  | +-------------------------------------------------------+ |   | update    |
#  |                             v  [ Cilium VXLAN (UDP :8472, MTU 1340) bọc trong WireGuard wg0 (UDP :51820, MTU 1420) ]         |  # |        |  |                             | (needs: secret-scan)        |   | deploy    |
#  |  +--- ON-PREMISES WORKERS (8GB/máy | zone=onprem-lan | LAN 10.10.0.0/24) -------------------------------------------------+  |  # |        |  |                             v                             |   |           |
#  |  |                                                                                                                        |  |  # |        |  | +--- [Job 3: manifest-security-gate] -------------------+ |   |           |
#  |  | +-------------------------------------------------+                +-------------------------------------------------+ |  |  # |        |  | | kubeconform -strict (manifests, kyverno, monit.)      | |   |           |
#  |  | | WORKER-01 (wg0: 10.100.0.2 | SSH :61122)        |  Direct LAN    | WORKER-02 (wg0: 10.100.0.3 | SSH :61222)        | |  |  # |        |  | | + Trivy Config Scan (k8s-manifests/, HIGH/CRITICAL)   | |   |           |
#  |  | |  * kubelet + containerd 2.3.6 + node-exporter   | /32 Bypass VPS |  * kubelet + containerd 2.3.6 + node-exporter   | |  |  # |        |  | +-------------------------------------------------------+ |   |           |
#  |  | |  * Cilium Agent (eBPF, VXLAN) + Hubble          |<-------------->|  * Cilium Agent (eBPF, VXLAN) + Hubble          | |  |  # |        |  |                             | (Gates Passed)              |   |           |
#  |  | |  * Longhorn 199GB (/var/lib/longhorn, Repl 1)   | 1Gbps (~0.3ms) |  * Longhorn 461GB (/var/lib/longhorn, Repl 2)   | |  |  # |        |  |                             v                             |   |           |
#  |  | +------------------------+------------------------+                +------------------------+------------------------+ |  |  # |        |  | +--- [Job 4: build-and-deploy-prod] --------------------+ |   |           |
#  |  |                          v                                                                  v                          |  |  # |        |  | | 1. Buildx + Trivy Image Gate (HIGH,CRITICAL, unfixed) | |   |           |
#  |  | +--- TẦNG 1: PLATFORM CORE (Platform Infrastructure & DevSecOps Services trên zone: onprem-lan) ---------------------+ |  |  # |        |  | | 2. Push ghcr.io/<repo>:<git-sha> (no :latest)         | |   |           |
#  |  | |  +---------------------------------------------------+  +-------------------------------------------------------+  | |  |  # |        |  | | 3. Regex update image & APP_VERSION (deployment.yaml) | |   |           |
#  |  | |  | [ns: traefik] HA x2 (AntiAffinity, :80/:443)      |  | [ns: argocd] GitOps Singleton (quản lý Tầng 2)        |  | |  |  # |        |  | | 4. git commit '[skip ci]' & push origin HEAD:main     | |---+           |
#  |  | |  |  * Cloudflare Origin TLS, metrics :9100 ClusterIP |  |  * Poll project-nt548/k8s-manifests/ -> sync app-prod<=============+        |  | +-------------------------------------------------------+ |               |
#  |  | |  +---------------------------------------------------+  +-------------------------------------------------------+  | |  |  #          |  +-----------------------------------------------------------+               |
#  |  | |  +---------------------------------------------------+  +-------------------------------------------------------+  | |  |  #          |                                                                   Cron 00:00 |
#  |  | |  | [ns: monitoring] kube-prometheus-stack (x1)       |  | [ns: longhorn-system] Distributed Storage (2 Repl)    |  | |  |  #          |  +--- [Job 5: nightly-ghcr-image-scan] ----------------------+    UTC Audit  |
#  |  | |  |  * Prometheus, Grafana :3000, Hubble UI           |  |  * Default StorageClass qua LAN 1Gbps                 |  | |  |  #          |  | Trigger: Cron '0 0 * * *' (00:00 UTC) | workflow_dispatch |               |
#  |  | |  |  * (dex/notifications/alertmanager tắt)           |  |  * Metrics :9500 (NetworkPolicy -> Pod prometheus)    |  | |  |  #          |  | Extract images: deployment.yaml + redis-statefulset.yaml  |               |
#  |  | |  +---------------------------------------------------+  +-------------------------------------------------------+  | |  |  #          |  | docker pull + trivy image HIGH,CRITICAL --ignore-unfixed  |<--------------+
#  |  | |  * [ns: kyverno] 4 CEL ValidatingPolicy (Deny)  |  [ns: kube-system] Bitnami Sealed Secrets (kubeseal) + CoreDNS   | |  |  #          |  | -> Audit CVE hằng đêm trên Runner (0 MB RAM cụm K8s)      |
#  |  | +--------------------------------------------------------------------------------------------------------------------+ |  |  #          |  +-----------------------------------------------------------+
#  |  | +--- TẦNG 2: PROJECT NT548 - [ns: app-prod] (policy-tier=hardened | Managed by ArgoCD) ------------------------------+ |  |  #          |
#  |  | |  +--------------------------------------------+     :6379/TCP      +--------------------------------------------+  | |  |  #          |  +--- TỔNG HỢP 2 RANH GIỚI MẠNG & PHÒNG THỦ CHIỀU SÂU -----------------------+
#  |  | |  | redis-0 (StatefulSet)                      |<------------------>| web-deployment x2 (Next.js 16, Rolling)    |  | |  |  #          |  | [1] Ranh giới 1 - WireGuard Mesh (wg0: 10.100.0.0/24, MTU 1420, :51820)   |
#  |  | |  |  * PVC -> Longhorn (2 Replicas LAN)        | (allow-web-to-red) |  * containerd 2.3.6 pulls ghcr.io/<sha>   <=============Pull GHCR+  |     * Lớp mã hóa nối VPS (.1), Workers (.2/.3) và Admin (.10/.11).        |
#  |  | |  +--------------------------------------------+                    +--------------------------------------------+  | |  |  #             |     * Worker<->Worker: Direct LAN /32 (bypass Internet -> 1Gbps ~0.3ms).  |
#  |  | |  * Bảo vệ: NetworkPolicy allow-web-to-redis + 4 Kyverno CEL (non-root, seccomp, limits, ghcr) + SealedSecret       | |  |  #             | [2] Ranh giới 2 - Cilium VXLAN Overlay (Pod 10.42/16 MTU 1340 | Svc 10.43)|
#  |  | +--------------------------------------------------------------------------------------------------------------------+ |  |  #             |     * Lồng bên trong wg0 cho Pod/Service; Admin .10/.11 KHÔNG vào đây.    |
#  |  +------------------------------------------------------------------------------------------------------------------------+  |  #             |     * Public HTTPS: eth0 (Cloud NSG) -> Cilium LB VIP -> Traefik HA Pod.  |
#  +--- END RANH GIỚI 2 (CILIUM K8S OVERLAY) -------------------------------------------------------------------------------------+  #             | [3] Defense-in-Depth (Từ Edge tới Container Runtime):                     |
#   * Pod<->Pod, Pod<->Service đi qua Cilium eBPF & VXLAN (MTU 1340) bên trong Ranh giới 2.                                          #             |     Cloudflare WAF/Access -> Cloud NSG -> wg0 /32 -> Cilium eBPF NetPol   |
#   * Admin Peers (.10/.11) và Direct LAN /32 (Worker<->Worker) chạy ở WireGuard wg0 (MTU 1420) bên ngoài K8s Overlay.               #             |     -> Kubeseal + 4 Kyverno CEL + CI Gate + Nightly Scan (0 MB RAM K8s).  |
#=== END RANH GIỚI 1 (WIREGUARD MESH wg0) ===========================================================================================#             +---------------------------------------------------------------------------+
```

### Đối chiếu nâng cấp so với sơ đồ kiến trúc cũ (`.png`)

| Hạng mục | Sơ đồ cũ (`.png` trước đây) | Kiến trúc hiện tại (`ARCHITECTURE.md`) |
|---|---|---|
| **VPN & CNI** | Tailscale (`tailscale0`) + K3s Flannel | **WireGuard Hub-and-Spoke + Direct LAN `/32` (`wg0`)** + **Cilium eBPF (`kubeProxyReplacement=true`, VXLAN `MTU 1340`)** + **Hubble UI** |
| **Kubernetes** | K3s đơn giản | **`kubeadm v1.37.1` + `containerd.io 2.3.6`** (`aescbc` EncryptionConfiguration) |
| **Ingress & TLS** | 1 Pod `traefik-controller` dùng `hostPort 80/443` trên `server-01` | **Traefik HA (`replicas: 2` trên 2 Worker)** qua **Cilium `LoadBalancer` IP Pool (`<VPS_PUBLIC_IP>/32`)**, `TLSStore` Cloudflare Origin, Service `traefik-metrics:9100` tách riêng |
| **Storage & Secrets** | Thiếu lưu trữ phân tán & mã hóa Secret trên Git | **Longhorn (`replicas: 2` qua LAN 1Gbps)** + **Bitnami Sealed Secrets (`kubeseal`)** |
| **Admission Policy** | Không có | **Kyverno (`admissionController`)** + **4 CEL `ValidatingPolicy` (`Deny`)** trên `policy-tier=hardened` |
| **Phạm vi ArgoCD** | Quản lý cả `monitoring` lẫn app; chạy `ApplicationSet` thừa | Chỉ quản lý Tầng 2 (`app-prod`); `applicationSet.replicas: 0`; tắt `dex`/`notifications`; `monitoring` cài ở Tầng 1 |
| **Manifests & CI/CD** | 3 job trong `ci-pipe.yml` + Kustomize `kustomization.yaml` | 5 job trong `ci.yml` (thêm **`kubeconform` + `Trivy Config`** và **`nightly-ghcr-image-scan`** `0 MB` RAM) + **YAML thuần** (`project-nt548/k8s-manifests/`) |

---

## 3. Thiết kế Chi tiết theo Lớp

### 3.1. Định tuyến Hybrid Mesh WireGuard (`wg0`) & Luồng Traffic Public

1. **Tối ưu LAN nội bộ cho Longhorn & Pod-to-Pod (`worker-01` $\leftrightarrow$ `worker-02`):**
   - `worker-01` (`10.100.0.2/24`) và `worker-02` (`10.100.0.3/24`) đặt tại mạng LAN gia đình **`10.10.0.0/24`**, cố định IP tĩnh (`Static IP` qua `netplan`, nằm ngoài dải DHCP pool `10.10.0.50–254`: `<WORKER_01_LAN_IP>`, `<WORKER_02_LAN_IP>`).
   - Trên mỗi worker khai báo **2 Peer WireGuard**:
     - Peer tới `server` (`vps.helios.id.vn:51820` — bản ghi `A` DNS Only $\rightarrow$ `<VPS_PUBLIC_IP>`): `AllowedIPs = 10.100.0.0/24` giúp 5 node (`server`, `client-01`, `client-02`, `client-fedora`, `client-phone`) thông mạng hai chiều dù ở LAN hay qua Internet.
     - Peer trực tiếp tới worker đối diện (`<PEER_LAN_IP>:51820` trong `10.10.0.0/24`): `AllowedIPs = 10.100.0.3/32` (hoặc `.2/32`). Nhờ **Longest-Prefix Match (`/32` ưu tiên hơn `/24`)**, toàn bộ lưu lượng Longhorn replication và Cilium VXLAN giữa 2 worker đi thẳng qua mạng LAN 1Gbps (~0.3ms), không vòng qua VPS.
2. **Luồng truy cập Internet $\rightarrow$ Pod trên Worker:**
   - User $\rightarrow$ **Cloudflare Edge** (`nt548.helios.id.vn`, `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn` trỏ `CNAME` Proxied $\rightarrow$ `vps.helios.id.vn`; 3 domain quản trị được bảo vệ thêm bởi **Cloudflare Zero Trust Access** OTP) $\rightarrow$ Public IP `<VPS_PUBLIC_IP>:443` trên `server-01`.
   - `server-01` chạy **Cilium eBPF (`kubeProxyReplacement: true`)** quảng bá `CiliumLoadBalancerIPPool` (`<VPS_PUBLIC_IP>/32`) gắn cho Service `LoadBalancer` của **Traefik** (`externalTrafficPolicy: Cluster`).
   - Cilium đóng gói qua **VXLAN tunnel (`MTU 1340`)** trên `wg0` (`MTU 1420`) đưa gói tin tới một trong 2 Pod **Traefik HA** trên `worker-01` / `worker-02`.
   - Traefik chấm dứt TLS bằng **Cloudflare Origin Certificate** (`Secret cloudflare-origin-tls`, chế độ SSL `Full (Strict)`) rồi chuyển vào ClusterIP Service tương ứng.

### 3.2. Bảo mật Đa lớp (Defense in Depth) & NetworkPolicy

1. **Tầng Host & Cloud NSG:**
   - Trên `server-01`, **Cloud Firewall (NSG)** chỉ mở Ingress IPv4 `61022/tcp`, `80/tcp`, `443/tcp`, `51820/udp` (`+ ICMP`), chặn tuyệt đối `6443/tcp`, `9100/tcp`, `10250/tcp`, `8472/udp`.
   - Cả 3 node tắt `ufw`/`firewalld` (tránh xung đột chain `FORWARD` với Cilium eBPF và `wg0`), bật `net.ipv4.ip_forward=1`, `rp_filter=0`, và giữ tắt `Cilium hostFirewall` (do `wg0` là giao diện L3). Trên LAN `10.10.0.0/24`, 2 worker được bảo vệ bởi Router NAT và SSH Key-only (`PasswordAuthentication no`).
   - API Server bật mã hóa Secrets trên `etcd` bằng `aescbc` (`/etc/kubernetes/enc/enc.yaml`).
2. **Tầng Secrets & Policy-as-Code:**
   - Mọi Secret lưu trên Git đều được mã hóa bằng **`kubeseal`** (`cloudflare-origin-tls`, `grafana-admin-secret` ở Tầng 1; `redis-auth-secret` ở Tầng 2), master key sao lưu ngoại tuyến.
   - **Kyverno (`admissionController`)** chạy 4 CEL `ValidatingPolicy` (`Deny`) giới hạn vào namespace mang nhãn **`policy-tier: hardened`** (tự động gắn trên `app-prod` qua `managedNamespaceMetadata`), bắt buộc `runAsNonRoot: true`, `seccompProfile: RuntimeDefault`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, đủ `requests`/`limits`, cấm `:latest` và khóa registry về `ghcr.io/helios-ryuu/*` hoặc `docker.io/library/redis:*`.
3. **Tầng NetworkPolicy eBPF (Cilium):**
   - Trong `app-prod`, `NetworkPolicy allow-web-to-redis` chỉ cho phép Pod mang nhãn `app: web` kết nối TCP `6379` tới `redis-0`; mọi Pod khác trong namespace bị chặn và hiện flow `DROPPED` trên Hubble UI.
   - Trong `longhorn-system`, mặc định chart Longhorn bật `restrictInternalTraffic: true` sinh `NetworkPolicy/longhorn-manager` khóa cổng `9500`; do đó [platform-core/longhorn/values.yaml](./platform-core/longhorn/values.yaml) cấu hình `networkPolicies.metricsScrapeSources` để mở riêng TCP `9500` cho Pod `app.kubernetes.io/name: prometheus` ở namespace `monitoring`.
   - Service `traefik-metrics` (`ClusterIP: 9100`) tách riêng khỏi LoadBalancer (`ports.metrics.expose.default: false`) để không lộ metrics Traefik ra Internet.

### 3.3. Ứng dụng & Luồng Continuous Delivery (`RollingUpdate` Zero-Downtime)

- **Ứng dụng Web (`app/`):** Next.js 16 App Router (`output: standalone`, `cacheComponents: true`), dùng client Redis thuần qua `node:net` (không thêm dependency ngoài), bọc khối đọc Redis trong `<Suspense>` + `connection()` để `pnpm run build` không cần Redis lúc build ảnh, cung cấp `/healthz` và `/ready`, đóng gói multi-stage non-root `USER 10001:10001`.
- **Pipeline `.github/workflows/ci.yml`:** Chạy tuần tự/song song các cổng kiểm tra (`Gitleaks` $\rightarrow$ `Trivy FS` & `kubeconform`/`Trivy Config` $\rightarrow$ `Buildx` + `Trivy Image Gate` $\rightarrow$ push **GHCR**) trước khi tự động cập nhật `image` và `APP_VERSION` (`<8-char-SHA>`) trong [project-nt548/k8s-manifests/deployment.yaml](./project-nt548/k8s-manifests/deployment.yaml) và commit `[skip ci]`.
- **Chiến lược `RollingUpdate` (`maxUnavailable: 0, maxSurge: 1`):** ArgoCD đồng bộ `deployment.yaml` xuống `app-prod`; Kubernetes tạo Pod mới, chờ `readinessProbe` (`GET /ready` xác nhận Redis) chuyển `Ready` rồi mới tắt Pod cũ, đảm bảo `0%` downtime; hỗ trợ rollback tức thì bằng `git revert HEAD --no-edit && git push`.
- **Nightly GHCR Audit (`0 0 * * *`):** Đọc trực tiếp image đang chạy từ `deployment.yaml` và `redis-statefulset.yaml`, kéo về GitHub Runner quét Trivy định kỳ với **0 MB RAM cụm**.

---

## 4. Quy hoạch Tài nguyên, Địa chỉ IP & Tên miền

### 4.1. Ngân sách RAM (VPS 6GB & 2 Workers 8GB/máy)

> **Tài nguyên khả dụng thực tế:** `server-01` (VPS 6GB RAM) còn **~5.78 GiB** khả dụng (theo biểu đồ Grafana thực tế, Control Plane + Cilium Agent + `node-exporter` dùng **~1.9 – 2.0 GiB**, dư **~3.8 – 3.9 GiB**). Hai Worker 8GB còn **~7.6 GB** (`worker-01`) và **~7.1 GB** (`worker-02`) khả dụng (~14.7 GB tổng 2 Workers). Để vừa ngân sách RAM, toàn bộ thành phần nền singleton (`Prometheus`, `Grafana`, `ArgoCD`, `Kyverno`, `Sealed Secrets`) giữ `replicas: 1`, tắt `dex`/`notifications`/`alertmanager`, tắt `Kyverno background/cleanup/reports` và đặt `applicationSet.replicas: 0`.

| Thành phần | Tầng | Cơ chế phân bổ | RAM thực tế tổng 2 Workers | Trung bình / 1 Worker (8GB) | Sau thu hồi Tầng 2 / Worker |
|---|---|---|---|---:|---:|
| Phần cứng / Kernel mặc định | Host | Cả 2 Worker (~400–900MB/máy) | ~1.3 GB | ~0.65 GB | ~0.65 GB |
| OS + `containerd` + `kubelet` + `wg0` | Core | Cả 2 Worker | ~0.70 – 0.90 GB | ~0.35 – 0.45 GB | ~0.35 – 0.45 GB |
| Cilium Agent (x2) + Operator/Hubble/CoreDNS (1) | Core | `kube-system` | ~0.50 – 0.70 GB | ~0.25 – 0.35 GB | ~0.25 – 0.35 GB |
| Traefik HA (`replicas: 2`, AntiAffinity) | Core | `traefik` (1 Pod/máy) | ~0.15 – 0.25 GB | ~0.08 – 0.13 GB | ~0.08 – 0.13 GB |
| Longhorn (`replicas: 2` trên 2 Worker) | Core | `longhorn-system` | ~1.00 – 1.50 GB | ~0.50 – 0.75 GB | ~0.45 – 0.70 GB |
| `kube-prometheus-stack` (Prometheus + Grafana) | Core | `monitoring` (Singleton) | ~0.80 – 1.20 GB | ~0.40 – 0.60 GB | ~0.40 – 0.60 GB |
| ArgoCD (`dex/notifications: false`, `applicationSet.replicas: 0`) | Core | `argocd` (Singleton) | ~0.50 – 0.80 GB | ~0.25 – 0.40 GB | ~0.25 – 0.40 GB |
| Bitnami Sealed Secrets | Core | `kube-system` (Singleton) | ~0.04 – 0.06 GB | ~0.02 – 0.03 GB | ~0.02 – 0.03 GB |
| Kyverno (`admissionController` `replicas: 1`, 4 rules) | Core | `kyverno` (Singleton) | ~0.15 – 0.25 GB | ~0.08 – 0.13 GB | ~0.08 – 0.13 GB |
| **GitHub Actions Nightly GHCR Audit (`0 0 * * *`)** | **Project** | GitHub Runner | **0 MB** | **0 MB** | **0 MB** |
| **App `app-prod` (`web-deployment` x2 & `redis-0`)** | **Project** | `app-prod` | ~0.25 – 0.40 GB | ~0.13 – 0.20 GB | **0 GB** |
| **TỔNG CỘNG (tính cả ~0.65 GB/máy mặc định)** | | | **~5.4 – 7.4 GB** *(trên 16GB)* | **~2.7 – 3.7 GB** *(dư ~4.3–5.3 GB)* | **~2.5 – 3.45 GB** |

### 4.2. Quy hoạch IP, Cổng SSH, Ổ đĩa & Tên miền

| Thành phần | Giao diện / Loại | Địa chỉ / Tên miền | Cổng / Ghi chú |
|---|---|---|---|
| `server-01` (`heliosvps`, 6GB) | `eth0` / `wg0` | `<VPS_PUBLIC_IP>` / `10.100.0.1/24` | SSH **`61022/tcp`**, API `10.100.0.1:6443`, `CiliumLoadBalancerIPPool` `<VPS_PUBLIC_IP>/32` |
| Bản ghi `A` Public VPS | Cloudflare (DNS Only) | `vps.helios.id.vn` $\rightarrow$ `<VPS_PUBLIC_IP>` | Tắt Proxy (đám mây xám) cho WireGuard UDP `:51820` & SSH `:61022` |
| `worker-01` (8GB) | `wg0` / LAN | `10.100.0.2/24` / `<WORKER_01_LAN_IP>` | SSH **`61122/tcp`**, Static IP `10.10.0.0/24` (ngoài DHCP `.50–.254`), Longhorn `199GB` (`/var/lib/longhorn`) |
| `worker-02` (8GB) | `wg0` / LAN | `10.100.0.3/24` / `<WORKER_02_LAN_IP>` | SSH **`61222/tcp`**, Static IP `10.10.0.0/24` (ngoài DHCP `.50–.254`), Longhorn `461GB` trên `/` (`/var/lib/longhorn`) |
| `client-fedora` / `client-phone` | `wg0` | `10.100.0.10/32` / `10.100.0.11/32` | Quản trị cụm (`kubectl`, `helm`, SSH) qua Hub `vps.helios.id.vn:51820` |
| Pod CIDR / Service CIDR | Overlay | `10.42.0.0/16` (`MTU 1340`) / `10.43.0.0/16` | Cilium VXLAN & CoreDNS `10.43.0.10` |
| Tên miền Public | Cloudflare Proxy | `nt548.helios.id.vn` | `CNAME` tới `vps.helios.id.vn` (Proxied), SSL Mode `Full (Strict)` |
| Tên miền Quản trị | Cloudflare Zero Trust | `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn` | `CNAME` tới `vps.helios.id.vn` (Proxied) + Access Policy `K8s Admin` (Email OTP) |

### 4.3. Ghi chú Vận hành Thực tế & Giới hạn Thiết kế (Trade-offs & SPOF)

1. **Điểm lỗi đơn (SPOF) có chủ đích theo ngân sách đồ án & hướng mở rộng Production:**
   - **`server-01` (Control Plane & Edge Ingress VIP):** Do giới hạn 1 VPS, `server-01` vừa là Control Plane đơn lẻ vừa là điểm vào duy nhất của `CiliumLoadBalancerIPPool`. Hướng nâng cấp Production: nhân bản 3 Control Plane (`etcd` quorum) kết hợp Cloud Load Balancer hoặc Cilium BGP Control Plane.
   - **`redis-0` (`StatefulSet`, `replicas: 1`):** Dùng PVC Longhorn `ReadWriteOnce (RWO)` đảm bảo **Data Durability (`RPO = 0`)** nhưng không phải Zero-Downtime khi chuyển node (gián đoạn ngắn ~30–60 giây để detach/attach PVC). Hướng nâng cấp Production: chuyển sang Redis Sentinel hoặc Redis Cluster.
2. **Chiến lược Monorepo + `[skip ci]` & Mã hóa `etcd` (`aescbc`):**
   - Dùng chung Monorepo kết hợp `paths` filter trong [ci.yml](./.github/workflows/ci.yml) và `[skip ci]` giúp quản lý tập trung ở quy mô đồ án, vẫn tách ranh giới GitOps (ArgoCD chỉ theo dõi `project-nt548/k8s-manifests/`). Doanh nghiệp lớn có thể tách riêng App Repo và GitOps Config Repo để phân quyền RBAC độc lập.
   - `etcd` dùng `aescbc` nội bộ ([init-server-01.yaml](./kubeadm-config/init-server-01.yaml)) không phụ thuộc Cloud KMS ngoài; các Secret trên Git mã hóa bằng `kubeseal` kèm sao lưu ngoại tuyến master key ([platform-core/sealed-secrets/README.md](./platform-core/sealed-secrets/README.md)).
3. **Quan sát thực tế trên Headlamp & Hubble UI:**
   - Trong namespace `argocd`, Helm chart vẫn tạo Deployment/Service `argocd-applicationset-controller` nhưng đã đặt `applicationSet.replicas: 0` (`0` Pod chạy, `0 MB` RAM).
   - Trên Hubble UI, luồng outbound từ `grafana` tới `world:443` là hành vi mặc định kiểm tra phiên bản/analytics của Grafana.

---

## 5. Kiểm tra Xác nhận Hệ thống & Kịch bản Demo

### 5.1. Danh mục kiểm chứng vận hành

| # | Thành phần cần xác minh | Lệnh / Cách kiểm tra | Kết quả đạt yêu cầu |
|---|---|---|---|
| 1 | WireGuard Mesh & LAN Direct | `sudo wg show` & `mtr -c 5 10.100.0.3` (từ `worker-01`) | Endpoint worker $\leftrightarrow$ worker là IP LAN, RTT < 1ms |
| 2 | Cổng Public & Cluster Security | `nmap -Pn -p 61022,80,443,6443,9100,10250 vps.helios.id.vn` (từ Internet) | `6443, 9100, 10250` bị `filtered`/chặn; chỉ mở `61022, 80, 443, 51820/udp` |
| 3 | Cilium eBPF & Nodes Ready | `cilium status` & `kubectl get nodes -o wide` | 3/3 `Ready`; `server-01` có `NoSchedule`; IP Internal `10.100.0.1..3` |
| 4 | Traefik HA & Longhorn Replicas | `kubectl get svc,pods -n traefik` & Longhorn UI (`Node`) | Service LB mang IP `<VPS_PUBLIC_IP>`; Longhorn nhận diện đúng `10.100.0.2`, `.3` |
| 5 | ArgoCD GitOps & Monitoring | `kubectl get applications -n argocd`, `hubble observe` & Grafana | Applications `Synced / Healthy`; Grafana có đủ CPU/RAM/Traefik/Cilium/Longhorn `:9500` |
| 6 | Kyverno Enforcement | `kubectl run test -n app-prod --image=nginx:latest` | API Server chặn ngay lập tức bởi Admission Policy |
| 7 | CI/CD & Nightly GHCR Audit | Push code thử + chạy `ci.yml` (`run_nightly_scan=true`) | Job CI pass các gate CVE/Config/Secret; Nightly Job pull & scan sạch image active (`0 MB` RAM cụm) |
| 8 | NetworkPolicy & Phát hành liên tục | `deploy/web-deployment`, `curl https://nt548.helios.id.vn/ready` | `RollingUpdate` zero downtime; Pod lạ tới Redis `:6379` bị `DROPPED` trên Hubble |

### 5.2. 5 Kịch bản Demo cho Hội đồng (Chi tiết lệnh tại [scripts/demo.sh](./scripts/demo.sh))

1. **Kịch bản 1 – DevSecOps CI Gate (Fail Fast):** Thêm tạm dependency có CVE (ví dụ `lodash@4.17.20`) hoặc cấu hình manifest sai để kích hoạt `Trivy FS` / `kubeconform` + `Trivy Config`; GitHub Actions chặn ngay và hủy bước đẩy GHCR.
2. **Kịch bản 2 – Kyverno Admission Policy Enforce:** Chạy `kubectl run test-violation -n app-prod --image=nginx:latest`; Kyverno (`admissionController`) từ chối ngay tại Kubernetes API Server do vi phạm root user, thiếu resource limits, tag `:latest` và registry ngoài whitelist.
3. **Kịch bản 3 – GitOps Continuous Delivery (`RollingUpdate` Zero-Downtime) & Instant Git Rollback:** Chạy vòng lặp `curl` liên tục vào `https://nt548.helios.id.vn/ready`, đẩy commit mới lên `app/` để `ci.yml` cập nhật image + `APP_VERSION` trong `project-nt548/k8s-manifests/deployment.yaml` và ArgoCD đồng bộ `RollingUpdate` (`maxUnavailable: 0, maxSurge: 1`) không rớt request nào; sau đó chạy `git revert HEAD --no-edit && git push` để rollback tức thì.
4. **Kịch bản 4 – NetworkPolicy Cô lập Redis & Hubble Observability:** Khởi chạy Pod hợp chuẩn Kyverno trong `app-prod` nhưng không mang nhãn `app: web` thử kết nối `redis-service.app-prod.svc.cluster.local:6379` $\rightarrow$ bị chặn đứng và hiển thị flow đỏ **`DROPPED`** trên Hubble UI (`https://hubble.helios.id.vn`).
5. **Kịch bản 5 – Nightly GHCR CVE Audit (`0 MB` RAM cụm), Traefik HA & Longhorn Failover:** Kích hoạt tay job quét hàng đêm `nightly-ghcr-image-scan` (`run_nightly_scan=true`) trên GitHub Actions + xem Dashboard tài nguyên trên Grafana (`https://grafana.helios.id.vn`); xóa nóng 1 Pod Traefik trong lúc `curl` liên tục để chứng minh **Zero-Downtime HA** (`0%` rớt HTTP 200); sau đó `kubectl drain` worker chứa `redis-0` để chứng minh **High Availability & Data Durability (`RPO = 0`)** — gián đoạn ngắn ~30–60 giây khi Longhorn detach/attach PVC `RWO` sang worker còn lại, tự phục hồi và giữ nguyên bộ đếm lượt truy cập.
