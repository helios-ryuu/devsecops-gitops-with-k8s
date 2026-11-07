# WORK BREAKDOWN STRUCTURE (WBS) - TINH GIẢN
## ĐỒ ÁN MÔN HỌC: HỆ THỐNG DEVSECOPS & GITOPS TRÊN HẠ TẦNG KUBERNETES HYBRID
- **Môn học:** NT548 - Công nghệ DevOps và Ứng dụng (Lớp: NT548.R12 - HK1 2026-2027)
- **Đơn vị:** Khoa Mạng máy tính và Truyền thông — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Thời gian thực hiện:** Bắt đầu Phase 2 từ **01/11/2026**, hoàn thành toàn bộ trước **06/12/2026** (Chốt nghiệm thu: **05/12/2026**)
- **Phân công trách nhiệm:**
  1. **Ngô Tiến Sỹ** (23521367) - **Platform & DevOps Lead**: Quản trị K3s Hybrid, Traefik Ingress, ArgoCD GitOps, CI/CD DevSecOps (GitHub Actions + Trivy/Gitleaks), dựng K8s manifests base và triển khai Prometheus stack 1 lần.
  2. **Trần Hồng Phúc** (23521222) - **Web Fullstack Dev**: Phát triển Frontend Next.js 16 App Router/Tailwind CSS và Backend/API Node.js + Express, tích hợp Redis theo contract; phân biệt probe Next hiện có với readiness/metrics backend cần xác minh; đóng gói runtime theo từng component.
  3. **Điền Quốc Huy** (23520600) - **QA & Observability Report**: Viết testcases, chạy kiểm thử tải nhẹ (Autocannon / Postman), khai thác Grafana UI chụp màn hình dashboard CPU/RAM/traffic và soạn thảo *Báo cáo quan sát & Hiệu năng hệ thống*.
  4. **Đặng Thế Long** (22520804) - **Documentation & Demo Support**: Hỗ trợ Sỹ chạy & lấy log 2 kịch bản Demo (Trivy Gate và ArgoCD Rollback), chủ trì soạn thảo *Báo cáo đồ án môn học NT548* và thiết kế bộ *Slide thuyết trình*.

---


> **Đối chiếu 04/11/2026 — version 0.2.0:** Cập nhật phân vai Next.js Frontend + Express Backend/API + Redis. Giữ nguyên ngày, assignee và cột Status do nhóm báo cáo trong WBS gốc; các trạng thái đó chưa được xác nhận độc lập bằng test/live evidence. Snapshot: `2110eddec91bc3e34137c86fef693095c4afb677`. Bảng evidence/dependencies bên dưới là phần bổ sung, không tự thay lịch cam kết.

## Bảng WBS Chi Tiết Kèm Ngày Tháng (Chuẩn Markdown)

