# WORK BREAKDOWN STRUCTURE (WBS) - TINH GIẢN
## ĐỒ ÁN MÔN HỌC: HỆ THỐNG DEVSECOPS & GITOPS TRÊN HẠ TẦNG KUBERNETES HYBRID
- **Môn học:** NT548 - Công nghệ DevOps và Ứng dụng (Lớp: NT548.R12 - HK1 2026-2027)
- **Đơn vị:** Khoa Mạng máy tính và Truyền thông — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Thời gian thực hiện:** Bắt đầu Phase 2 từ **01/11/2026**, hoàn thành toàn bộ trước **06/12/2026** (Chốt nghiệm thu: **05/12/2026**)
- **Phân công trách nhiệm:**
  1. **Ngô Tiến Sỹ** (23521367) - **Platform & DevOps Lead**: Quản trị K3s Hybrid, Traefik Ingress, ArgoCD GitOps, CI/CD DevSecOps (GitHub Actions + Trivy/Gitleaks), dựng K8s manifests base và triển khai Prometheus stack 1 lần.
  2. **Trần Hồng Phúc** (23521222) - **Web Fullstack Dev**: Viết code ứng dụng Web 2 tầng (Giao diện UI đẹp + API Express + Redis đếm view), tích hợp endpoint `/metrics` (`prom-client`), đóng gói Dockerfile non-root.
  3. **Điền Quốc Huy** (23520600) - **QA & Observability Report**: Viết testcases, chạy kiểm thử tải nhẹ (Autocannon / Postman), khai thác Grafana UI chụp màn hình dashboard CPU/RAM/traffic và soạn thảo *Báo cáo quan sát & Hiệu năng hệ thống*.
  4. **Đặng Thế Long** (22520804) - **Documentation & Demo Support**: Hỗ trợ Sỹ chạy & lấy log 2 kịch bản Demo (Trivy Gate và ArgoCD Rollback), chủ trì soạn thảo *Báo cáo đồ án môn học NT548* và thiết kế bộ *Slide thuyết trình*.

---

## Bảng WBS Chi Tiết Kèm Ngày Tháng (Chuẩn Markdown)

