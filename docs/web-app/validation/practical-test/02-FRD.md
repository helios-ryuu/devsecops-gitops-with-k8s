# FRD — AI Agent Office Monitor

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| PT-FRD | 0.1.0 | DRAFT | 2026-11-05 | Web Fullstack Dev; reviewer QA | E-100..E-108, [report](evaluation-report.md) | PT-BRD 0.1.0; shared standard 1.0.0 |

Change log 0.1.0: phân rã mandatory và conditional MVP, không đưa optional/future thành active FR. Mọi behavior mới dưới đây là proposed design; nguồn không chứng minh đã chạy.

## Actors, boundary và flows

Người xem mở UI; simulator là actor nội bộ trong trình duyệt nếu được chọn. Probe consumer và metrics scraper là clients kỹ thuật do nhóm quản lý. Không có administrator, đăng nhập, task editor hay AI executor trong release draft. Quyền truy cập deployment chưa chốt Q-102; thiếu auth feature không đồng nghĩa mọi endpoint được duyệt public.

Mandatory flow: mở web → đọc thông tin release/counter → nếu Redis lỗi hiển thị unavailable, không số giả. Counter trigger và đơn vị visit phải chốt Q-101 trước khi triển khai. Operator gọi liveness không phụ thuộc Redis; readiness kiểm tra điều kiện phục vụ; scraper lấy application metrics, không tăng business visits.

Conditional MVP flow: vào demo có nhãn “Simulated” → tạo 2–3 agents idle → simulator gán task rồi phát event hợp lệ → reducer cập nhật agent/task cùng lúc → dashboard, animation và recent panel dùng cùng snapshot. Mở lại trang bắt đầu demo mới theo A-100; không hứa history xuyên phiên, dữ liệu shared hay real execution.

## Functional requirements

Mỗi hàng là một observable behavior. M = Mandatory/requested obligation; P = Proposed MVP Extension/conditional, chưa accepted. Inputs không lấy từ người dùng ngoài simulator; thiếu dữ liệu và concurrency được quy định ở RULEs/ACs bên dưới.