| Giai đoạn (Phase) | Tên công việc (Task Name) | Mô tả (Description) | Người thực hiện (Assignee) | Ngày bắt đầu | Ngày kết thúc | Trạng thái (Status) |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Phase 1: Khởi động dự án** | | | | | | **Đã hoàn thành** |
| 1.1 | Chọn ý tưởng & Chốt đề tài | Lựa chọn đề tài Xây dựng hệ thống DevSecOps và GitOps trên hạ tầng K8s Hybrid; tinh giản phạm vi phù hợp năng lực nhóm. | Cả nhóm | 25/10/2026 | 26/10/2026 | Đã hoàn thành |
| 1.2 | Thống nhất công nghệ sử dụng | Chốt stack: K3s, Tailscale, Cloudflare DNS (UI), GitHub Actions (Trivy, Gitleaks), ArgoCD, Prometheus/Grafana; Frontend Next.js 16 + Backend/API Node.js/Express + Redis (phân vai được người dùng xác nhận ngày 04/11/2026). | Cả nhóm | 27/10/2026 | 28/10/2026 | Đã hoàn thành |
| 1.3 | Phân định trách nhiệm & Vai trò | Phân công mới: Sỹ làm 85-90% DevOps/K8s/CI/CD, Phúc làm Web App, Huy làm QA/Observability, Long làm Báo cáo/Slide. | Ngô Tiến Sỹ | 29/10/2026 | 31/10/2026 | Đã hoàn thành |
| **Phase 2: Phân tích & Thiết kế** | | | | | | **Đã hoàn thành** |
| 2.1 | Tạo cấu trúc phân rã công việc (WBS) | Lập kế hoạch chi tiết, phân rã công việc tinh giản, thiết lập mốc hoàn thành trước 05/12/2026 và đưa lên Sheet. | Ngô Tiến Sỹ | 01/11/2026 | 02/11/2026 | Đã hoàn thành |
| 2.2 | Thiết kế kiến trúc K3s Hybrid & GitOps | Vẽ sơ đồ kiến trúc tổng thể (Control Plane VPS + 2 Worker On-prem qua Tailscale Overlay, Traefik Ingress, GitOps ArgoCD). | Ngô Tiến Sỹ | 03/11/2026 | 03/11/2026 | Đã hoàn thành |
| 2.3 | Thiết kế Monorepo & Quy trình Git | Chuẩn hóa cấu trúc thư mục repo: `app/`, `k8s-manifests/`, `argocd/`, `monitoring/`, `scripts/`, `.github/`, `secrets/`, `traefik`. | Ngô Tiến Sỹ | 04/11/2026 | 04/11/2026 | Đã hoàn thành |
| 2.4 | Thống nhất API Contract & Môi trường cấu hình | Làm rõ HTTP contract Next/browser <-> Express; Data access Express <-> Redis; config/auth/routing và probes của từng component. Hai probe Next có source; business/API/Data contract và backend source cần đối chiếu, không suy ra từ trạng thái báo cáo. | Trần Hồng Phúc, Ngô Tiến Sỹ | 05/11/2026 | 05/11/2026 | Đã hoàn thành |
| **Phase 3: Triển khai & Tích hợp** | | | | | | **Đang thực hiện** |
| 3.1 | Cài đặt & Kết nối cụm K3s Hybrid 3-Node | Dựng K3s Control Plane trên VPS Ubuntu (6GB RAM), nối 2 Worker Node on-prem (16GB RAM) qua Tailscale Mesh Network; cấu hình Taints. | Ngô Tiến Sỹ | 06/11/2026 | 08/11/2026 | Đã hoàn thành |
| 3.2 | Cấu hình DNS Cloudflare & Traefik Ingress | Trỏ 3 bản ghi Proxied DNS (A: nt548 - Target: IP PUBLIC của Server, CNAME: nt548-grafana, CNAME: nt548-argocd); cấu hình Traefik Helm, TLSStore Cloudflare Origin cert. | Ngô Tiến Sỹ | 09/11/2026 | 10/11/2026 | Đã hoàn thành |
| 3.3 | Phát triển Frontend Next.js + Backend/API Express + Redis | Có scaffold Next.js 16/Tailwind; hoàn thiện UI, xác minh/bổ sung source Express, tích hợp HTTP API và Redis qua backend. Visit counter/AI Office cần scope và AC rõ; chưa coi config Redis là tích hợp hoàn tất. | Trần Hồng Phúc, Ngô Tiến Sỹ | 07/11/2026 | 11/11/2026 | Đang thực hiện |
| 3.4 | Hardening Container & Đóng gói Dockerfile non-root | Đóng gói multi-stage Dockerfile dựa trên `node:26.13.0-alpine3.23`, pnpm, `output: standalone`, chạy quyền non-root UID 10001:10001, tạo `.dockerignore`. | Ngô Tiến Sỹ | 12/11/2026 | 13/11/2026 | Đã hoàn thành |
| 3.5 | Xây dựng Pipeline CI & DevSecOps (GitHub Actions) | Tích hợp Gitleaks quét secret; Trivy quét CVE dependencies & Container image; build & push image lên GHCR; tự động update Kustomize tag; phân quyền repo. | Ngô Tiến Sỹ | 14/11/2026 | 16/11/2026 | Đã hoàn thành |
| 3.6 | Soạn thảo Kubernetes Manifests chuẩn (GitOps Base) | Viết Kustomize manifests: Web App Deployment (UID 10001, seccomp), Service, ConfigMap, Redis LTS 8.2.11 (probes), Ingress Traefik và NetworkPolicy. | Ngô Tiến Sỹ | 17/11/2026 | 18/11/2026 | Đã hoàn thành |
| 3.7 | Khởi tạo & Cấu hình ArgoCD GitOps Continuous Delivery | Cài đặt ArgoCD lên K3s qua Helm, ghim Worker affinity, cấu hình Ingress Traefik, tạo Application CRD (`app.yaml`) với `ServerSideApply` và auto-create namespace. | Ngô Tiến Sỹ | 19/11/2026 | 20/11/2026 | Đã hoàn thành |
| **Phase 4: Đo kiểm, Bảo mật & Giám sát** | | | | | | **Đang thực hiện** |
| 4.1 | Triển khai Hệ thống Giám sát kube-prometheus-stack | Cấu hình Helm values và ArgoCD Application `monitoring.yaml` theo cơ chế Multiple Sources ($values từ Git + chart Prometheus) với `ServerSideApply=true`. | Ngô Tiến Sỹ | 21/11/2026 | 22/11/2026 | Đang thực hiện (Đã hoàn thiện file values & app CRD - Chờ kích hoạt) |
| 4.2 | Đo kiểm chức năng & Kiểm thử tải Web | Viết testcases và chạy kiểm thử tải cơ bản bằng Autocannon hoặc Postman để kích thích phát sinh traffic và metrics. | Điền Quốc Huy | 23/11/2026 | 24/11/2026 | Chưa bắt đầu |
| 4.3 | Khai thác Grafana & Soạn Báo cáo Quan sát | Đăng nhập Grafana UI, chụp ảnh biểu đồ CPU, RAM, HTTP request rate, trạng thái Pod và viết Báo cáo Quan sát (Observability). | Điền Quốc Huy | 25/11/2026 | 26/11/2026 | Chưa bắt đầu |
| 4.4 | Thực nghiệm & Thu thập log 2 kịch bản Demo | Chuẩn bị script `demo.sh` chế độ non-destructive; chạy thử và ghi nhận log/ảnh minh chứng: (1) Trivy Gate chặn commit dính CVE, (2) ArgoCD Self-healing & Git Rollback. | Đặng Thế Long, Ngô Tiến Sỹ | 27/11/2026 | 28/11/2026 | Đang thực hiện (Script demo đã sẵn sàng) |
| **Phase 5: Báo cáo & Nghiệm thu** | | | | | | **Chưa bắt đầu** |
| 5.1 | Soạn thảo Báo cáo đồ án môn học hoàn chỉnh | Viết tài liệu báo cáo NT548: kiến trúc K3s Hybrid, DevSecOps pipeline, ArgoCD GitOps, kết quả đo kiểm tải và giám sát Grafana. | Đặng Thế Long, Cả nhóm | 29/11/2026 | 01/12/2026 | Chưa bắt đầu |
| 5.2 | Thiết kế Slide thuyết trình & Kịch bản Demo | Thiết kế bộ slide báo cáo tổng kết, chuẩn bị flow thuyết trình và kịch bản demo live ngắn gọn, trực quan. | Đặng Thế Long, Điền Quốc Huy | 02/12/2026 | 03/12/2026 | Chưa bắt đầu |
| 5.3 | Nghiệm thu nội bộ & Đóng gói sản phẩm trước 05/12 | Diễn tập thuyết trình thử, rà soát mã nguồn repo, kiểm tra tính sẵn sàng của cụm K3s và đóng gói sản phẩm hoàn tất trước 05/12/2026. | Cả nhóm | 04/12/2026 | 05/12/2026 | Chưa bắt đầu |

