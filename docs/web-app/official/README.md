# Bộ tài liệu BA Official — AI Agent Office Monitor

| Document ID | Document version | Status | Date | Owner role | Source / upstream |
|---|---|---|---|---|---|
| WEB-INDEX | 1.0.0 | review | 2026-11-06 | Web Fullstack Dev; phối hợp QA và Platform | Sáu practical documents 0.1.0 tại commit `2ce6d347516b0ea8ca384ae619a2b1718107bda6`; người dùng duyệt tổ chức Official trong phiên hiện tại |

Change log 1.0.0: thiết lập bộ Official, biên tập để dễ đọc và giữ nguyên ID yêu cầu, operationIds, phạm vi, quy tắc và các quyết định còn mở. Các bản practical-test không bị thay thế hoặc chỉnh sửa. Đây là nguồn chính để phát triển Web App; các phần còn `proposed`, `deferred` hoặc `BLOCKED` được giữ đúng trạng thái.

## 1. Đọc theo công việc

| Thứ tự / tài liệu | Trả lời câu hỏi | Người dùng chính |
|---|---|---|
| 1. [BRD](BRD.md) | Cần đạt điều gì, vì sao, ai liên quan và phần nào thuộc phạm vi? | Nhóm dự án, Web owner |
| 2. [FRD](FRD.md) | Hệ thống phải xử lý ra sao, trạng thái chuyển thế nào và kiểm tra bằng tiêu chí nào? | Web Dev, QA |
| 3. [API Contract](api-contract.yaml) | Request/response, status, schema và lỗi HTTP có dạng gì? | Web Dev, Platform, QA |
| 4. [Architecture](architecture.md) | Thành phần nào thực hiện yêu cầu, kết nối ra sao và xử lý lỗi ở đâu? | Web Dev, Platform |
| 5. [Data Contract](data-contract.md) | Dữ liệu có ý nghĩa gì, ai cập nhật và được lưu/khôi phục thế nào? | Web Dev, Platform, QA |
| 6. [Migration Plan](migration-plan.md) | Khi nào có thể thay Express bằng Laravel mà giữ đúng hành vi và dữ liệu? | Web owner, Platform, QA; định hướng tương lai |

Chuỗi truy vết: **BR → FR/RULE/AC → operationId hoặc lý do không dùng HTTP → ENT/data mapping**. NFR được liên kết với control và cách kiểm chứng tại Architecture. Migration phải bảo toàn baseline được chốt của năm tài liệu trước, không tự sửa baseline đó.

Mỗi loại nội dung có một nơi định nghĩa chính: nhu cầu/scope tại BRD; hành vi và acceptance criteria tại FRD; wire schema tại API; components/ADRs tại Architecture; storage/lifecycle tại Data; parity/cutover/rollback tại Migration. Registry E/A/C/Q dùng chung nằm ở các phần 4–6 dưới đây.

## 2. Hiểu đúng trạng thái

Các nhóm trạng thái sau mô tả những việc khác nhau; không dùng chúng thay thế nhau.

| Nhóm | Giá trị cần phân biệt | Cách hiểu |
|---|---|---|
| Vòng đời tài liệu | `review` | Bản Official đang được review; việc tạo tài liệu không tự phê duyệt mọi yêu cầu bên trong |
| Cam kết yêu cầu / quyết định | `requested`, `proposed`, `deferred`, `accepted` | Requested: nhu cầu/nghĩa vụ được cung cấp; Proposed: cách đặc tả/giải pháp đang đề xuất; Deferred: chưa đưa vào phạm vi hiện tại; Accepted chỉ ghi khi có quyết định và nguồn rõ |
| Bằng chứng triển khai | `code-observed`, `configured`, `planned`, `tested`, `unknown` | Đã đọc code; đã thấy cấu hình; dự kiến; đã chạy kiểm chứng; hoặc chưa biết. Code/config không tự chứng minh runtime |
| Kết quả kiểm tra / điều kiện thực hiện | `PASS`, `FAIL`, `BLOCKED`, `N/A` | Đạt trong phạm vi đã kiểm tra; không đạt; thiếu quyết định/bằng chứng; hoặc không áp dụng kèm lý do |
| Phần chưa xác định | `TBD`, mã `Q-…` | Giá trị/quyết định còn mở; theo registry, không tự điền default như TTL, deadline hoặc scope |

