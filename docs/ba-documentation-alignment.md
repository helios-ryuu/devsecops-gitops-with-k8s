# NT548 — BA documentation alignment

| Document ID | Version | Status | Date | Owner role | Upstream |
|---|---|---|---|---|---|
| NT548-BA-ALIGN | 0.2.0 | Draft — impact review | 2026-11-04 | BA / Web Fullstack / Platform | README/WBS snapshot 2110eddec91bc3e34137c86fef693095c4afb677; NT548-STACK/ARCH 0.2.0; xác nhận của người dùng |

Thay đổi: bỏ diễn giải Next.js thay Express. Phân vai chuẩn: Next.js 16 frontend, Node.js + Express backend/API, Redis data store; Laravel là hướng thay backend dài hạn. Xem [Technology Stack](technology-stack.md) cho canonical role/status và [Architecture](architecture.md) cho luồng/dependencies.

## Phạm vi nghiệp vụ và bằng chứng

- DevSecOps/GitOps/Kubernetes Hybrid là bối cảnh đồ án; README/WBS nêu các mục tiêu và phân công. Chưa có rubric học phần trong bộ nguồn đã kiểm tra, nên không biến mọi lựa chọn của nhóm thành yêu cầu bắt buộc của giảng viên.
- Visit counter có trong README/WBS nhưng source trang hiện là starter; không đánh dấu tính năng đếm view hoàn tất.
- AI Agent Workspace/Office Monitor, simulator, Three.js và SSE là ý tưởng/phạm vi dự kiến trước đó. Không tự biến thành chức năng bắt buộc, chốt rules hay coi có agents thật đang chạy.
- Chưa có bộ BRD/FRD/OpenAPI/Data/Migration đầy đủ trong tree target đã kiểm tra. File này là impact note để cập nhật các artifact đó khi có đầu vào, không tạo thay một baseline đã được phê duyệt. Các excerpt Queue Board trong repository skill là ví dụ hư cấu và không áp dụng vào NT548.

## Tác động theo từng tài liệu

| Artifact | Điều chỉnh cần giữ | Dependencies / điều chưa thể xác thực |
|---|---|---|
| BRD | Business problem/goals/scope không được suy ra từ stack; ghi Next/Express/Redis là ràng buộc/decision có nguồn. Tách nghĩa vụ đồ án, release scope và mở rộng | Cần problem/stakeholders/success evidence và authority/rubric trước khi baseline BR |
| FRD | Mô tả UI/actor behavior, business rules và AC độc lập framework; xác định hành vi frontend, backend và lỗi dependency. Probe kỹ thuật không thay FR nghiệp vụ | Cần BR cha, rules/permissions, payload expectations và NFR targets; chưa tự cấp BR/FR IDs giả cho chức năng chưa chốt |
| API Contract | Next/browser là consumer; Express là provider theo phân vai. OpenAPI giữ độc lập Express/Laravel; HTTP business contract tách khỏi probe Next hiện tại | Chưa có endpoints/payload/error/auth baseline; không tự tạo `/api/*`, ports hoặc event schema. Mỗi operation tương lai phải link FR |
| Architecture | Hai framework có trách nhiệm riêng trên runtime Node; Express/Redis data flow cần source; ghi source/config/live riêng | NT548-ARCH 0.2.0 ghi các đường giao tiếp chưa chốt, routing/build context/probes/namespace và gaps |
| Data Contract | Redis mapping hỗ trợ nghiệp vụ/API; backend sở hữu data-access theo đề xuất phân vai. Frontend không mặc định đọc Redis | Cần entities/key patterns, TTL/retention, atomicity/concurrency và recovery evidence. Không dùng keys/TTL từ ví dụ hư cấu |
| Migration Plan | Express -> Laravel thay lớp backend/API; giữ Next frontend là consumer, giữ business/API/Data behavior và Redis semantics đã cam kết | Phải có Express source và baselined contract trước parity/cutover readiness. Next image không phải source backend để migrate |

## Traceability và trình tự cập nhật

Trình tự khởi tạo vẫn là BRD -> FRD -> API -> Architecture -> Data -> Migration, với vòng phản hồi. Hiện chưa đủ baseline để công nhận chuỗi BR -> FR -> operation -> entity là PASS. Dùng đúng IDs có sẵn khi xuất hiện, không dùng E-NT/DEC-NT/Q-NT như business requirements.

1. Giữ xác nhận công nghệ DEC-NT-01 trong architecture; bổ sung nguồn Express vào E-NT-08/Q-NT-01 khi có.
2. Chốt scope/business behavior trước FR/API/Data, nhất là visit counter so với AI Office; không trộn hai phạm vi thành tính năng đã triển khai.
3. Xác định endpoint provider/consumer, routing/SSR/auth, Redis ownership và health/metrics theo từng component.
4. Với nguồn mới, cập nhật trạng thái và source refs, chỉ sửa mô tả ở canonical owner rồi link tài liệu liên quan; kiểm tra tương thích và WBS dependencies.

## Milestones và evidence gates

Giữ các mốc người dùng đã nêu: Web App cơ bản 11/11/2026; Docker/metrics 13/11/2026; nghiệm thu 05/12/2026. Đây là deadline, không là bằng chứng hoàn thành. Ngày/assignee/status gốc trong WBS được bảo toàn; bổ sung evidence table để giải thích các phần chưa xác minh.

| Gate | Bằng chứng cần có | Tình trạng review |
|---|---|---|
| Frontend hoàn thiện | UI nghiệp vụ và AC/test tương ứng | Chỉ thấy scaffold; chưa PASS |
| Frontend -> Express -> Redis | Source backend/client/rules và kiểm thử E2E | BLOCKED trong snapshot |
| Docker/metrics | Build/test của component thực tế, endpoint + scrape evidence | Có frontend Docker config; backend/metrics chưa xác minh |
| Migration compatibility | Baseline contracts + source/target parity + rollback/recovery evidence | Chỉ là hướng dài hạn, chưa sẵn sàng cutover |

## Validation và giới hạn

PASS về consistency mô tả trong README, WBS, Stack và Architecture: ba công nghệ cùng tồn tại đúng vai trò; future work được tách khỏi source/config. BLOCKED về traceability chi tiết và implementation/live readiness do thiếu contract và backend source. Không sửa code, Dockerfile, CI workflow, manifests hoặc hạ tầng; không tạo kết quả test ứng dụng giả.