## Đối chiếu bằng chứng và dependencies kỹ thuật

| WBS | Trạng thái báo cáo gốc | Bằng chứng tại snapshot | Phần còn thiếu / gate |
|---|---|---|---|
| 1.2 | Đã hoàn thành | Người dùng xác nhận Next.js Frontend + Express Backend/API + Redis; source Next có trong repo | Không đồng nhất lựa chọn stack với tiến độ triển khai từng component |
| 2.4 | Đã hoàn thành | Có ConfigMap và hai probe Next; chưa thấy OpenAPI/Data contract hoặc source Express | Cần provider/consumer, auth, routing, business API và Data contract |
| 3.3 | Đang thực hiện | Next scaffold; không thấy Express/client Redis trong snapshot | Cần UI nghiệp vụ, source backend và E2E Next/browser -> Express -> Redis |
| 3.4 | Đã hoàn thành | Dockerfile hiện build Next standalone bằng Node image ghi trong file, non-root | Build evidence/backend packaging chưa xác minh; không tự tạo Dockerfile mới |
| 3.5 / 3.7 | Đã hoàn thành | Có workflow context app/ và ArgoCD/Kustomize source | Không tự kết luận delivery backend độc lập đã sẵn sàng; live pipeline/cluster chưa review |
| 3.6 | Đã hoàn thành | Web/Redis/NetworkPolicy manifests; root namespace production-app | Cấu hình không chứng minh live; không coi database/ là namespace database riêng |
| 4.1 | Đang thực hiện | Có cấu hình monitoring | Endpoint HTTP metrics/prom-client/source backend và scrape evidence chưa thấy |

### Phân rã phụ thuộc cho task 3.3 — đề xuất làm rõ công việc

Các nhãn con dưới đây chỉ là phân rã tài liệu dưới 3.3; không bổ sung lịch/assignee cam kết mới.

| Hạng mục | Trách nhiệm / deliverable | Phụ thuộc | Điều kiện xác nhận |
|---|---|---|---|
| 3.3-FE | Next.js UI và API consumption | Scope/AC, 2.4 HTTP contract | UI nghiệp vụ + test/AC; scaffold một mình chưa đủ |
| 3.3-BE | Source Node.js + Express, rules/validation/errors và Redis adapter | 2.4 HTTP/Data contract; vị trí source thực | Có source và kiểm thử backend; không suy từ Next server.js |
| 3.3-INT | Luồng frontend/browser -> Express -> Redis | 3.3-FE, 3.3-BE; routing/auth/config được chốt | E2E success/failure/dependency tests |
| 3.4 + 4.1 | Packaging, probes và metrics từng component | Source entry points, readiness/metrics semantics | Build/startup + endpoint/scrape evidence trước khi báo live PASS |
| 4.2 | Đo kiểm chức năng/tải theo scope | Integration baseline + NFR targets có nguồn | Kết quả test thực tế, không suy từ deadline hoặc label hoàn thành |

Milestones do người dùng cung cấp: Web App cơ bản 11/11/2026; Docker/metrics 13/11/2026; nghiệm thu 05/12/2026. Giữ lịch gốc trong bảng trên; các nguồn lực/dependencies mới cần được người phụ trách điều phối, không tự kéo deadline.

Canonical phân vai và trạng thái: [Technology Stack](docs/technology-stack.md). Luồng hiện có/tích hợp: [System Architecture](docs/architecture.md). Handoff BRD/FRD/API/Data/Migration: [BA alignment](docs/ba-documentation-alignment.md).