| FR | Parent BR | Actor / trigger / precondition | Inputs và behavior / outputs | Alternative / failure / concurrency | Interface / priority / status | RULE / AC |
|---|---|---|---|---|---|---|
| FR-100 | BR-100 | Viewer mở trang | Render web interface của release đã chọn | Lỗi counter không làm giả total; lỗi assets không được báo app healthy thay cho UI success | UI, HTTP page ngoài OpenAPI JSON; High/M; starter code-observed | RULE-100; AC-100 |
| FR-101 | BR-101 | Viewer; visit trigger TBD Q-101 | Đọc/ghi counter Redis và hiển thị kết quả theo định nghĩa visit được duyệt | Không trả total 0 khi Redis unavailable; đồng thời tăng phải atomic; retry policy TBD | HTTP counter operations BLOCKED Q-101; High/M; planned | RULE-100/101; AC-101/102 |
| FR-102 | BR-102 | Probe GET; process phục vụ được | Trả 200, status ok, uptime giây và timestamp UTC | Redis down vẫn 200 nếu process còn phục vụ; process không đáp ứng do consumer phát hiện timeout | HTTP getLiveness; High/M; code-observed | RULE-102; AC-103 |
| FR-103 | BR-102 | Readiness consumer GET | Candidate: trả 200 status ready khi init hoàn tất và Redis check thành công trong deadline Q-104 | Redis error/timeout/draining → 503 DEPENDENCY_UNAVAILABLE hoặc NOT_READY; không lộ host/secret | HTTP getReadiness; High/M; hiện handler luôn 200, delta proposed | RULE-102; AC-104/105 |
| FR-104 | BR-103 | Scraper GET | Xuất Prometheus-compatible text; proposed metric set tại API | Registry không phục vụ → 503; Redis down không ngăn scrape process/HTTP metrics; scrape không tăng visit | HTTP getApplicationMetrics; High/M; planned | RULE-103; AC-106 |
| FR-105 | BR-104 | Web/Platform bàn giao bản build | Ứng dụng có thể đóng gói container, nhận cấu hình runtime và phục vụ integration contract đã chốt | Thiếu config bắt buộc → not ready; không nhúng credential vào image | Internal/package, HTTP N/A do đây là packaging; High/M; configured, chưa tested | RULE-102; AC-107 |
| FR-106 | BR-105 | Viewer vào conditional demo | Hiển thị agents với ID, name, state và current task; hiển thị task được tạo | Empty list có thông báo; field state lạ không làm crash hoặc ép completed | UI, HTTP N/A theo ADR-101; Medium/P; proposed | RULE-104/105; AC-108/114 |
| FR-107 | BR-105 | Internal simulator; demo active | Tạo event giả lập theo state transitions, không chạy command/model | Một browser có một writer simulator; stop/unmount ngừng timers; không nhập external event chưa validate | Internal, HTTP N/A; Medium/P; proposed | RULE-104..106; AC-109/113 |
| FR-108 | BR-105 | Reducer nhận assignment/result event | Cập nhật agent và task quan hệ nhất quán | Task không tồn tại/agent bận/duplicate hoặc out-of-order → reject/no-op có diagnostic; không tiến state | Internal, HTTP N/A; Medium/P; proposed | RULE-104..106; AC-110/113 |
| FR-109 | BR-106 | Viewer mở office nếu extension selected | Hiển thị office scene với 2–3 nhân vật tương ứng agent IDs | WebGL/init fail → thông báo 3D unavailable; dashboard text vẫn là state source; không cam kết optional 2D renderer | UI, HTTP N/A; Medium/P; proposed | RULE-107; AC-111/114 |
| FR-110 | BR-106 | Agent state thay đổi | Map idle→rest pose, working→typing, completed→success gesture, failed→error gesture và text label | Animation không tự thay business state; unknown state giữ diagnostic; không chỉ dùng màu | UI, HTTP N/A; Medium/P; proposed | RULE-107; AC-111 |
| FR-111 | BR-106 | Event được reducer chấp nhận | Recent activity hiển thị mới nhất trước, timestamp và agent/task liên quan, nhãn simulated | Empty panel rõ ràng; bounded buffer có sức chứa TBD Q-107; không hứa persisted history/filter | UI/internal, HTTP N/A; Medium/P; proposed | RULE-106/108; AC-112/113 |

## Rules và state transitions — canonical behavior owner

| RULE | Rule / source / parent | Status |
|---|---|---|
| RULE-100 | Visit chỉ tính theo định nghĩa Q-101; probe/metrics/static assets không phải business visits. BR-101, proposed interpretation | BLOCKED definition |
| RULE-101 | Mỗi increment được Redis xác nhận có một atomic tăng; lỗi/timeout không được nói chắc chưa tăng. Không promise exactly-once hoặc unique visitor. BR-101 | Proposed; retry gate Q-101 |
| RULE-102 | Liveness chỉ process; readiness gồm init + Redis dependency và chưa drain. BR-102/104 | Proposed delta; không mô tả current readiness như vậy |
| RULE-103 | Metrics không chứa agent ID, task ID, URL tự do, credentials hoặc nội dung task trong labels. BR-103/104 | Proposed bounded vocabulary |
| RULE-104 | Agent state enum duy nhất idle, working, completed, failed. Task status proposed running/completed/failed; không gọi task status là agent state. BR-105 | Agent enum user-provided, task rules proposed |
| RULE-105 | Một agent có tối đa một running task; assignment tạo task ID mới; chỉ running task hiện tại được complete/fail. Terminal agent giữ task ref tới reset; reset bỏ ref. BR-105 | Proposed |
| RULE-106 | Một simulator writer/browser, event seq tăng trong demoRunId; chỉ seq kế tiếp được apply, duplicate là no-op; gap/invalid ref reject và báo diagnostic, không thêm activity. Reset demo tạo run mới và state rỗng trước bootstrap. BR-105/106 | Proposed |
| RULE-107 | UI đọc snapshot; animation là derived presentation, không trigger task completion. BR-106 | Proposed |
| RULE-108 | Recent buffer là transient trong browser, không phải event history; capacity Q-107; khởi động lại mất buffer có chủ ý. BR-106 | Proposed |