`Mandatory` trong BRD là nghĩa vụ theo đầu vào người dùng được ghi lại ở E-100, chưa phải rubric học phần được kiểm chứng độc lập. `Proposed MVP Extension` chỉ áp dụng khi được chọn release. Việc duyệt cấu trúc Official không tự chọn extension hoặc phê duyệt migration.

Các status vận hành HTTP được giải thích cạnh bảng API tại FRD; agent state và task status được giải thích cạnh state machine. Các thuật ngữ dữ liệu như TTL/atomicity/durability được giải thích tại Data, không lặp glossary ở mọi tài liệu.

## 3. Version và nguồn chuyển đổi

| Bản nguồn giữ nguyên | Bản Official | Document ID mới |
|---|---|---|
| [01-BRD.md](../validation/practical-test/01-BRD.md), PT-BRD 0.1.0 | [BRD.md](BRD.md) | WEB-BRD 1.0.0 |
| [02-FRD.md](../validation/practical-test/02-FRD.md), PT-FRD 0.1.0 | [FRD.md](FRD.md) | WEB-FRD 1.0.0 |
| [03-api-contract.yaml](../validation/practical-test/03-api-contract.yaml), PT-API document 0.1.0 | [api-contract.yaml](api-contract.yaml) | WEB-API document 1.0.0; **API version vẫn 0.1.0** |
| [04-architecture.md](../validation/practical-test/04-architecture.md), PT-ARCH 0.1.0 | [architecture.md](architecture.md) | WEB-ARCH 1.0.0 |
| [05-data-contract.md](../validation/practical-test/05-data-contract.md), PT-DATA 0.1.0 | [data-contract.md](data-contract.md) | WEB-DATA 1.0.0 |
| [06-migration-plan.md](../validation/practical-test/06-migration-plan.md), PT-MIG 0.1.0 | [migration-plan.md](migration-plan.md) | WEB-MIG 1.0.0 |

Document version 1.0.0 đánh dấu lần biên tập Official đầu tiên, không là tuyên bố API breaking change hay nghiệm thu phần mềm. OpenAPI dialect giữ `3.1.1`; domain schema simulator giữ logical `v1`. Các IDs BR/FR/RULE/AC/NFR/ENT/ADR/MIG/E/A/C/Q/VAL hiện có và ba operationIds được giữ nguyên.

## 4. Registry nguồn và assumptions

Ngày đọc source của practical evaluation: **2026-11-05**, snapshot ứng dụng `2110eddec91bc3e34137c86fef693095c4afb677`. Ngày biên tập Official: **2026-11-06**, nhánh `ba/documentation`, baseline `2ce6d347516b0ea8ca384ae619a2b1718107bda6`. Đây là hai mốc khác nhau; việc biên tập không làm dữ liệu runtime cũ trở thành bằng chứng mới.

