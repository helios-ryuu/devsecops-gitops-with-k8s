# WORK BREAKDOWN STRUCTURE (WBS)
## ĐỒ ÁN MÔN HỌC: HỆ THỐNG DEVSECOPS & GITOPS TRÊN HẠ TẦNG KUBERNETES HYBRID
- **Môn học:** NT548 - Công nghệ DevOps và Ứng dụng (Lớp: NT548.R12 - HK1 2026-2027)
- **Đơn vị:** Khoa Mạng máy tính và Truyền thông — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Thời gian thực hiện:** Bắt đầu Phase 2 từ **01/11/2026**, hoàn thành toàn bộ trước **06/12/2026** (Chốt nghiệm thu: **05/12/2026**)
- **Phân công trách nhiệm:**
  1. **Ngô Tiến Sỹ** (23521367) - **Platform & DevOps Lead**: Quản trị Kubernetes Hybrid (`kubeadm v1.37.1`) trên WireGuard `wg0`, Cilium eBPF LB + Hubble UI, Traefik HA, Longhorn Storage, ArgoCD GitOps, HashiCorp Vault & External Secrets Operator (ESO), Kyverno Policy, CI/CD DevSecOps & Nightly GHCR Trivy Audit, và `kube-prometheus-stack`.
  2. **Trần Hồng Phúc** (23521222) - **Web Fullstack Dev**: Viết code ứng dụng Web 2 tầng (Next.js 16 App Router + Tailwind CSS + Redis đếm lượt truy cập + `APP_ENV`/`APP_VERSION`), tích hợp endpoint `/healthz`, `/ready`, đóng gói Dockerfile non-root (`UID 10001`).
  3. **Điền Quốc Huy** (23520600) - **Observability & Kiểm thử quan sát**: Khai thác Grafana Web UI & Hubble UI, chụp ảnh minh chứng biểu đồ CPU/RAM, lưu lượng Traefik và luồng mạng bị chặn phục vụ dán vào báo cáo, đồng thời phối hợp hoàn thiện tài liệu và slide.
  4. **Đặng Thế Long** (22520804) - **Documentation & Kiểm thử hệ thống**: Phối hợp với Sỹ chạy kiểm thử hệ thống và thu thập log/ảnh minh chứng 5 kịch bản theo `scripts/test.sh`, chủ trì soạn thảo *Báo cáo đồ án môn học NT548*, thiết kế bộ *Slide thuyết trình* và sơ đồ kiến trúc Draw.io.

---

## Bảng WBS Chi Tiết Kèm Ngày Tháng

