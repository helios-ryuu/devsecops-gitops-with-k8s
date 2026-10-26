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
  <img src="https://img.shields.io/badge/Terraform-Cloudflare_DNS-F38020?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />
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
- [6. Kế hoạch triển khai 8 tuần](#6-kế-hoạch-triển-khai-8-tuần)
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
| 1 | 23521367 | **Ngô Tiến Sỹ** | **Platform Lead** | • Quản trị cụm K3s 3-node qua Tailscale Mesh Network, cấu hình Taints/Tolerations.<br>• Cấu hình Traefik Ingress Controller lắng nghe port 80/443 trên VPS.<br>• Khởi tạo nền tảng ArgoCD quản lý 2 Application (App & Monitoring). | Toàn quyền Server (VPS & K3s Cluster) |
| 2 | 23521222 | **Trần Hồng Phúc** | **App & Observability Dev** | • Phát triển Web 2 tầng (Node.js 24 Express + Redis đếm lượt truy cập).<br>• Xây dựng endpoints `/healthz`, `/ready` và `/metrics` (`prom-client`).<br>• Đóng gói `Dockerfile` (`node:24-alpine`, `USER 10001` non-root).<br>• Thiết kế và xuất bản Grafana Dashboard as Code (ConfigMap JSON). | 100% Localhost & Grafana Web UI |
| 3 | 23520600 | **Điền Quốc Huy** | **K8s Manifests & GitOps** | • Soạn thảo K8s Manifests chuẩn (Deployment có SecurityContext non-root, Service, Ingress).<br>• Thiết lập NetworkPolicy cô lập tầng dữ liệu Redis trong namespace `database`.<br>• Cấu hình Helm values `kube-prometheus-stack` (tắt target K8s không dùng trong K3s). | 100% Git (Thư mục `k8s-manifests/`) |
| 4 | 22520804 | **Đặng Thế Long** | **DevSecOps CI & Automation** | • Xây dựng GitHub Actions: Gitleaks (quét secret) $\rightarrow$ Trivy FS & Image Scan (`--ignore-unfixed`) $\rightarrow$ Build Docker $\rightarrow$ Push GHCR $\rightarrow$ Auto-update Git tag.<br>• Viết Terraform tự động tạo bản ghi DNS Cloudflare trỏ domain về VPS.<br>• Xây dựng bash script tự động hóa 3 kịch bản demo (`scripts/demo-all.sh`). | 100% GitHub Web, Actions Cloud & Git |

---

## 2. Tổng quan đề tài

### 2.1 Tên chủ đề

> **Xây dựng hệ thống DevSecOps và GitOps tự động hóa triển khai, bảo mật và giám sát ứng dụng trên hạ tầng Kubernetes Hybrid.**

### 2.2 Nội dung thực hiện (5 nội dung)

1. **Quản trị hạ tầng dạng mã (IaC) và cụm Kubernetes Hybrid:**  
   Sử dụng Terraform tự động quản lý DNS Cloudflare trỏ domain về VPS Public IP. Vận hành cụm K3s 3-node (1 Control Plane VPS 6GB RAM + 2 Worker nodes on-premises 2x 8GB = 16GB, tổng 22GB RAM) kết nối an toàn qua mạng Tailscale Overlay.
2. **Thiết lập đường ống CI & DevSecOps tự động hóa:**  
   Xây dựng GitHub Actions tích hợp rà soát bí mật mã nguồn (Gitleaks), quét lỗ hổng thư viện và container image (Trivy), tự động đóng gói image chuẩn `node:24-alpine` với user non-root UID 10001 (`USER 10001`), lưu trữ an toàn trên GitHub Container Registry (GHCR) và tự động cập nhật tag GitOps.
3. **Triển khai Continuous Deployment (CD) theo mô hình GitOps:**  
   Cấu hình ArgoCD tự động đồng bộ cấu hình ứng dụng từ Git repository xuống Kubernetes (`directory: {recurse: true}`), kích hoạt cơ chế tự phục hồi (Self-healing: `prune: true`, `selfHeal: true`) và hỗ trợ Rollback an toàn qua `git revert`.
4. **Bảo mật Kubernetes (Runtime Security & NetworkPolicy):**  
   Áp dụng Pod SecurityContext (`runAsNonRoot: true`, `runAsUser: 10001`, `allowPrivilegeEscalation: false`, `capabilities: {drop: [ALL]}`). Xây dựng NetworkPolicy cô lập namespace `database`, kết hợp điều kiện AND giữa `namespaceSelector` và `podSelector` để chỉ cho phép duy nhất Pod Web App truy cập cổng 6379 của Redis.
5. **Hệ thống Giám sát & Quản lý Dashboard dạng mã (Observability as Code):**  
   Triển khai `kube-prometheus-stack` thông qua ArgoCD (`ServerSideApply=true`, `serviceMonitorSelectorNilUsesHelmValues: false`, vô hiệu hóa các exporter không dùng của K3s), quản lý Dashboard Grafana bền vững dưới dạng ConfigMap đồng bộ qua Git.

### 2.3 Kết quả dự kiến đạt được

1. Bộ mã nguồn Terraform quản trị DNS Cloudflare tự động và cụm Kubernetes Hybrid 3-node hoạt động ổn định, phân tách rõ vai trò Control Plane và Worker nodes.
2. Pipeline CI/DevSecOps vận hành tự động, chặn kịp thời mọi commit làm rò rỉ secret (Gitleaks) hoặc chứa lỗ hổng CVE nghiêm trọng có bản vá (Trivy).
3. Ứng dụng Web 2 tầng (Node.js 24 + Redis) được triển khai tự động (Zero-touch deployment) qua ArgoCD với khả năng tự phục hồi trạng thái tức thì.
4. Luồng traffic vào tầng dữ liệu Redis được kiểm soát nghiêm ngặt bởi NetworkPolicy, container vận hành ở chế độ non-root.
5. Dashboard Grafana hiển thị trực quan thông số phần cứng, trạng thái Pod và metrics ứng dụng thời gian thực, lưu trữ bền vững dưới dạng mã khai báo (GitOps).

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
|  Internet Traffic ──► [Cloudflare DNS + SSL] ──► [Traefik Ingress on VPS]        |
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
| **IaC** | Terraform (Cloudflare Provider) | Tự động hóa bản ghi DNS, quản lý hạ tầng mạng dạng khai báo (Declarative IaC). |
| **Cluster Setup** | Linux (Ubuntu), K3s, Tailscale Mesh | **Trọng tâm CKA**: Cấu hình mạng Overlay, Taints/Tolerations, phân bổ tải đa node. |
| **CI & DevSecOps** | GitHub Actions, Gitleaks, Trivy, GHCR | **Nền tảng CKS & DevSecOps**: Secret scanning, Quét CVE mã nguồn và Container image, Container Hardening. |
| **CD & GitOps** | ArgoCD | **Trọng tâm CKAD & GitOps**: Declarative Delivery, Auto-sync, Self-healing & Rollback. |
| **K8s Security** | Traefik Ingress, Kubernetes NetworkPolicy, SecurityContext | **Trọng tâm CKAD & CKS**: Định tuyến Ingress, SecurityContext non-root, cô lập mạng tầng database. |
| **Observability** | Prometheus, Grafana (Helm `kube-prometheus-stack`) | Giám sát hạ tầng & ứng dụng (`prom-client`), quản lý Dashboard as Code. |

---

## 5. Cấu trúc Repository (Monorepo)

```text
devsecops-gitops-with-k8s/
├── README.md                           # Tài liệu tổng quan dự án
├── argocd/                             # File cấu hình Application CRD cho ArgoCD (Bootstrap thủ công 1 lần)
│   ├── app.yaml                        # Application triển khai Web App & Redis (directory: {recurse: true})
│   └── monitoring.yaml                 # Application triển khai kube-prometheus-stack (ServerSideApply=true)
├── terraform/                          # Mã nguồn Terraform quản lý DNS Cloudflare (Long phụ trách)
│   ├── main.tf                         # Khai báo bản ghi A/CNAME trỏ về VPS IP
│   ├── variables.tf
│   └── terraform.tfvars.example
├── app/                                # Mã nguồn ứng dụng Web 2 tầng (Phúc phụ trách)
│   ├── src/                            # Express API + Redis visitor counter + /metrics
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile                      # Multi-stage build (node:24-alpine, USER 10001)
├── k8s-manifests/                      # Thư mục GitOps quản lý trạng thái ứng dụng (Huy phụ trách)
│   ├── base/                           # Tài nguyên Web App (namespace: production-app)
│   │   ├── deployment.yaml             # Web App Deployment (SecurityContext non-root UID 10001)
│   │   ├── service.yaml                # Web App Service
│   │   ├── configmap.yaml              # Biến môi trường (REDIS_HOST, PORT)
│   │   └── ingress.yaml                # Traefik Ingress
│   ├── database/                       # Tài nguyên Database (namespace: database)
│   │   └── redis.yaml                  # Redis Deployment & Service
│   └── security/                       # Tài nguyên an ninh (namespace: database)
│       └── network-policy.yaml         # Cô lập traffic vào Redis (namespaceSelector + podSelector AND)
├── monitoring/                         # Cấu hình giám sát (Huy + Phúc phụ trách)
│   ├── values.yaml                     # Values cho Helm (tắt etcd/scheduler K3s; serviceMonitorSelectorNilUsesHelmValues=false)
│   └── dashboards/                     # Dashboard as Code (Phúc phụ trách - ConfigMap JSON)
├── scripts/                            # Kịch bản tự động hóa kiểm chứng (Long phụ trách)
│   └── demo-all.sh                     # Bash script chạy tự động 3 kịch bản demo
└── .github/workflows/                  # Đường ống CI/DevSecOps (Long phụ trách)
    └── ci-devsecops.yml                # Workflow: Gitleaks + Trivy (FS & Image) + Build & Push GHCR
```

---

## 6. Kế hoạch triển khai 8 tuần

| Tuần | Mục tiêu hoàn thành (Definition of Done) | Người phụ trách chính |
|:---:|:---|:---|
| **Tuần 1** | Thông mạng Tailscale 3 node K3s; chốt hợp đồng API & biến môi trường giữa Phúc và Huy; app Hello World chạy local; Huy và Long dựng khung manifest & CI trên k3d. | Sỹ, Phúc, Huy, Long |
| **Tuần 2** | Cụm K3s nhận đủ 3 node `Ready`, taint Control Plane; cài ArgoCD; build Dockerfile `node:24-alpine` non-root chuẩn. | Sỹ, Phúc |
| **Tuần 3** | Thêm Redis vào app local; pipeline CI build và push image lên GHCR; ArgoCD sync app 2 tầng lên cụm; kiểm tra sớm NetworkPolicy enforcement. | Long, Phúc, Huy |
| **Tuần 4** | Tích hợp Gitleaks, Trivy vào CI; viết Terraform quản lý DNS Cloudflare; cấu hình Traefik Ingress HTTPS; bắt đầu viết báo cáo đồ án song song. | Long, Sỹ, Cả nhóm |
| **Tuần 5** | Hoàn thiện SecurityContext trên Deployment; tinh chỉnh NetworkPolicy chuẩn AND logic; viết kịch bản bash script `scripts/demo-all.sh`. | Huy, Long |
| **Tuần 6** | Triển khai `kube-prometheus-stack` qua ArgoCD (`ServerSideApply=true`), export Grafana Dashboard thành ConfigMap. | Huy, Phúc, Sỹ |
| **Tuần 7** | Thực nghiệm toàn bộ 3 kịch bản demo (Trivy chặn build, ArgoCD tự phục hồi & rollback, test NetworkPolicy). | Cả nhóm |
| **Tuần 8** | Vùng đệm xử lý lỗi phát sinh, tổng kết số liệu đo đạc, hoàn thiện báo cáo đồ án và chuẩn bị slide thuyết trình. | Cả nhóm |

---

## 7. Kịch bản Demo kiểm chứng

Khi báo cáo đồ án, nhóm chứng minh tính hiệu quả của hệ thống thông qua 3 kịch bản thực tế:

### Kịch bản 1: Kiểm chứng DevSecOps Pipeline (Trivy Gate)
- **Hành động:** Cố tình thêm một thư viện có lỗ hổng CVE nghiêm trọng đã có bản vá (ví dụ `lodash@4.17.20`) vào `package.json` và commit.
- **Kết quả:** Pipeline GitHub Actions dừng lại ở bước Trivy Image Scan với exit code 1 (báo đỏ), từ chối đẩy image lên GHCR và từ chối cập nhật GitOps manifest.

### Kịch bản 2: Kiểm chứng GitOps Self-healing & Rollback (ArgoCD)
- **Tự phục hồi (Self-healing):**
  - Chạy `kubectl scale deploy web -n production-app --replicas=5` $\rightarrow$ ArgoCD phát hiện sai lệch trạng thái mong muốn và tự động kéo số lượng Pod về lại 2.
  - Chạy `kubectl delete deploy web -n production-app` $\rightarrow$ ArgoCD lập tức tái tạo lại Deployment hoàn chỉnh.
- **Rollback tự động:**
  - Thực hiện lệnh `git revert HEAD` trên nhánh chính $\rightarrow$ ArgoCD phát hiện commit hoàn tác và tự động rollback ứng dụng về phiên bản ổn định trước đó.

### Kịch bản 3: Kiểm chứng NetworkPolicy Isolation (3 phép thử)
1. **Phép thử 1 (Khác namespace):** Chạy Pod từ namespace `default`:
   ```bash
   kubectl run t1 -n default --rm -it --image=busybox -- nc -zv -w 3 redis.database.svc.cluster.local 6379
   ```
   $\rightarrow$ **Kết quả:** Timeout sau 3 giây (kết nối bị DROP).
2. **Phép thử 2 (Cùng namespace nhưng sai label):** Chạy Pod từ namespace `production-app` nhưng không gắn label `app: web`:
   ```bash
   kubectl run t2 -n production-app --rm -it --image=busybox -- nc -zv -w 3 redis.database.svc.cluster.local 6379
   ```
   $\rightarrow$ **Kết quả:** Timeout sau 3 giây (chứng minh điều kiện `podSelector`).
3. **Phép thử 3 (Pod Web hợp lệ):** Kiểm tra từ Pod Web App:
   ```bash
   kubectl exec -n production-app deploy/web -- nc -zv -w 3 redis.database.svc.cluster.local 6379
   ```
   $\rightarrow$ **Kết quả:** Kết nối thành công (`open`).

---

## 8. Tài liệu tham khảo

1. [Tài liệu chính thức K3s - Lightweight Kubernetes](https://docs.k3s.io/)
2. [Tài liệu chính thức ArgoCD GitOps](https://argo-cd.readthedocs.io/en/stable/)
3. [Tài liệu Aqua Security Trivy](https://aquasecurity.github.io/trivy/)
4. [Tài liệu Gitleaks Secret Scanner](https://github.com/gitleaks/gitleaks)
5. [Tài liệu HashiCorp Terraform Cloudflare Provider](https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs)
6. [Tài liệu Prometheus Operator & Kube-Prometheus-Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
7. Giáo trình & bài giảng học phần NT548 - Công nghệ DevOps và Ứng dụng (UIT).
