<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>
<h1 align="center"><b>NT548.R12 - CÔNG NGHỆ DEVOPS VÀ ỨNG DỤNG</b></h1>
<p align="center"><b>ĐỒ ÁN MÔN HỌC: HỆ THỐNG DEVSECOPS & GITOPS TRÊN HẠ TẦNG KUBERNETES HYBRID</b></p>
<p align="center">
  <i>Repository: <code>devsecops-gitops-with-k8s</code></i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kubernetes-v1.37.1%20(kubeadm)-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/WireGuard-wg0_Mesh-88171A?style=for-the-badge&logo=wireguard&logoColor=white" alt="WireGuard" />
  <img src="https://img.shields.io/badge/Cilium-eBPF_CNI_&_LB-F8C517?style=for-the-badge&logo=cilium&logoColor=black" alt="Cilium" />
  <img src="https://img.shields.io/badge/Traefik-HA_Ingress-24A1C1?style=for-the-badge&logo=traefikproxy&logoColor=white" alt="Traefik HA" />
  <img src="https://img.shields.io/badge/Longhorn-Distributed_Storage-5F259F?style=for-the-badge" alt="Longhorn" />
  <img src="https://img.shields.io/badge/HashiCorp_Vault-ESO_Secrets-FFEC6E?style=for-the-badge&logo=vault&logoColor=black" alt="HashiCorp Vault" />
  <img src="https://img.shields.io/badge/ArgoCD-GitOps-EF6B48?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD" />
  <img src="https://img.shields.io/badge/Kyverno-Policy_as_Code-00A86B?style=for-the-badge" alt="Kyverno" />
  <img src="https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Trivy-CVE_&_Config_Scan-00A4A6?style=for-the-badge&logo=aqua&logoColor=white" alt="Trivy" />
  <img src="https://img.shields.io/badge/Node.js-26_Alpine-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js 26" />
  <img src="https://img.shields.io/badge/Prometheus_&_Grafana-Observability-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus" />
</p>

---