| Giai đoạn (Phase) | Tên công việc (Task Name) | Mô tả (Description) | Người thực hiện (Assignee) | Ngày bắt đầu | Ngày kết thúc | Trạng thái (Status) |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Phase 1: Khởi động dự án** | | | | | | **Đã hoàn thành** |
| 1.1 | Chọn ý tưởng & Chốt đề tài | Lựa chọn đề tài Xây dựng hệ thống DevSecOps và GitOps trên hạ tầng K8s Hybrid. | Cả nhóm | 25/10/2026 | 26/10/2026 | Đã hoàn thành |
| 1.2 | Thống nhất công nghệ sử dụng | Chốt stack: WireGuard `wg0`, Kubernetes `v1.37.1` (`kubeadm` + `containerd.io 2.3.6`), Cilium eBPF & Hubble UI, Traefik HA, Longhorn, Cloudflare DNS & Zero Trust, GitHub Actions (Gitleaks/Trivy + Cron GHCR), ArgoCD, HashiCorp Vault & ESO (Kubernetes Auth), Kyverno, Prometheus/Grafana, Next.js + Redis. | Cả nhóm | 27/10/2026 | 28/10/2026 | Đã hoàn thành |
| 1.3 | Phân định trách nhiệm & Vai trò | Phân công nhiệm vụ: Sỹ (Platform/DevOps), Phúc (Web App), Huy (Observability/Báo cáo), Long (Báo cáo/Slide/Kiểm thử). | Ngô Tiến Sỹ | 29/10/2026 | 31/10/2026 | Đã hoàn thành |
| **Phase 2: Phân tích & Thiết kế** | | | | | | **Đã hoàn thành** |
| 2.1 | Tạo cấu trúc phân rã công việc (WBS) | Lập kế hoạch chi tiết, thiết lập mốc hoàn thành trước 05/12/2026. | Ngô Tiến Sỹ | 01/11/2026 | 02/11/2026 | Đã hoàn thành |
| 2.2 | Thiết kế kiến trúc Kubernetes Hybrid & GitOps | Thiết kế kiến trúc 2 tầng (`platform-core/` & `project-nt548/`), mạng `wg0` + Cilium eBPF LB, RollingUpdate Zero-Downtime & GitOps ArgoCD. | Ngô Tiến Sỹ | 03/11/2026 | 03/11/2026 | Đã hoàn thành |
| 2.3 | Thiết kế Monorepo & Quy trình Git | Chuẩn hóa cấu trúc thư mục repo: `wireguard/`, `kubeadm-config/`, `platform-core/`, `project-nt548/`, `app/`, `scripts/`, `.github/workflows/`. | Ngô Tiến Sỹ | 04/11/2026 | 04/11/2026 | Đã hoàn thành |
| 2.4 | Thống nhất API Contract & Môi trường cấu hình | Chốt giao thức kết nối Web <-> Redis auth, ConfigMap (`APP_ENV`, `REDIS_HOST`), endpoints `/healthz`, `/ready`. | Trần Hồng Phúc, Ngô Tiến Sỹ | 05/11/2026 | 05/11/2026 | Đã hoàn thành |
| **Phase 3: Triển khai & Tích hợp** | | | | | | **Đã hoàn thành** |
| 3.1 | Cài đặt & Kết nối cụm Kubernetes Hybrid 3-Node | Dựng WireGuard `wg0` + khóa Cloud NSG (tắt host firewall) + `sysctl`, cài `containerd.io 2.3.6` + `kubeadm v1.37.1` Control Plane (`server-01` 6GB RAM) & 2 Worker (`worker-01`/`worker-02` 8GB RAM), cài Cilium eBPF LB + Hubble UI + Longhorn + HashiCorp Vault & ESO (Kubernetes Auth). | Ngô Tiến Sỹ | 06/11/2026 | 08/11/2026 | Đã hoàn thành |
| 3.2 | Cấu hình DNS Cloudflare, Traefik HA & Zero Trust | Trỏ DNS (`A vps.helios.id.vn` -> `<VPS_PUBLIC_IP>` DNS Only; `CNAME` `nt548.helios.id.vn`, `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn` -> `vps.helios.id.vn`); cấu hình Traefik HA (`LoadBalancer`), TLSStore `cloudflare-origin-tls` và Cloudflare Access `K8s Admin`. | Ngô Tiến Sỹ | 09/11/2026 | 10/11/2026 | Đã hoàn thành |
| 3.3 | Phát triển ứng dụng Web 2 tầng (Next.js + Redis) | Hoàn thiện Next.js 16 App Router + Tailwind CSS + client Redis thuần (`node:net`), hiển thị `APP_ENV` / `APP_VERSION` và bộ đếm truy cập. | Trần Hồng Phúc, Ngô Tiến Sỹ | 07/11/2026 | 11/11/2026 | Đã hoàn thành |
| 3.4 | Hardening Container & Đóng gói Dockerfile non-root | Đóng gói multi-stage Dockerfile (`node:26.13.1-alpine3.24`, pnpm, `output: standalone`, UID `10001:10001` non-root). | Ngô Tiến Sỹ | 12/11/2026 | 13/11/2026 | Đã hoàn thành |
| 3.5 | Xây dựng Pipeline CI/CD DevSecOps & Nightly Cron | Tích hợp `ci.yml` (Gitleaks, Trivy FS/Config/Image, `kubeconform`, cập nhật tag `deployment.yaml` & lịch cron `0 0 * * *` quét GHCR). | Ngô Tiến Sỹ | 14/11/2026 | 16/11/2026 | Đã hoàn thành |
| 3.6 | Soạn thảo Kubernetes Manifests & Kyverno Policies | Hoàn thiện manifests YAML thuần (`web-deployment` `RollingUpdate` `replicas: 2`, `redis-statefulset`, `NetworkPolicy`) và 4 Kyverno `ValidatingPolicy` (CEL). | Ngô Tiến Sỹ | 17/11/2026 | 18/11/2026 | Đã hoàn thành |
| 3.7 | Khởi tạo & Cấu hình ArgoCD GitOps | Cấu hình ArgoCD (`platform-core/argocd/values.yaml`) và GitOps Application Tầng 2 (`project-nt548/app-prod.yaml` với nhãn `policy-tier=hardened`). | Ngô Tiến Sỹ | 19/11/2026 | 20/11/2026 | Đã hoàn thành |
| **Phase 4: Đo kiểm, Bảo mật & Giám sát** | | | | | | **Đang thực hiện** |
| 4.1 | Triển khai Hệ thống Giám sát `kube-prometheus-stack` | Đồng bộ Prometheus (Longhorn 10Gi) + Grafana (Longhorn 5Gi) + ServiceMonitors (Cilium/Hubble, Traefik, Longhorn, ArgoCD). | Ngô Tiến Sỹ | 21/11/2026 | 22/11/2026 | Đã hoàn thành |
| 4.2 | Khai thác Grafana & Hubble UI chụp ảnh quan sát cho báo cáo | Chụp các biểu đồ CPU, RAM, lưu lượng Traefik và luồng NetworkPolicy `DROPPED` trên Hubble UI bổ sung cho mục 4.4 và 4.5 của báo cáo. | Điền Quốc Huy | 25/11/2026 | 29/11/2026 | Đang thực hiện |
| 4.3 | Kiểm thử hệ thống 5 kịch bản & Thu thập log/ảnh minh chứng | Chạy kiểm thử theo `scripts/test.sh` (hướng dẫn an toàn) và lưu log, ảnh minh chứng 5 kịch bản hoàn thiện mục 4.4 báo cáo. | Đặng Thế Long, Ngô Tiến Sỹ | 27/11/2026 | 29/11/2026 | Đang thực hiện |
| **Phase 5: Báo cáo & Nghiệm thu** | | | | | | **Đang thực hiện** |
| 5.1 | Soạn thảo Báo cáo đồ án môn học hoàn chỉnh | Đã hoàn thiện `docs/REPORT.md` và đưa nội dung kèm ảnh minh chứng từ Chương 1 đến hết mục 4.3 vào `docs/NT548-R12_Nhom-6_BaoCaoDoAn.docx`; còn lại mục 4.4, 4.5 và Chương 5 sau khi chạy kiểm thử. | Đặng Thế Long, Cả nhóm | 26/11/2026 | 01/12/2026 | Đang thực hiện |
| 5.2 | Thiết kế Slide thuyết trình & Sơ đồ Draw.io | Đã hoàn thiện sơ đồ kiến trúc `diagrams/architecture.drawio` (xuất 2x/4x PNG); tiếp tục thiết kế bộ slide thuyết trình và diễn tập flow kiểm thử live. | Đặng Thế Long, Điền Quốc Huy | 28/11/2026 | 03/12/2026 | Đang thực hiện |
| 5.3 | Nghiệm thu nội bộ & Đóng gói sản phẩm trước 05/12 | Diễn tập thuyết trình thử, rà soát repo, kiểm tra tính sẵn sàng của cụm Kubernetes trước 05/12/2026. | Cả nhóm | 04/12/2026 | 05/12/2026 | Chưa bắt đầu |