| Agent current | Trigger / guard | Next | Task / forbidden / race | RULE |
|---|---|---|---|---|
| idle | task.started, task ID mới, agent không có task | working | Tạo running task và ref atomic trong reducer | RULE-105/106 |
| working | task.completed, đúng current task | completed | Task→completed; giữ ref | RULE-105 |
| working | task.failed, đúng current task | failed | Task→failed; giữ ref | RULE-105 |
| completed hoặc failed | agent.reset | idle | Ref→null, task terminal còn trong demo snapshot tới reset run | RULE-105 |
| idle | complete/fail | Forbidden | Không tạo task/state/event mới | RULE-105/106 |
| working | task.started khác hoặc reset | Forbidden | Không overwrite task đang chạy | RULE-105/106 |
| terminal | complete/fail/start trước reset | Forbidden | Duplicate seq no-op; event mới sai transition reject | RULE-105/106 |

Không có auto-retry task hay tự reset sau X giây được chốt. Simulator scenario và cadence TBD Q-107, không biến failed thành working ngầm.

## Acceptance criteria — Given / When / Then

| AC | FR / RULE | Given | When | Then / case |
|---|---|---|---|---|
| AC-100 | FR-100 | Release mandatory được build | Mở web | Nội dung web render; lỗi counter hiện unavailable thay vì dữ liệu giả / success+failure |
| AC-101 | FR-101, RULE-100 | Quy tắc visit đã duyệt Q-101 và Redis hoạt động | Phát sinh visit hợp lệ và probe/scrape | Chỉ visit hợp lệ thay đổi total đúng quy tắc / BLOCKED expected delta đến khi Q-101 đóng |
| AC-102 | FR-101, RULE-101 | Counter n, N increments đã được xác nhận, không reset/eviction | Hai clients ghi đồng thời | Total n+N; Redis timeout phải báo unavailable/ambiguous, không retry mù / concurrency+failure, retry gate mở |
| AC-103 | FR-102, RULE-102 | HTTP process chạy nhưng Redis unreachable | GET /healthz | 200 status ok, uptime >=0, timestamp UTC; không tăng counter / alternate |
| AC-104 | FR-103, RULE-102 | Init xong, Redis check thành công | GET /ready | 200 status ready và timestamp; không mutate business data / success |
| AC-105 | FR-103, RULE-102 | Redis timeout/error hoặc đang drain | GET /ready, sau đó Redis phục hồi và hết drain | 503 envelope trước; lần check đạt trả 200; không cần restart chỉ vì Redis / failure+recovery; deadline TBD Q-104 |
| AC-106 | FR-104, RULE-103 | Registry ready; traffic thử được QA tạo | Scrape /metrics | Parser Prometheus đọc được metrics, có process/HTTP series đã chốt, labels không nhạy cảm; Redis down vẫn scrape / success+boundary; series approval Q-106 |
| AC-107 | FR-105 | Image build/config integration được chọn | Nhóm chạy container local/staging, bỏ config Redis cần thiết | Normal: UI/probes accessible; missing config: not ready; process không cần root / integration, chưa thực thi |
| AC-108 | FR-106 | Extension được chọn; demo mới | Bootstrap 2–3 agents idle rồi một task.started hợp lệ | Dashboard có ID/name/state/task khớp snapshot và nhãn simulated / success |
| AC-109 | FR-107 | Demo active | Chạy scenario start→result→reset rồi unmount | Chỉ event mô phỏng; transitions hợp lệ; sau unmount không tạo event mới / success+cleanup |
| AC-110 | FR-108, RULE-105 | Agent working trên task A | Result task A; thử assign task B khi A còn running ở run khác | Case hợp lệ cập nhật cả task và agent; case busy reject không đổi snapshot / success+guard |
| AC-111 | FR-109/110, RULE-107 | Cùng agent lần lượt đi qua bốn states | Render từng snapshot | Đúng 2–3 chibi, animation+text label tương ứng, animation không đổi state / boundary |
| AC-112 | FR-111, RULE-108 | Buffer capacity đã chốt Q-107 | Nhận C+1 events hợp lệ rồi reload | Hiện C mới nhất theo seq giảm, cũ nhất bị loại; reload bắt đầu demo mới / conditional boundary |
| AC-113 | FR-107/108/111, RULE-106 | Event seq k đã apply | Nhận k lại hoặc k+2/unknown task | Duplicate no-op; gap/ref sai diagnostic, không thêm activity/state sai / failure |
| AC-114 | FR-106/109 | Snapshot rỗng hoặc WebGL không init | Mở view | Empty text hoặc 3D unavailable; dashboard đọc state text được, không giả lập successful renderer / alternative |