## MỤC LỤC
- [1. Giới thiệu](#1-giới-thiệu)
- [2. Tổng quan đề tài](#2-tổng-quan-đề-tài)
- [3. Kiến trúc 2 tầng & Luồng vận hành](#3-kiến-trúc-2-tầng--luồng-vận-hành)
- [4. Cấu trúc Repository](#4-cấu-trúc-repository)
- [5. Kịch bản Kiểm thử hệ thống](#5-kịch-bản-kiểm-thử-hệ-thống)
- [6. Tài liệu chi tiết](#6-tài-liệu-chi-tiết)

---

## 1. Giới thiệu

### 1.1 Thông tin chung
- **Môn học:** NT548 - Công nghệ DevOps và Ứng dụng
- **Lớp:** NT548.R12 — HK1 2026-2027
- **Đơn vị:** Khoa Mạng máy tính và Truyền thông — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Đề tài:** Xây dựng hệ thống DevSecOps và GitOps tự động hóa triển khai, bảo mật và giám sát ứng dụng trên hạ tầng Kubernetes Hybrid
- **Repository:** `devsecops-gitops-with-k8s`

### 1.2 Thành viên nhóm & Phân chia công việc

| STT | MSSV | Họ và Tên | Vai trò chính | Nhiệm vụ đảm nhiệm | Môi trường làm việc |
|:---:|:---:|:---|:---|:---|:---|
| 1 | 23521367 | **Ngô Tiến Sỹ** | **Platform & DevOps Lead** | • Thiết kế & vận hành mạng WireGuard `wg0`, Kubernetes Hybrid (`kubeadm v1.37.1`), Cilium eBPF LB + Hubble UI.<br>• Triển khai Traefik HA, Longhorn Storage, HashiCorp Vault & ESO (Kubernetes Auth), Kyverno Policy.<br>• Vận hành ArgoCD (`app-prod`), `kube-prometheus-stack` & Nightly GHCR Audit.<br>• Xây dựng GitHub Actions CI/DevSecOps (`ci.yml`). | Server VPS & Workers, GitHub Actions, GitOps |
| 2 | 23521222 | **Trần Hồng Phúc** | **Web Fullstack Dev** | • Phát triển Web 2 tầng (Next.js 16 App Router + Redis đếm lượt truy cập + `APP_ENV`/`APP_VERSION`).<br>• Xây dựng endpoints `/healthz`, `/ready` kiểm tra Redis phục vụ Kubernetes Probes.<br>• Đóng gói `Dockerfile` (`node:26.13.1-alpine3.24`, `USER 10001:10001` non-root). | Localhost & Git (`app/`) |
| 3 | 23520600 | **Điền Quốc Huy** | **Observability & Kiểm thử quan sát** | • Khai thác Grafana Web UI & Hubble UI theo dõi CPU, RAM, Cilium eBPF, Traefik và luồng NetworkPolicy.<br>• Chụp ảnh minh chứng dashboard quan sát phục vụ dán vào báo cáo và slide.<br>• Phối hợp rà soát phần đánh giá quan sát hệ thống. | Grafana / Hubble Web UI & Báo cáo |
| 4 | 22520804 | **Đặng Thế Long** | **Documentation & Kiểm thử hệ thống** | • Phối hợp thực nghiệm kiểm thử hệ thống và thu thập log/ảnh minh chứng 5 kịch bản (`scripts/test.sh`).<br>• Chủ trì soạn thảo tài liệu Báo cáo đồ án môn học NT548 hoàn chỉnh (`docs/REPORT.md`).<br>• Thiết kế bộ Slide thuyết trình và sơ đồ kiến trúc Draw.io. | Tài liệu Báo cáo / Slide / Draw.io & Git |

---

## 2. Tổng quan đề tài

1. **Hạ tầng mạng & Kubernetes Hybrid chuẩn Production:**
   Thiết lập mạng WireGuard `wg0` (`10.100.0.0/24`, endpoint `vps.helios.id.vn:51820` $\rightarrow$ `<VPS_PUBLIC_IP>`) nối `server-01` (VPS 6GB RAM, Control Plane) với `worker-01` và `worker-02` (2×8GB RAM on-premises nối thẳng LAN `10.10.0.0/24` 1Gbps). Sử dụng **Cilium eBPF CNI** (`kubeProxyReplacement: true`), cấp phát External IP `<VPS_PUBLIC_IP>/32` qua `CiliumLoadBalancerIPPool`, vận hành **Traefik HA (2 replicas)** và **Longhorn Distributed Storage (2 replicas)**.
2. **Bảo mật đa lớp (Defense in Depth & Policy as Code):**
   - **CI Gate:** Gitleaks, Trivy FS, `kubeconform` + Trivy Config (YAML thuần), Docker multi-stage build non-root (`UID 10001:10001`), Trivy Image trước khi đẩy lên **GHCR**.
   - **Secret & Admission:** **HashiCorp Vault** (Longhorn PVC `2Gi`, UI chỉ mở nội bộ qua `port-forward`) kết hợp **External Secrets Operator (ESO)** xác thực bằng **Kubernetes Auth** (tách `ServiceAccount` & `SecretStore` theo từng namespace, **Zero Static Secret**), **Kyverno** (`admissionController` Enforce/Deny 4 `ValidatingPolicy` trên nhãn `policy-tier: hardened`), Cilium **NetworkPolicy** cô lập Redis StatefulSet (`UID 999`), và **Cloudflare Zero Trust Access** bảo vệ toàn bộ UI quản trị (`argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn`).
   - **Runtime CVE:** **GitHub Actions Nightly Cron (`0 0 * * *`)** tự động pull các image tag đang triển khai trên GHCR và base image về runner để quét Trivy định kỳ (`0 MB` RAM cụm).
3. **GitOps Continuous Delivery (`RollingUpdate` Zero-Downtime):**
   - **ArgoCD Application (`app-prod`)** đồng bộ trực tiếp `project-nt548/k8s-manifests/` vào namespace `app-prod` (`nt548.helios.id.vn`).
   - Triển khai **`Deployment web-deployment`** (`replicas: 2`, `RollingUpdate` `maxUnavailable: 0, maxSurge: 1`, `podAntiAffinity`) tự động cập nhật image tag & `APP_VERSION` từ CI và hỗ trợ `git revert` rollback tức thì.
4. **Observability toàn diện:**
   - Kết hợp `kube-prometheus-stack` (Prometheus + Grafana lưu trên Longhorn PVC) với **Hubble UI** quan sát flow gói tin Layer 4/7 và trạng thái `DROPPED` của NetworkPolicy theo thời gian thực.

---

## 3. Kiến trúc 2 tầng & Luồng vận hành

Hệ thống chia rõ **2 tầng** trong cùng repository:
- **Tầng 1 (`platform-core/`):** Nền tảng Kubernetes cố định dài hạn (`Cilium`, `Hubble`, `Longhorn`, `HashiCorp Vault`, `External Secrets Operator`, `Traefik HA`, `Prometheus/Grafana`, `ArgoCD`, `Kyverno`).
- **Tầng 2 (`project-nt548/`):** Tài nguyên riêng của đồ án (Manifest YAML thuần cho `web-deployment` `replicas: 2`, `redis-statefulset`, `SecretStore`/`ExternalSecret`, `NetworkPolicy`, `Ingress`) neo tại [project-nt548/app-prod.yaml](./project-nt548/app-prod.yaml).

Chi tiết sơ đồ mạng WireGuard `wg0`, sơ đồ kiến trúc tổng thể (`diagrams/architecture-2x.png`, `architecture-4x.png`, `architecture.drawio`), quy hoạch IP/RAM xem tại **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** và hướng dẫn triển khai chi tiết từ đầu đến kết thúc xem tại **[docs/RUNBOOK.md](./docs/RUNBOOK.md)**.

---

## 4. Cấu trúc Repository

```text
devsecops-gitops-with-k8s/
├── README.md                           # Tổng quan dự án NT548
├── docs/                               # Tài liệu kiến trúc, vận hành & báo cáo đồ án
│   ├── ARCHITECTURE.md                 # Kiến trúc 2 tầng, sơ đồ ASCII tổng thể, quy hoạch IP/RAM & kịch bản kiểm thử
│   ├── RUNBOOK.md                      # Hướng dẫn triển khai đầy đủ từng bước từ Pha 0 đến kết thúc
│   ├── REPORT.md                       # Nội dung báo cáo đồ án môn học NT548 đầy đủ (kèm vị trí hình & bảng)
│   ├── NT548-R12_Nhom-6_BaoCaoDoAn.docx # File báo cáo Word chính thức của Nhóm 6
│   ├── WBS.md                          # Cấu trúc phân rã công việc & timeline
│   └── LOG.md                          # Nhật ký thực thi & checklist triển khai theo pha
├── diagrams/                           # Sơ đồ kiến trúc (Draw.io, PNG 2x/4x) & ảnh minh chứng triển khai, kiểm thử
│   ├── architecture.drawio
│   ├── architecture-2x.png
│   └── architecture-4x.png
├── wireguard/                          # Cấu hình mẫu wg0.conf & hướng dẫn chuẩn bị host / Cloud NSG
├── kubeadm-config/                     # Cấu hình kubeadm Init/Join (v1beta4) & EncryptionConfiguration
├── app/                                # Ứng dụng Web Next.js 16 + Redis (UID 10001 non-root, APP_ENV/APP_VERSION)
├── platform-core/                      # Tầng 1: Hạ tầng nền tảng dài hạn
│   ├── cilium/                         # Cilium eBPF + Hubble UI & CiliumLoadBalancerIPPool
│   ├── longhorn/                       # Longhorn Distributed Storage (2 replicas)
│   ├── vault/                          # HashiCorp Vault (Longhorn PVC 2Gi) & hướng dẫn KV v2 / Kubernetes Auth
│   ├── external-secrets/               # External Secrets Operator (ESO — Kubernetes Auth, Zero Static Secret)
│   ├── traefik/                        # Traefik HA (LoadBalancer), TLSStore, ExternalSecret & ClusterIP metrics
│   ├── monitoring/                     # kube-prometheus-stack (Longhorn PVC), ExternalSecret & ServiceMonitors
│   ├── kyverno/                        # Kyverno (admissionController) + 4 ValidatingPolicies (policy-tier: hardened)
│   └── argocd/                         # ArgoCD values (GitOps cho Tầng 2 app-prod)
├── project-nt548/                      # Tầng 2: Tài nguyên riêng của đồ án
│   ├── k8s-manifests/                  # Manifest YAML thuần: web-deployment, Service, Ingress, Redis, ExternalSecret, NetworkPolicy
│   └── app-prod.yaml                   # ArgoCD Application Tầng 2 (namespace app-prod)
├── .github/workflows/                  # Kiến trúc Modular CI/CD (workflow_call + vars.* + yq + setup-trivy)
│   ├── ci.yml                          # Orchestrator CI/CD (gọi security-scan.yml & build-deploy.yml)
│   ├── security-scan.yml               # workflow_call: Gitleaks, Trivy FS, kubeconform & Trivy Config
│   ├── build-deploy.yml                # workflow_call: Buildx, Trivy Image Gate, Push GHCR & update YAML (yq)
│   └── nightly-audit.yml               # Nightly GHCR Image Audit tách riêng (cron 0 0 * * *, 0 MB RAM cụm)
└── scripts/test.sh                     # Script in hướng dẫn từng bước thực hiện 5 kịch bản kiểm thử hệ thống
```

---

## 5. Kịch bản Kiểm thử hệ thống

Chạy `./scripts/test.sh` (hoặc `./scripts/test.sh --all`) để hiển thị hướng dẫn và câu lệnh kiểm thử 5 kịch bản:
1. **CI DevSecOps Gate:** Chặn commit rò rỉ secret, dính CVE (`Trivy FS`) hoặc manifest lỗi (`kubeconform` + `trivy config`).
2. **Kyverno Enforce:** Chặn tức thì Pod vi phạm (`:latest`, chạy `root`, thiếu `limits`, sai registry) trong `app-prod`.
3. **GitOps Continuous Delivery (`RollingUpdate` Zero-Downtime) & Instant Rollback:** Push commit lên `app/` kích hoạt CI build & cập nhật `project-nt548/k8s-manifests/deployment.yaml`, ArgoCD đồng bộ `RollingUpdate` (`maxUnavailable: 0, maxSurge: 1`) không rớt HTTP 200 và `git revert` rollback tức thì.
4. **Zero-Trust Redis Isolation & Hubble UI:** Kiểm chứng NetworkPolicy chặn Pod lạ kết nối Redis `:6379` với luồng `DROPPED` trực quan trên Hubble UI.
5. **Nightly GHCR Audit, Traefik HA & Longhorn Failover:** Kích hoạt tay workflow **`Nightly Active GHCR & Base Image Audit`** (`nightly-audit.yml`, `0 MB` RAM cụm), theo dõi tài nguyên trên Grafana, test xóa nóng Pod Traefik (**Zero-Downtime HA**) và drain node chứa `redis-0` (tự phục hồi sau ~30–60s chuyển PVC `RWO`, **`RPO = 0`** không mất dữ liệu bộ đếm).

---

## 6. Tài liệu chi tiết

1. **[docs/REPORT.md](./docs/REPORT.md)** — Nội dung báo cáo đồ án môn học NT548 hoàn chỉnh kèm vị trí hình ảnh và bảng.
2. **[docs/RUNBOOK.md](./docs/RUNBOOK.md)** — Hướng dẫn triển khai từng bước từ đầu đến kết thúc (Pha 0 $\rightarrow$ Pha 6) kèm kiểm chứng & thu hồi Tầng 2.
3. **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — Kiến trúc 2 tầng, sơ đồ ASCII tổng thể, phân bổ IP/RAM, bảo mật đa lớp và 5 kịch bản kiểm thử.
4. **[wireguard/README.md](./wireguard/README.md)** — Hướng dẫn cài đặt gói, `sysctl`, `open-iscsi`/`nfs-common`, tắt host firewall & khóa Cloud NSG, và kích hoạt `wg0` trên các node.
5. **[platform-core/vault/README.md](./platform-core/vault/README.md)** — Hướng dẫn khởi tạo/unseal HashiCorp Vault (1 khóa), cấu hình KV v2 + Kubernetes Auth từng bước, mở Vault UI qua `port-forward` và quy trình xoay vòng (rotate) bí mật với ESO.
6. **[diagrams/architecture-2x.png](./diagrams/architecture-2x.png)** *(và [architecture-4x.png](./diagrams/architecture-4x.png) / [architecture.drawio](./diagrams/architecture.drawio))* — Sơ đồ kiến trúc tổng thể chất lượng cao phục vụ báo cáo & slide thuyết trình.