| Giai đoạn (Phase) | Tên công việc (Task Name) | Mô tả (Description) | Người thực hiện (Assignee) | Ngày bắt đầu | Ngày kết thúc | Trạng thái (Status) |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Phase 1: Khởi động dự án** | | | | | | **Đã hoàn thành** |
| 1.1 | Chọn ý tưởng & Chốt đề tài | Lựa chọn đề tài Xây dựng hệ thống DevSecOps và GitOps trên hạ tầng K8s Hybrid; tinh giản phạm vi phù hợp năng lực nhóm. | Cả nhóm | 25/10/2026 | 26/10/2026 | Đã hoàn thành |
| 1.2 | Thống nhất công nghệ sử dụng | Chốt stack: K3s, Tailscale, Cloudflare DNS (UI), GitHub Actions (Trivy, Gitleaks), ArgoCD, Prometheus/Grafana, Node.js + Redis. | Cả nhóm | 27/10/2026 | 28/10/2026 | Đã hoàn thành |
| 1.3 | Phân định trách nhiệm & Vai trò | Phân công mới: Sỹ làm 85-90% DevOps/K8s/CI/CD, Phúc làm Web App, Huy làm QA/Observability, Long làm Báo cáo/Slide. | Ngô Tiến Sỹ | 29/10/2026 | 31/10/2026 | Đã hoàn thành |
| **Phase 2: Phân tích & Thiết kế** | | | | | | **Đang thực hiện** |
| 2.1 | Tạo cấu trúc phân rã công việc (WBS) | Lập kế hoạch chi tiết, phân rã công việc tinh giản, thiết lập mốc hoàn thành trước 05/12/2026 và đưa lên Sheet. | Ngô Tiến Sỹ | 01/11/2026 | 02/11/2026 | Đang thực hiện |
| 2.2 | Thiết kế kiến trúc K3s Hybrid & GitOps | Vẽ sơ đồ kiến trúc tổng thể (Control Plane VPS + 2 Worker On-prem qua Tailscale Overlay, Traefik Ingress, GitOps ArgoCD). | Ngô Tiến Sỹ | 03/11/2026 | 03/11/2026 | Chưa bắt đầu |
| 2.3 | Thiết kế Monorepo & Quy trình Git | Chuẩn hóa cấu trúc thư mục repo: `app/`, `k8s-manifests/`, `argocd/`, `monitoring/`, `scripts/`, `.github/`. | Ngô Tiến Sỹ, Đặng Thế Long | 04/11/2026 | 04/11/2026 | Chưa bắt đầu |
| 2.4 | Thống nhất API Contract & Môi trường cấu hình | Chốt giao thức kết nối Web <-> Redis, biến môi trường (ConfigMap), endpoints `/healthz`, `/ready`, `/metrics`. | Trần Hồng Phúc, Ngô Tiến Sỹ | 05/11/2026 | 05/11/2026 | Chưa bắt đầu |
| **Phase 3: Triển khai & Tích hợp** | | | | | | **Chưa bắt đầu** |
| 3.1 | Cài đặt & Kết nối cụm K3s Hybrid 3-Node | Dựng K3s Control Plane trên VPS Ubuntu (6GB RAM), nối 2 Worker Node on-prem (16GB RAM) qua Tailscale Mesh Network; cấu hình Taints. | Ngô Tiến Sỹ | 06/11/2026 | 08/11/2026 | Chưa bắt đầu |
| 3.2 | Cấu hình DNS Cloudflare & Traefik Ingress | Trỏ bản ghi DNS trên giao diện Cloudflare về IP VPS; cấu hình Traefik Ingress định tuyến traffic HTTPS vào ứng dụng. | Ngô Tiến Sỹ | 09/11/2026 | 10/11/2026 | Chưa bắt đầu |
| 3.3 | Phát triển ứng dụng Web 2 tầng (Node.js + Redis) | Vibe code ứng dụng Express: giao diện hiển thị lượt truy cập, kết nối Redis đếm view, xử lý lỗi cơ bản. | Trần Hồng Phúc | 07/11/2026 | 11/11/2026 | Chưa bắt đầu |
| 3.4 | Hardening Container & Đóng gói Dockerfile non-root | Tích hợp `/metrics` (`prom-client`), đóng gói multi-stage Dockerfile dựa trên `node:24-alpine`, chạy quyền non-root UID 10001. | Trần Hồng Phúc, Ngô Tiến Sỹ | 12/11/2026 | 13/11/2026 | Chưa bắt đầu |
| 3.5 | Xây dựng Pipeline CI & DevSecOps (GitHub Actions) | Tích hợp Gitleaks quét secret; Trivy quét CVE dependencies & Container image; build & push image lên GHCR; tự động update Git tag. | Ngô Tiến Sỹ | 14/11/2026 | 16/11/2026 | Chưa bắt đầu |
| 3.6 | Soạn thảo Kubernetes Manifests chuẩn (GitOps Base) | Viết manifests Web App (SecurityContext non-root), Service, ConfigMap và Redis Deployment/Service. | Ngô Tiến Sỹ | 17/11/2026 | 18/11/2026 | Chưa bắt đầu |
| 3.7 | Khởi tạo & Cấu hình ArgoCD GitOps Continuous Delivery | Cài đặt ArgoCD lên cụm K3s, tạo Application CRD (`app.yaml`) với `directory: {recurse: true}`, bật `selfHeal: true` và `prune: true`. | Ngô Tiến Sỹ | 19/11/2026 | 20/11/2026 | Chưa bắt đầu |
| **Phase 4: Đo kiểm, Bảo mật & Giám sát** | | | | | | **Chưa bắt đầu** |
| 4.1 | Triển khai Hệ thống Giám sát kube-prometheus-stack | Cấu hình Helm values và ArgoCD Application `monitoring.yaml` với `ServerSideApply=true` để deploy Prometheus & Grafana. | Ngô Tiến Sỹ | 21/11/2026 | 22/11/2026 | Chưa bắt đầu |
| 4.2 | Đo kiểm chức năng & Kiểm thử tải Web | Viết testcases và chạy kiểm thử tải cơ bản bằng Autocannon hoặc Postman để kích thích phát sinh traffic và metrics. | Điền Quốc Huy | 23/11/2026 | 24/11/2026 | Chưa bắt đầu |
| 4.3 | Khai thác Grafana & Soạn Báo cáo Quan sát | Đăng nhập Grafana UI, chụp ảnh biểu đồ CPU, RAM, HTTP request rate, trạng thái Pod và viết Báo cáo Quan sát (Observability). | Điền Quốc Huy | 25/11/2026 | 26/11/2026 | Chưa bắt đầu |
| 4.4 | Thực nghiệm & Thu thập log 2 kịch bản Demo | Chạy thử và ghi nhận log/ảnh minh chứng: (1) Trivy Gate chặn commit dính CVE, (2) ArgoCD Self-healing khi xóa Pod & Git Rollback. | Đặng Thế Long, Ngô Tiến Sỹ | 27/11/2026 | 28/11/2026 | Chưa bắt đầu |
| **Phase 5: Báo cáo & Nghiệm thu** | | | | | | **Chưa bắt đầu** |
| 5.1 | Soạn thảo Báo cáo đồ án môn học hoàn chỉnh | Viết tài liệu báo cáo NT548: kiến trúc K3s Hybrid, DevSecOps pipeline, ArgoCD GitOps, kết quả đo kiểm tải và giám sát Grafana. | Đặng Thế Long, Cả nhóm | 29/11/2026 | 01/12/2026 | Chưa bắt đầu |
| 5.2 | Thiết kế Slide thuyết trình & Kịch bản Demo | Thiết kế bộ slide báo cáo tổng kết, chuẩn bị flow thuyết trình và kịch bản demo live ngắn gọn, trực quan. | Đặng Thế Long, Điền Quốc Huy | 02/12/2026 | 03/12/2026 | Chưa bắt đầu |
| 5.3 | Nghiệm thu nội bộ & Đóng gói sản phẩm trước 05/12 | Diễn tập thuyết trình thử, rà soát mã nguồn repo, kiểm tra tính sẵn sàng của cụm K3s và đóng gói sản phẩm hoàn tất trước 05/12/2026. | Cả nhóm | 04/12/2026 | 05/12/2026 | Chưa bắt đầu |