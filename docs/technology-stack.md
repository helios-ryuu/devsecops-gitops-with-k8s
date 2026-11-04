# NT548 — Technology Stack

| Document ID | Version | Status | Date | Owner role | Upstream |
|---|---|---|---|---|---|
| NT548-STACK | 0.2.0 | Draft — đối chiếu source | 2026-11-04 | Web Fullstack / Platform Lead | Xác nhận của người dùng; README/WBS tại commit 2110eddec91bc3e34137c86fef693095c4afb677 |

Thay đổi 0.2.0: làm rõ hệ thống sử dụng đồng thời **Next.js 16 (Frontend), Node.js + Express (Backend/API), Redis (data store)**. Việc nhìn thấy Next.js trong source không có nghĩa Express bị thay thế. Mức triển khai được ghi riêng, không suy ra từ lựa chọn công nghệ.

## Vai trò và dependencies

| Công nghệ | Vai trò / trách nhiệm | Phụ thuộc / giao tiếp | Bằng chứng và trạng thái |
|---|---|---|---|
| Next.js 16 + React | Frontend: routing trang, render giao diện và tương tác người dùng; gọi API nghiệp vụ theo contract | Chạy trên Node.js khi build/standalone; browser nhận HTML/assets. Dữ liệu nghiệp vụ dự kiến lấy từ Express qua HTTP; việc gọi từ browser hay SSR cần chốt | `app/package.json` khai báo Next 16.4.3; `page.tsx` còn starter UI; đã có scaffold, chưa có bằng chứng giao diện AI Office hoàn chỉnh |
| Node.js | Runtime JavaScript, dùng cho frontend build/server và backend Express; Node.js không đồng nghĩa Express | Phiên bản runtime cần xác minh riêng cho từng process/image | Dockerfile hiện tại của Next ghi `node:26.13.0-alpine3.23`; Node 24 là định hướng backend được cung cấp trước đó, chưa thấy source/image backend để xác minh; không thay Dockerfile |
| Express | Backend/API: xử lý HTTP nghiệp vụ, validation, rules, định dạng phản hồi/lỗi và truy cập Redis qua adapter/client | Chạy trên Node.js; nhận request từ frontend/client; kết nối Redis phía server; port, route, package và cách triển khai cần bổ sung bằng chứng | Vai trò do người dùng xác nhận; không tìm thấy package/entry point Express trong toàn bộ tree của snapshot main; tiến độ thực tế ngoài snapshot chưa xác minh |
| Redis | Data store cho nghiệp vụ đã chốt; visit counter được README/WBS nhắc tới; entities AI Office chưa được chốt | Backend Express dự kiến là nơi đọc/ghi nghiệp vụ. Browser không kết nối Redis; frontend không sở hữu Redis credentials | Manifest Deployment/Service có trong repo; ConfigMap có REDIS_HOST/PORT nhưng chưa thấy client sử dụng; chưa kiểm thử kết nối, keys, TTL, durability hoặc triển khai live |
| TypeScript / JavaScript | Ngôn ngữ nguồn theo từng component | Frontend hiện có `.tsx`/`.ts`; ngôn ngữ và toolchain backend cần đối chiếu source riêng | TypeScript frontend đã quan sát; không mô tả toàn bộ hệ thống là JavaScript thuần |
| Tailwind CSS | Styling frontend | Toolchain frontend | Khai báo và sử dụng class trong scaffold; không chứng minh UI sản phẩm đã hoàn thiện |
| Three.js / 3D Chibi Office | Ý tưởng trực quan hóa frontend | Nếu được chọn, sử dụng dữ liệu từ API; thư viện UI không thay backend | Định hướng mở rộng/MVP trước đó; chưa có dependency/source Three.js trong snapshot target; repo tham khảo không là bằng chứng triển khai |
| SSE | Kênh cập nhật một chiều backend -> browser nếu yêu cầu realtime được chốt | Cần event contract, auth, reconnect, retention và proxy timeout tương ứng | Đang dự kiến; chưa thấy endpoint SSE; không cam kết replay/durable events |
| Docker | Đóng gói runtime triển khai | Dockerfile hiện build Next standalone bằng pnpm | Có cấu hình frontend non-root UID/GID 10001; chưa có Dockerfile Express trong snapshot; không suy ra build đã thành công |
| K3s / Traefik / ArgoCD / GitHub Actions | Hạ tầng và chuỗi delivery | Ingress -> Web Service; GitHub Actions -> image -> GitOps; ArgoCD áp manifests | Có cấu hình trong repo; trạng thái cluster/pipeline live chưa được kiểm chứng trong lần review này |
| Prometheus / Grafana | Thu thập metrics và quan sát | Cần endpoint/exporter và scrape target đã chốt cho mỗi component | Có cấu hình monitoring; chưa thấy `prom-client` hoặc `/metrics` trong source ứng dụng; không tuyên bố đã scrape HTTP metrics nghiệp vụ |
| PHP + Laravel | Hướng thay thế backend dài hạn | Giữ business/API/Data contract và tương thích frontend Next.js | Ý định tương lai; không thay Next.js và không phải component hiện tại đã xác minh |

## Ranh giới trách nhiệm

- Frontend sở hữu trải nghiệm hiển thị; nghiệp vụ và dữ liệu đi qua backend/API. Next route handlers có thể tồn tại cho nhu cầu kỹ thuật; hai probe hiện tại thuộc Next, không chứng minh backend Express đã có.
- Express sở hữu API nghiệp vụ theo thiết kế đã xác nhận; backend dùng Redis client phía server. Chưa có contract được chốt nên không tự thêm endpoint, enum, Redis key hoặc TTL.
- Node.js là dependency runtime của các process liên quan. Tag image frontend không xác định phiên bản Node của backend; `server.js` trong Next standalone không tự trở thành Express entry point.
- Redis không phải REST endpoint và không lộ cổng 6379 ra browser. Việc Redis có manifest hoặc biến môi trường không chứng minh frontend/backend đã tích hợp dữ liệu.

## Các trạng thái cần giữ riêng

`Đã có source` / `đã có cấu hình` / `người dùng xác nhận vai trò` / `đang dự kiến` / `đã kiểm thử hoặc triển khai live` là các loại bằng chứng khác nhau. Lần review này không thực thi build, test ứng dụng hoặc kiểm tra cluster, nên không đánh dấu live PASS.

Nguồn, luồng giao tiếp và câu hỏi: [System Architecture](architecture.md). Tác động tới BRD/FRD/API/Data/Migration: [BA alignment](ba-documentation-alignment.md). Tiến độ và dependencies công việc: [WBS](../WBS.md).

## Validation

PASS về phân vai tài liệu: Next.js và Express cùng tồn tại trong mô hình đã xác nhận; runtime Node.js tách khỏi framework; Redis là dependency phía server. BLOCKED về xác thực backend source/live integration, phiên bản backend, API/Data contract và metrics nghiệp vụ. Không chỉnh application code hoặc infrastructure configuration.