| ID | Nguồn / provenance | Nội dung được dùng và giới hạn |
|---|---|---|
| E-100 | Brief người dùng được ghi trong [practical evaluation](../validation/practical-test/evaluation-report.md) | Intent, problem và các scope classes; không phải implementation proof hoặc rubric độc lập |
| E-101 | [README snapshot](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/README.md), §1.2/§2/§6 | Phân công Web, Express/Node24, Redis/probes/metrics, lịch nhóm; source-stated |
| E-102 | [WBS snapshot](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/WBS.md), 2.4/3.3/3.4/4.2 | Next/Redis, kế hoạch và hạn 05/12/2026; status done không là runtime evidence |
| E-103 | [Package](../../../app/package.json), [UI](../../../app/src/app/page.tsx), [healthz](../../../app/src/app/healthz/route.ts), [ready](../../../app/src/app/ready/route.ts) ở snapshot nguồn | Next starter và hai GET handlers; ready luôn 200. Không thấy Express/Redis client/metrics/Three/simulator trong app đã đọc; code-observed, chưa runtime-tested |
| E-104 | [Dockerfile](../../../app/Dockerfile), [Next config](../../../app/next.config.ts), [Kustomization](../../../k8s-manifests/kustomization.yaml), configmap/deployment/Redis/policy | Standalone Next, node26 string, port3000, UID10001, Redis configuration cùng production-app; không volume/PVC trong Redis manifest đã đọc; configured, chưa chứng minh live |
| E-105 | [Validation trước đó](../validation/README.md), [smoke report](../validation/report.md) | Lịch sử thử nghiệm, khác input với practical test; không là scope hiện hành |
| E-106 | Sáu BA Skills, shared standard và templates được practical evaluation ghi lại | Hướng dẫn tạo/review; không phải yêu cầu nghiệp vụ ứng dụng |
| E-107 | Git/status/hash checks được ghi tại [verification record](../validation/practical-test/evaluation-report.md) | Bảo toàn branch/file của lần practical test; không chứng minh tính năng |
| E-108 | [Reference analysis](../validation/practical-test/07-reference-analysis.md), My Office commit `77fdd1371ea1f3a78bd905880b5681deec3b7a45` | Bằng chứng thiết kế và ma trận chọn module; chưa reuse/chạy reference; không biến feature reference thành requirement |

**A-100 — proposed:** simulator cục bộ trong browser đủ cho candidate MVP, không cần shared state. Chủ sở hữu giải pháp: Web owner; decision liên quan ADR-101. Chưa dùng assumption này để đóng Q-100/Q-108 hoặc cam kết lịch sử xuyên phiên. ADR-100..104 thuộc Architecture; ADR-105 thuộc Migration, tất cả vẫn proposed.

## 5. Điểm chưa thống nhất giữa nguồn và implementation

| ID | Nguồn / expected vs observed | Tác động | Hướng xử lý / owner |
|---|---|---|---|
| C-100 | E-100/E-101 nêu Express intended; E-102/E-103 chỉ cho thấy Next | Chưa xác minh source backend và chưa có Express migration baseline; Next có thể đồng tồn tại với Express | Tìm source/ref và chốt boundary Q-108 / Web + Platform |
| C-101 | README nêu Node24, WBS/Dockerfile nêu node26.13.0 string | Chưa thống nhất runtime theo component; chưa chứng minh build/runtime support | Đối chiếu từng deployable / Web + Platform |
| C-102 | README vẽ database namespace; root Kustomization đặt production-app | Host/policy phải theo topology thực tế, không theo tên folder | Xác nhận render/live topology / Platform; không tự đổi manifests |
| C-103 | WBS 2.4 ghi done; `/ready` hiện chỉ trả 200 | Code hiện có chưa thực hiện dependency-aware readiness được đề xuất | Chốt check/deadline/owner và acceptance / Web + QA + Platform |

## 6. Câu hỏi cần chốt trong quá trình phát triển

| Q | Quyết định cần có | Ảnh hưởng / gate | Resolution role / status |
|---|---|---|---|
| Q-100 | Authority/rubric nghiệm thu; release mandatory-only hay thêm office extension? | Chọn extension và phê duyệt yêu cầu; quyền tổ chức Official đã được duyệt riêng | Người dùng/Web owner + nhóm; OPEN |
| Q-101 | Visit là page view/navigation/unique visitor? Refresh/bots/preload/probes, trigger, retries/idempotency, timeout sau write? | FR-101/AC-101/AC-102, counter API và storage | Web owner + QA; OPEN |
| Q-102 | Ai đọc UI/probes/metrics; network exposure, origins/CORS và secrets nếu có? | Access/security integration trước deploy; auth sản phẩm vẫn Future | Web + Platform; OPEN |
| Q-103 | Counter scope/init/reset authority; TTL hay no expiry; eviction/persistence/restore; max/wire encoding; RPO/RTO? | ENT-100, counter API, migration recovery | Web + Platform; OPEN |
| Q-104 | Thiết bị/browser/load và latency/FPS/memory targets; Redis check depth/deadline; shutdown/drain/time limits? | NFRs, ready, topology/resource fit và recovery gates | Web + QA + Platform; OPEN |
| Q-105 | Accessibility/keyboard standard, thiết bị; optional 2D fallback hay text dashboard? | NFR-106 và scene acceptance | Web owner + QA; OPEN |
| Q-106 | Metric names/units/labels, counter inclusion, scrape access và consumer integration? | FR-104, API metrics, Architecture/Migration | Web + QA/Observability + Platform; OPEN |
| Q-107 | Simulator scenario/cadence, terminal/reset control, string/run/task/buffer limits? | Conditional demo/Data/AC-112/FR-111 | Web owner; OPEN |
| Q-108 | Next/Express deployables, routing/ports/probe ownership? Migration business case, source/ref, target version, window/rollback authority? | Architecture/packaging; MIG-100 và cutover gates | Web + Platform + người dùng; OPEN |