## Non-functional requirements

| NFR | BR / source | Attribute / metric / target | Conditions / verification | Commitment / gap |
|---|---|---|---|---|
| NFR-100 | BR-104, E-100/E-104 | Container chạy non-root; runtime config tách image | Inspect/build/run image; UID configured 10001:10001 | Requested integration; test chưa chạy |
| NFR-101 | BR-102, E-100 | Readiness response deadline và recovery observation TBD Q-104 | Redis fail/restore; QA đo duration; phân biệt liveness | Proposed semantics, target BLOCKED |
| NFR-102 | BR-105/106, E-100 | 2–3 characters; FPS, memory, browser/GPU matrix TBD Q-104 | Browser profile với demo scene và tab lifecycle | Conditional; không lấy FPS reference làm SLA |
| NFR-103 | BR-104/105, E-100 | Không có real execution/credential access trong demo; exposure policy TBD Q-102 | Dependency/code/security review; inspect logs và network | Scope invariant; deployment access BLOCKED |
| NFR-104 | BR-101/105, E-100 | RPO/RTO, persistence/eviction và counter max TBD Q-103 | Redis loss/restart/concurrency characterization | Không promise durability |
| NFR-105 | BR-103/104, E-101 | Scrape-compatible metrics, bounded labels, graceful shutdown/drain deadline TBD Q-106/Q-104 | Parser, traffic, termination check cùng Platform | Metrics required; limits pending |
| NFR-106 | BR-100/106, E-100 | Không dùng màu/animation làm kênh state duy nhất; keyboard/accessibility standard TBD Q-105 | Inspect text labels, keyboard/manual review | Proposed; không tuyên bố WCAG compliance |

## Traceability và impacts

BR mapping đầy đủ tại [BRD](01-BRD.md). HTTP coverage: FR-102→getLiveness, FR-103→getReadiness, FR-104→getApplicationMetrics; FR-101 là gap công khai, không dùng GET để tăng counter. FR-100 là HTML UI; FR-105 packaging; FR-106..111 UI/internal theo ADR-101, nên HTTP N/A có lý do. Data ENT-100 phục vụ counter; ENT-101..103 phục vụ conditional demo. Mỗi NFR có control/gap tại [Architecture](04-architecture.md).

Facts: E-103 probes code-observed, không có simulator implemented. A-100 và task/event semantics là proposals từ yêu cầu người dùng, không lấy My Office làm source business. Q-100..Q-108 canonical tại report. Nếu simulator phải shared backend, phải revise FR/API/Data/Architecture trước implementation; không chỉ gắn SSE vào draft này.

## Validation

Checked behavior/BR parents/rules/ACs/NFR mapping tại 0.1.0; runtime ACs chưa thực thi. Không coi danh sách AC là kết quả test.

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|
| VAL-102 | Traceability / major | FR-100..111 đều có BR hợp scope; API coverage chỉ ba operational FR | Không có orphan FR | Giữ explicit gap FR-101 / Web owner | PASS links; gap BLOCKED |
| VAL-103 | Behavior / blocker | FR-101/AC-101 cần visit semantics; Q-101 chưa trả lời | Chưa thể nghiệm thu counter | Chốt trigger/retry / Web owner | BLOCKED |
| VAL-104 | NFR / major | NFR-101/102/104/105 thresholds TBD có owner | Không chứng nhận capacity/recovery | Q-103/104/106 / Web+Platform+QA | BLOCKED targets |
