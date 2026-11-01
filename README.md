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
  <img src="https://img.shields.io/badge/Kubernetes-K3s-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="K3s" />
  <img src="https://img.shields.io/badge/Cloudflare-DNS_SSL-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Cloudflare" />
  <img src="https://img.shields.io/badge/Tailscale-Mesh_VPN-000000?style=for-the-badge&logo=tailscale&logoColor=white" alt="Tailscale" />
  <img src="https://img.shields.io/badge/ArgoCD-GitOps-EF6B48?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD" />
  <img src="https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Trivy-CVE_Scan-00A4A6?style=for-the-badge&logo=aqua&logoColor=white" alt="Trivy" />
  <img src="https://img.shields.io/badge/Gitleaks-Secret_Scan-red?style=for-the-badge" alt="Gitleaks" />
  <img src="https://img.shields.io/badge/Node.js-24_Alpine-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js 24" />
  <img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus" />
  <img src="https://img.shields.io/badge/Grafana-Dashboard-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana" />
</p>

---

## MỤC LỤC
- [1. Giới thiệu & Phân công nhóm](#1-giới-thiệu--phân-công-nhóm)
- [2. Tổng quan đề tài](#2-tổng-quan-đề-tài)
- [3. Kiến trúc hệ thống & Luồng hoạt động](#3-kiến-trúc-hệ-thống--luồng-hoạt-động)
- [4. Bảng tổng hợp công nghệ & Kỹ năng](#4-bảng-tổng-hợp-công-nghệ--kỹ-năng)
- [5. Cấu trúc Repository (Monorepo)](#5-cấu-trúc-repository-monorepo)
- [6. Kế hoạch triển khai 5 giai đoạn](#6-kế-hoạch-triển-khai-5-giai-đoạn-hoàn-thành-trước-05122026)
- [7. Kịch bản Demo kiểm chứng](#7-kịch-bản-demo-kiểm-chứng)
- [8. Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. Giới thiệu & Phân công nhóm

### 1.1 Thông tin chung
- **Môn học:** NT548 - Công nghệ DevOps và Ứng dụng
- **Lớp:** NT548.R12 — HK1 2026-2027
- **Đơn vị:** Khoa Mạng máy tính và Truyền thông — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Đề tài:** Xây dựng hệ thống DevSecOps và GitOps tự động hóa triển khai, bảo mật và giám sát ứng dụng trên hạ tầng Kubernetes Hybrid
- **Repository:** `devsecops-gitops-with-k8s`

### 1.2 Thành viên nhóm & Phân chia công việc

| STT | MSSV | Họ và Tên | Vai trò chính | Nhiệm vụ đảm nhiệm | Môi trường làm việc |
|:---:|:---:|:---|:---|:---|:---|
| 1 | 23521367 | **Ngô Tiến Sỹ** | **Platform & DevOps Lead** | • Quản trị cụm K3s 3-node qua Tailscale Mesh Network, cấu hình Taints/Tolerations.<br>• Cấu hình Traefik Ingress và trỏ DNS Cloudflare.<br>• Khởi tạo ArgoCD GitOps quản lý 2 Application (App & Monitoring).<br>• Xây dựng GitHub Actions: Gitleaks $\rightarrow$ Trivy Scan $\rightarrow$ Build Docker $\rightarrow$ GHCR $\rightarrow$ Git tag.<br>• Soạn thảo Kubernetes Manifests chuẩn và triển khai kube-prometheus-stack. | Toàn quyền Server (VPS & K3s Cluster), GitHub Actions & Git |
| 2 | 23521222 | **Trần Hồng Phúc** | **Web Fullstack Dev** | • Phát triển Web 2 tầng (Node.js 24 Express + Redis đếm lượt truy cập).<br>• Xây dựng endpoints `/healthz`, `/ready` và `/metrics` (`prom-client`).<br>• Đóng gói `Dockerfile` (`node:24-alpine`, `USER 10001` non-root). | 100% Localhost & Git (Thư mục `app/`) |
| 3 | 23520600 | **Điền Quốc Huy** | **QA & Observability Report** | • Thiết kế testcases và thực hiện kiểm thử tải Web (Autocannon / Postman).<br>• Khai thác Grafana Web UI, theo dõi metrics CPU, RAM, HTTP traffic.<br>• Soạn thảo Báo cáo Quan sát (Observability) và đánh giá hiệu năng hệ thống. | 100% Postman/Autocannon & Grafana Web UI |
| 4 | 22520804 | **Đặng Thế Long** | **Documentation & Demo Support** | • Hỗ trợ thực nghiệm và thu thập log/ảnh minh chứng 2 kịch bản demo.<br>• Chủ trì soạn thảo tài liệu Báo cáo đồ án môn học NT548 hoàn chỉnh.<br>• Thiết kế bộ Slide thuyết trình nghiệm thu đồ án. | 100% Google Docs / Word / Slide & Git |

---

## 2. Tổng quan đề tài

### 2.1 Tên chủ đề

> **Xây dựng hệ thống DevSecOps và GitOps tự động hóa triển khai, bảo mật và giám sát ứng dụng trên hạ tầng Kubernetes Hybrid.**

### 2.2 Nội dung thực hiện (5 nội dung cốt lõi)

1. **Quản trị hạ tầng mạng & cụm Kubernetes Hybrid:**  
   Cấu hình DNS Cloudflare và SSL/TLS trỏ tên miền về VPS Public IP. Vận hành cụm K3s 3-node (1 Control Plane VPS 6GB RAM + 2 Worker nodes on-premises 2x 8GB = 16GB, tổng 22GB RAM) kết nối bảo mật qua mạng Tailscale Overlay.
2. **Thiết lập đường ống CI & DevSecOps tự động hóa:**  
   Xây dựng GitHub Actions tích hợp rà soát bí mật mã nguồn (Gitleaks), quét lỗ hổng thư viện và container image (Trivy), tự động đóng gói image chuẩn `node:24-alpine` với user non-root UID 10001 (`USER 10001`), lưu trữ an toàn trên GitHub Container Registry (GHCR) và tự động cập nhật tag GitOps.
3. **Triển khai Continuous Deployment (CD) theo mô hình GitOps:**  
   Cấu hình ArgoCD tự động đồng bộ cấu hình ứng dụng từ Git repository xuống Kubernetes (`directory: {recurse: true}`), kích hoạt cơ chế tự phục hồi (Self-healing: `prune: true`, `selfHeal: true`) và hỗ trợ Rollback an toàn qua `git revert`.
4. **Bảo mật Kubernetes (Runtime Security & NetworkPolicy):**  
   Áp dụng Pod SecurityContext (`runAsNonRoot: true`, `runAsUser: 10001`, `allowPrivilegeEscalation: false`, `capabilities: {drop: [ALL]}`). Xây dựng NetworkPolicy cô lập namespace `database`, đảm bảo chỉ cho phép duy nhất Pod Web App truy cập cổng 6379 của Redis.
5. **Hệ thống Giám sát & Báo cáo Quan sát (Observability):**  
   Triển khai `kube-prometheus-stack` thông qua Helm/ArgoCD (`ServerSideApply=true`, vô hiệu hóa các exporter không dùng của K3s), ứng dụng tích hợp `prom-client` xuất metrics `/metrics`, khai thác giao diện Grafana Web UI để theo dõi tài nguyên và lập Báo cáo Quan sát & Đánh giá hiệu năng hệ thống.

### 2.3 Kết quả dự kiến đạt được

1. Hệ thống DNS Cloudflare và cụm Kubernetes Hybrid 3-node vận hành ổn định qua Tailscale, phân tách rõ vai trò Control Plane và Worker nodes.
2. Pipeline CI/DevSecOps vận hành tự động, chặn kịp thời mọi commit làm rò rỉ secret (Gitleaks) hoặc chứa lỗ hổng CVE nghiêm trọng có bản vá (Trivy).
3. Ứng dụng Web 2 tầng (Node.js 24 + Redis) được triển khai tự động (Zero-touch deployment) qua ArgoCD với khả năng tự phục hồi trạng thái tức thì.
4. Container ứng dụng vận hành an toàn ở chế độ non-root với đầy đủ SecurityContext bảo vệ.
5. Dashboard Grafana hiển thị trực quan thông số CPU, RAM, trạng thái Pod và HTTP metrics ứng dụng thời gian thực; có tài liệu Báo cáo Quan sát & Đo kiểm tải chi tiết.

---

## 3. Kiến trúc hệ thống & Luồng hoạt động

### 3.1 Sơ đồ kiến trúc tổng thể (Architecture Blueprint)

```
[Developer] ──(git push)──► [GitHub: Monorepo /app]
                                   │
                                   ▼
                     [CI & DevSecOps Pipeline: GitHub Actions]
                     ├─ 1. Gitleaks (Secret Leak Detection)
                     ├─ 2. Trivy FS Scan (Dependency CVE Check)
                     ├─ 3. Docker Multi-stage Build (node:24-alpine, USER 10001)
                     ├─ 4. Trivy Image Scan (--severity HIGH,CRITICAL --ignore-unfixed)
                     ├─ 5. Push Image ──► [GitHub Container Registry: ghcr.io]
                     └─ 6. Auto-update Image Tag (commit [skip ci])
                                   │
                                   ▼
                     [GitOps Folder: /k8s-manifests]
                                   │
                                   ▼ (ArgoCD Auto-Sync with recurse: true)
+---------------------------------------------------------------------------------+
| Multi-node Kubernetes Cluster (K3s - Tailscale Mesh Network - 22GB RAM)         |
|                                                                                 |
|  [Control Plane: VPS 6GB RAM, Public IP] (Tainted: NoSchedule)                  |
|  Internet Traffic ──► [Cloudflare DNS + SSL] ──► [Traefik Ingress on VPS]       |
|                                                              │ (toleration)     |
|  [Worker Nodes: 2x On-Premises Servers (2x 8GB = 16GB RAM)]  │                  |
|  +───────────────────────────────────────────────────────────┼───────────────+  |
|  |  • [argocd]         : ArgoCD Application Controller       │               |  |
|  |  • [production-app] : Web App Pods (Node.js 24) ◄─────────┘               |  |
|  |                       │ (SecurityContext: non-root 10001, drop ALL)       |  |
|  |                       ▼ (Allow Port 6379 via NetworkPolicy)               |  |
|  |  • [database]       : Redis Pod (Blocked from all unauthorized pods)      |  |
|  |  • [monitoring]     : Prometheus + Grafana Dashboard as Code (ConfigMap)  |  |
|  +───────────────────────────────────────────────────────────────────────────+  |
+---------------------------------------------------------------------------------+
```

### 3.2 Luồng vận hành chi tiết

1. **Giai đoạn 1 (Code & Security Scan):** Lập trình viên push code vào thư mục `app/`. GitHub Actions kích hoạt:
   - Gitleaks kiểm tra không để lộ secret/token trong commit.
   - Trivy quét dependencies để phát hiện lỗ hổng CVE thư viện.
2. **Giai đoạn 2 (Build & Container Hardening):**
   - Đóng gói container bằng `node:24-alpine`, chạy với user non-root UID 10001 (`USER 10001`).
   - Trivy quét container image với cờ `--severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed`.
   - Đẩy image lên GitHub Container Registry (`ghcr.io` public) kèm tag commit SHA.
3. **Giai đoạn 3 (GitOps Sync via ArgoCD):**
   - Pipeline CI cập nhật tag image mới vào `k8s-manifests/base/deployment.yaml`.
   - ArgoCD phát hiện thay đổi và tự động đồng bộ (Auto-sync) xuống cụm K3s theo cấu hình đệ quy (`directory: {recurse: true}`).
4. **Giai đoạn 4 (Traffic Routing & NetworkPolicy Isolation):**
   - Traefik Ingress tiếp nhận traffic HTTPS từ Cloudflare, định tuyến vào Web App ở namespace `production-app`.
   - Web App chạy với Pod SecurityContext non-root an toàn.
   - NetworkPolicy tại namespace `database` kiểm soát chặt chẽ: chỉ cho phép Pod mang label `app: web` thuộc namespace `production-app` kết nối cổng 6379 của Redis, chặn mọi Pod lạ khác.
5. **Giai đoạn 5 (Continuous Monitoring):**
   - Prometheus tự động scrape chỉ số từ Node Exporter và endpoint `/metrics` của Web App.
   - Grafana tự động nạp dashboard từ ConfigMap để hiển thị thông số CPU, RAM và số lượng truy cập.

---

## 4. Bảng tổng hợp công nghệ & Kỹ năng

| Thành phần | Công cụ sử dụng | Kỹ năng đạt được / Trọng tâm chứng chỉ |
|:---|:---|:---|
| **Networking & DNS** | Cloudflare DNS, Tailscale Mesh VPN | Quản trị định tuyến tên miền, SSL/TLS, kết nối mạng Overlay an toàn giữa VPS và Worker nodes on-premises. |
| **Cluster Setup** | Linux (Ubuntu), K3s, Tailscale Mesh | **Trọng tâm CKA**: Cấu hình mạng Overlay, Taints/Tolerations, phân bổ tải đa node. |
| **CI & DevSecOps** | GitHub Actions, Gitleaks, Trivy, GHCR | **Nền tảng CKS & DevSecOps**: Secret scanning, Quét CVE mã nguồn và Container image, Container Hardening non-root. |
| **CD & GitOps** | ArgoCD | **Trọng tâm CKAD & GitOps**: Declarative Delivery, Auto-sync, Self-healing & Rollback. |
| **K8s Security** | Traefik Ingress, Kubernetes NetworkPolicy, SecurityContext | **Trọng tâm CKAD & CKS**: Định tuyến Ingress HTTPS, SecurityContext non-root, cô lập mạng tầng database. |
| **Observability** | Prometheus, Grafana (Helm `kube-prometheus-stack`) | Giám sát hạ tầng & ứng dụng (`prom-client`), trực quan hóa chỉ số qua Grafana Web UI và lập Báo cáo Quan sát. |

---

## 5. Cấu trúc Repository (Monorepo)

```text
devsecops-gitops-with-k8s/
├── README.md                           # Tài liệu tổng quan dự án
├── WBS.md                              # Cấu trúc phân rã công việc (WBS) & timeline chi tiết (dùng cho Sheet)
├── argocd/                             # Cấu hình Application CRD cho ArgoCD (Sỹ phụ trách)
│   ├── app.yaml                        # Application triển khai Web App & Redis (directory: {recurse: true})
│   └── monitoring.yaml                 # Application triển khai kube-prometheus-stack (ServerSideApply=true)
├── app/                                # Mã nguồn ứng dụng Web 2 tầng (Phúc phụ trách)
│   ├── src/                            # Express API + Redis visitor counter + /metrics (prom-client)
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile                      # Multi-stage build (node:24-alpine, USER 10001 non-root)
├── k8s-manifests/                      # Thư mục GitOps quản lý trạng thái ứng dụng (Sỹ phụ trách)
│   ├── base/                           # Tài nguyên Web App (namespace: production-app)
│   │   ├── deployment.yaml             # Web App Deployment (SecurityContext non-root UID 10001)
│   │   ├── service.yaml                # Web App Service
│   │   ├── configmap.yaml              # Biến môi trường (REDIS_HOST, PORT)
│   │   └── ingress.yaml                # Traefik Ingress
│   ├── database/                       # Tài nguyên Database (namespace: database)
│   │   └── redis.yaml                  # Redis Deployment & Service
│   └── security/                       # Tài nguyên an ninh (namespace: database)
│       └── network-policy.yaml         # Cô lập traffic vào Redis
├── monitoring/                         # Cấu hình giám sát (Sỹ setup, Huy khai thác)
│   └── values.yaml                     # Values cho Helm (tắt component K3s không dùng)
├── scripts/                            # Kịch bản kiểm chứng tự động (Long & Sỹ phụ trách)
│   └── demo.sh                         # Script hỗ trợ thực nghiệm 2 kịch bản demo
└── .github/workflows/                  # Đường ống CI/DevSecOps (Sỹ phụ trách)
    └── ci-devsecops.yml                # Workflow: Gitleaks + Trivy (FS & Image) + Build & Push GHCR
```

---

## 6. Kế hoạch triển khai 5 giai đoạn (Hoàn thành trước 05/12/2026)

| Giai đoạn | Thời gian | Mục tiêu hoàn thành (Definition of Done) | Người phụ trách chính |
|:---|:---:|:---|:---|
| **Phase 1: Khởi động** | Trước 01/11 | Chốt đề tài & phạm vi tinh giản; thống nhất tech stack; phân định trách nhiệm các thành viên. | Cả nhóm (Sỹ chủ trì) |
| **Phase 2: Thiết kế & Setup** | 01/11 - 05/11 | Lập WBS đưa lên Sheet; vẽ topology K3s Hybrid & luồng GitOps; thống nhất API contract Web <-> K8s. | Sỹ, Long, Phúc |
| **Phase 3: Triển khai & Tích hợp** | 06/11 - 20/11 | Dựng K3s 3-node qua Tailscale; trỏ DNS Cloudflare; vibe code Web Node.js + Redis; build Dockerfile non-root; viết CI GitHub Actions (Trivy/Gitleaks); cài ArgoCD sync tự động. | Sỹ (DevOps), Phúc (Web App) |
| **Phase 4: Đo kiểm & Giám sát** | 21/11 - 28/11 | Dựng kube-prometheus-stack qua ArgoCD; kiểm thử tải Web (Autocannon/Postman); chụp biểu đồ Grafana viết Báo cáo Quan sát; lấy log 2 kịch bản demo. | Sỹ, Huy, Long |
| **Phase 5: Báo cáo & Nghiệm thu** | 29/11 - 05/12 | Hoàn thiện Báo cáo đồ án môn học NT548; thiết kế Slide thuyết trình; nghiệm thu nội bộ và sẵn sàng trước ngày 06/12/2026. | Long, Huy, Cả nhóm |

---

## 7. Kịch bản Demo kiểm chứng

Khi báo cáo đồ án, nhóm chứng minh tính hiệu quả của hệ thống thông qua 2 kịch bản thực tế trực quan và trọng tâm:

### Kịch bản 1: Kiểm chứng DevSecOps Pipeline (Trivy Gate)
- **Hành động:** Cố tình thêm một thư viện có lỗ hổng CVE nghiêm trọng đã có bản vá (ví dụ `lodash@4.17.20`) vào `package.json` và commit lên Git.
- **Kết quả:** Pipeline GitHub Actions dừng lại ở bước Trivy Image Scan với exit code 1 (báo đỏ), từ chối đẩy image lên GHCR và từ chối cập nhật GitOps manifest.

### Kịch bản 2: Kiểm chứng GitOps Self-healing & Rollback (ArgoCD)
- **Tự phục hồi (Self-healing):**
  - Thử nghiệm xóa Pod hoặc Deployment trên cụm: `kubectl delete deploy web -n production-app`.
  - $\rightarrow$ ArgoCD phát hiện sai lệch trạng thái mong muốn và tự động tái tạo lại Deployment ngay lập tức.
- **Rollback tự động:**
  - Thực hiện lệnh `git revert HEAD` trên repository Git.
  - $\rightarrow$ ArgoCD phát hiện commit hoàn tác và tự động rollback ứng dụng về phiên bản ổn định trước đó trong vài giây.

---

## 8. Tài liệu tham khảo

1. [Tài liệu chính thức K3s - Lightweight Kubernetes](https://docs.k3s.io/)
2. [Tài liệu chính thức ArgoCD GitOps](https://argo-cd.readthedocs.io/en/stable/)
3. [Tài liệu Aqua Security Trivy](https://aquasecurity.github.io/trivy/)
4. [Tài liệu Gitleaks Secret Scanner](https://github.com/gitleaks/gitleaks)
5. [Tài liệu Cloudflare DNS & SSL/TLS](https://developers.cloudflare.com/dns/)
6. [Tài liệu Tailscale Mesh VPN](https://tailscale.com/kb)
7. [Tài liệu Prometheus Operator & Kube-Prometheus-Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
8. Giáo trình & bài giảng học phần NT548 - Công nghệ DevOps và Ứng dụng (UIT).