## 7. Cách cập nhật và sử dụng

Web/QA có thể dùng BRD/FRD để phân việc, API để review consumers và Architecture/Data để thiết kế implementation. Các phần BLOCKED phải được chốt tại đúng owner trước khi triển khai phần phụ thuộc; không cần chờ đóng toàn bộ questions để làm việc độc lập khác.

Khi một Q được giải quyết: ghi decision/source/date, sửa định nghĩa ở tài liệu sở hữu nội dung, cập nhật upstream versions và trace downstream, rồi chạy lại checks bị ảnh hưởng. Giữ snapshot Validation nguyên trạng. Không lấy PASS của lần thử nghiệm trước làm kết quả kiểm tra bản Official hoặc runtime mới.

Tình trạng cần lưu ý: counter wire contract/lifecycle còn mở; access policy chưa duyệt; extension chưa selected; migration source/parity/cutover vẫn BLOCKED. Chúng là prerequisites được quản lý trong bộ Official, không bị xóa khi chuyển đổi hình thức tài liệu.

## 8. Kiểm tra bản Official ngày 2026-11-06

Đã thực thi kiểm định riêng cho bản Official, không dùng kết quả của practical test để thay cho lượt kiểm tra này: **7 nhóm checks PASS, 0 FAIL**. Lượt đầu phát hiện Architecture chưa ghi Document ID nguồn ngay trong metadata; đã bổ sung `PT-ARCH 0.1.0` và kiểm tra lại. Không thay đổi yêu cầu hoặc contract để vượt qua checks.

| Nhóm kiểm tra | Kết quả / phạm vi |
|---|---|
| Bảo toàn workspace | 79 file tracked trước chuyển đổi giữ nguyên SHA-256; chỉ thêm 9 file tài liệu: sáu Official và ba README. Nhánh/HEAD không đổi; toàn bộ Validation giữ nguyên |
| OpenAPI specification | `openapi-spec-validator 0.9.0` kiểm định OpenAPI3.1.1 thành công |
| Wire contract và version | Paths, methods, operationIds, FR links, status/headers, metric catalog, components/schemas và examples bằng bản nguồn; chỉ dịch ba summaries. API version vẫn0.1.0, document version1.0.0 |
| References và examples | 6 local refs resolve; 6 response examples qua JSON Schema Draft202012 và format checks với `jsonschema 4.26.0` |
| Trace và logical data | Giữ 9 BR, 12 FR-parent pairs, 9 RULE, 15 AC, 7 NFR, 4 ENT, field dictionary, enums và ba operation mappings; counter gap/non-HTTP dispositions rõ |
| Controls và gates | NFR realization rows, architecture ADRs, migration phases, 9 OPEN questions, key proposal và TTL unknown được giữ; migration readiness vẫn BLOCKED |
| Nội dung và navigation | Local links, metadata/source lineage, Markdown table columns và code fences hợp lệ; 8 Mermaid blocks được kiểm tra văn bản, chưa render |

Giới hạn: cùng agent biên tập và review, chưa là đánh giá ngữ nghĩa độc lập; chưa chạy app/Redis/load/live cluster/migration parity. Example `text/plain` hợp lệ theo schema không thay thế Prometheus exposition parser hoặc scrape integration test. Không dùng các PASS tài liệu này để đóng Q hoặc tuyên bố nghiệm thu runtime.
