# FRD — Chức năng và acceptance theo V1/V2

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-FRD | 1.1.0 | review | 2026-11-07 | Web Dev; QA review | E-109 và [registry](README.md) | WEB-BRD 1.1.0; WEB-FRD 1.0.0 |

Change log 1.1.0: giữ 12 FR, 9 RULE, 15 AC, 7 NFR; thêm Delivery Stage, page-view retry/TTL, readiness 2 s/probe 3 s/startup≈50 s, metrics và fallback đã chốt. Contract details là thiết kế dẫn xuất; không tuyên bố đã implement/test. Nguồn [PT-FRD0.1.0](../validation/practical-test/02-FRD.md) giữ nguyên.

## 1. Release và actors

V1 Integration Release thực hiện đầy đủ FR-100..FR-105 và mức cơ bản FR-106..FR-110. V2 Full AI Office hoàn thiện FR-106..FR-111. Viewer chỉ truy cập website/Office; operational endpoints/tools chỉ infra hoặc authorized admin. Stakeholder không tự có Admin; không login V1, không task editor/AI executor.

### Workflow V1

1. Mỗi lần document load/F5 tạo requestId mới; hydration/re-render/retry cùng document phải dùng lại ID đó.
2. POST register page view; cùng requestId được xử lý một lần trong cửa sổ dedup 600 s. GET đọc tổng không ghi visit. Probe/metrics/assets/Reset Demo không ghi visit.
3. Hiển thị total nếu known; Redis lỗi hiện unavailable, không tạo 0 giả hoặc reset total.
4. Bootstrap 3 Agents Idle; simulator/reducer tối thiểu phát event cách 5–8 s, cập nhật UI/scene chung snapshot. Viewer có Reset Demo; reload cũng tạo run mới.
5. WebGL/3D lỗi thì dùng Text Dashboard; keyboard thao tác được, không chỉ màu/animation.

### Workflow V2

Giữ V1 và hoàn thiện completed/failed/recovery scenarios, transitions/validation/animations và FR-111 Recent Activity 20 events. Tối đa 1 running task/Agent và 30 tasks/run; khi đạt 30 không tạo task 31, cho task đang chạy kết thúc rồi chờ Reset Demo. Không tự reset total hoặc tự khởi tạo run vô hạn để né giới hạn.

## 2. Functional requirements và Delivery Stage

| FR | Parent BR | V1 — Integration Release | V2 — Full AI Office | Interface / links / implementation |
|---|---|---|---|---|
| FR-100 | BR-100 | Render website/Office cơ bản, counter unavailable khi lỗi; Text Dashboard/keyboard | Giữ V1, hiển thị Office đầy đủ | HTML/UI; RULE-100; AC-100; starter code-observed |
| FR-101 | BR-101 | F5 là page view mới; register requestId atomic/dedup 600 s; read total; total no TTL/no auto-reset; xử lý exceptions | Giữ đúng semantics V1 | getVisitorCount/registerPageView; RULE-100/101; AC-101/102; chưa code |
| FR-102 | BR-102 | GET /healthz:200 ok, uptime>=0, UTC; độc lập Redis, không ghi visit | Giữ V1 | getLiveness; RULE-102; AC-103; current handler observed |
| FR-103 | BR-102 | Init/config xong, Redis check thành công trong 2 s và chưa drain→200; lỗi/timeout→503; probe timeout 3 s, startup budget≈50 s | Giữ V1 | getReadiness; RULE-102; AC-104/105; current ready vẫn luôn 200 |
| FR-104 | BR-103 | Scrape 4 metrics V1, labels bounded; Redis down không làm mất process/HTTP export; redis_up=0 khi check thất bại | Giữ V1; không thêm agent/task labels | getApplicationMetrics; RULE-103; AC-106; chưa route |
| FR-105 | BR-104 | Next Fullstack container/config, non-root, operational access, probe integration; persistence/backup/recovery plan trước acceptance | Giữ integration khi nâng V2 | Internal/package; RULE-102; AC-107; configured only |
| FR-106 | BR-105 | Dashboard 3 Agents:ID/name, Idle/Working, current task; empty/unavailable text rõ | Đủ idle/working/completed/failed và task results | Browser UI, HTTP N/A; RULE-104/105; AC-108/114; planned |
| FR-107 | BR-105 | Một browser simulator writer, events 5–8 s, Reset Demo/reload new run; tối đa 30 tasks/run; cleanup timers | Success/Failure/Recovery scenarios đầy đủ | Browser internal, HTTP N/A; RULE-104..106; AC-109/113; planned |
| FR-108 | BR-105 | Reducer tối thiểu giữ agent-task nhất quán, 1 running/Agent; basic ID/run/seq/guard checks không được bỏ | Full invalid/ref/gap/duplicate/terminal validation và recovery scenarios | Internal, HTTP N/A; RULE-104..106; AC-110/113; planned |
| FR-109 | BR-106 | 3 chibi trong dải 2–3; 3D cơ bản; lỗi WebGL→Text Dashboard, không task failure giả | Hoàn thiện scene/scenarios tương thích bốn states | UI, HTTP N/A; RULE-107; AC-111/114; planned |
| FR-110 | BR-106 | Idle→rest, Working→typing và text label; animation không đổi state | Completed→success gesture, Failed→error gesture; recovery theo rules | UI, HTTP N/A; RULE-107; AC-111; planned |
| FR-111 | BR-106 | NOT IN V1; không panel/buffer Recent Activity để nghiệm thu V1 | 20 accepted events gần nhất, seq giảm, timestamp/agent/task, label simulated; transient | UI/internal, HTTP N/A; RULE-106/108; AC-112/113; planned V2 |

Các scope/stage/numeric targets E-109 là accepted. API/storage choices là design dẫn xuất. Không agents CRUD/server simulator/SSE/login hoặc real execution trong V1/V2.

## 3. Rules — canonical behavior owner

| RULE | Quy tắc | Stage / authority |
|---|---|---|
| RULE-100 | Một F5/document load là page view mới. requestId mới cho load mới; cùng document retry dùng cùng ID. Không đếm probes, metrics, static assets, GET đọc total hoặc Reset Demo | V1, V2; E-109/Q-101 |
| RULE-101 | Một logical registration được increment và ghi dedup cùng atomic boundary. Dedup 600 s từ success đầu, không refresh TTL khi retry; total no TTL/no auto-reset. Confirmed new IDs tăng đúng 1; cùng ID replay không tăng. Timeout có thể outcome unknown: retry chỉ cùng ID trong cửa sổ, không sinh ID thay thế để che lỗi | V1, V2; behavior accepted; atomic/wire design ở API/Data |
| RULE-102 | Liveness chỉ process. Ready kiểm init/config, Redis check timeout 2 s và không drain; fail 503. Readiness probe timeout 3 s, startupProbe budget≈50 s. Redis failure không làm liveness fail hoặc tự reset counter | V1, V2; E-109/Q-104 |
| RULE-103 | 4 metric families tại API; CPU/RAM/K8s dùng infrastructure metrics. Labels không raw URL/query, requestId, agent/taskID, user/secret hoặc task content; registry không cần đọc business counter để export | V1, V2; E-109/Q-106 |
| RULE-104 | Agent enum giữ idle/working/completed/failed; Task enum running/completed/failed. V1 UI dùng idle/working; completed/failed Agent scenarios chỉ V2 | V1 subset, V2 full; E-109 |
| RULE-105 | Tối đa 1 running task/Agent; assignment tạo task ID mới; result phải current task. V2 terminal Agent giữ ref đến agent.reset→idle. Reset Demo global bỏ run, không là agent.reset và không là counter reset | V1 basic, V2 full; V1 finish detail bên dưới |
| RULE-106 | Một writer/browser, runId/seq; chỉ next seq apply, duplicate no-op, gap/invalid ref reject+diagnostic. Events 5–8 s khi có transition; 30 tasks/run; không await giữa validate/commit; cleanup timers. New run clear trước bootstrap | V1 basic, V2 full validation; values accepted |
| RULE-107 | UI/scene đọc snapshot; animation không trigger task completion. Text Dashboard fallback và keyboard bắt buộc, không chỉ màu | V1, V2; E-109/Q-105 |
| RULE-108 | Recent Activity chỉ V2, 20 accepted events, seq giảm; bỏ event cũ không xóa task; transient, reset/reload mất theo run; không retained history | V2; E-109/Q-107 |

### V1 task completion — design detail cần phân biệt scope

Để giữ event cadence khi UI chỉ Idle/Working, **đề xuất triển khai**: basic task.completed kết thúc task nội bộ và đưa Agent thẳng Working→Idle, ref→null; không có Success pose/Agent completed hoặc failure/recovery scenario trong V1. Đây là completion tối thiểu của reducer, không full Success feature. Quy tắc này còn cần Web owner xác nhận Q-107; không gắn accepted chỉ vì các numeric targets đã chốt. Nếu chọn giữ Working đến Reset Demo, phải ghi giới hạn scheduler khi cả 3 Agents bận; không tự tạo task chồng. V2 giữ terminal behavior đã có ở nguồn.

| Agent current | Trigger / guard | Next | Task / ref / giới hạn | Stage |
|---|---|---|---|---|
| idle | task.started; ID mới, còn quota, Agent rảnh | working | Tạo running task + ref atomic | V1, V2 |
| working | task.completed đúng current | idle | Task completed nội bộ, ref null; không Success pose | V1 design proposal, Q-107 |
| working | task.completed đúng current | completed | Task completed, giữ ref | V2 |
| working | task.failed đúng current | failed | Task failed, giữ ref | V2 |
| completed/failed | agent.reset | idle | Ref null, task terminal giữ tới new run | V2 recovery |
| busy/terminal | task.started không đúng guard | Forbidden | Không overwrite running task; V2 terminal cần reset | Stage-specific guards |
| bất kỳ | Reset Demo hoặc reload | new run / idle | Clear toàn run, bootstrap 3 Agents; không total reset | V1, V2 |
| taskCount=30 | Thử assignment mới | Forbidden | Không task 31; finish in-flight rồi chờ Reset | V1, V2 |

Không tự thêm auto-retry failed task hoặc tự reset total/run sau X giây. Events là mô phỏng; task completion không là command/model execution.

## 4. Operational behavior và availability

| Trường hợp | Liveness | Readiness | Counter / Office |
|---|---|---|---|
| Process đáp ứng, Redis tốt, init xong | 200 | 200 ready | Counter có thể phục vụ; Office theo stage |
| Redis lỗi/timeout 2 s | 200 nếu process đáp ứng | 503DEPENDENCY_UNAVAILABLE | Counter 503/unavailable; Pod có thể bị rút serving endpoints, viewer mới không tải Office |
| Init/config chưa đủ hoặc drain | 200 nếu process đáp ứng | 503 NOT_READY | Không nhận traffic qua ready endpoints; không reset total |
| Process không đáp ứng | Caller timeout | Caller timeout | Không hứa JSON response |

Browser đã tải Office có thể tiếp tục local simulator/Text Dashboard khi counter lỗi; reload/new viewer cần server và có thể thất bại nếu mọi Next pod NotReady. Readiness không tự restart pod; startup/liveness failure policy riêng. Không nới `/ready` để giả availability độc lập Redis. Metrics có thể vẫn export trong process nhưng scrape qua Service cũng có thể mất khi endpoints bị rút; Platform cần đường scrape trực tiếp Pod/monitoring phù hợp.

## 5. Acceptance criteria theo stage

Mọi hàng là **expected behavior, not executed result**. Giữ mã AC cũ và tách stage trong cùng hàng.

| AC | FR / RULE | Delivery Stage | Given / When | Then / evidence cần |
|---|---|---|---|---|
| AC-100 | FR-100 | V1, V2 | Mở page; thử counter lỗi | UI/text status trung thực, counter unavailable không 0 giả; không claim ready thay UI-render test |
| AC-101 | FR-101, RULE-100 | V1, V2 | F5 hai lần; retry cùng request trong 600 s; gửi GET/probe/scrape/assets/Reset Demo | Hai load IDs khác nhau tăng 2; retries không tăng; excluded requests không tăng; UUID lifecycle kể cả double hydration |
| AC-102 | FR-101, RULE-101 | V1, V2 | N new IDs với concurrent duplicates; response mất sau commit; key TTL boundary | Total n+N; replay original receipt, same ID không tăng; dedup TTL không refresh; total no expiry; expired/lost dedup ngoài guarantee; exceptions không reset |
| AC-103 | FR-102, RULE-102 | V1, V2 | Process còn đáp ứng, Redis down; GET /healthz | 200 ok, uptime>=0, UTC; không Redis check/visit |
| AC-104 | FR-103, RULE-102 | V1, V2 | Init/config xong, check Redis thành công ≤2 s; probe timeout 3 s | 200 ready; không mutate business data; QA đo end-to-end response đủ margin trước 3 s |
| AC-105 | FR-103, RULE-102 | V1, V2 | Redis lỗi/timeout hoặc drain rồi phục hồi | 503 đúng error code; Redis wait không vượt 2 s; next valid check 200; không restart chỉ do Redis; kiểm tra endpoints/routing tác động Office, new load/reload |
| AC-106 | FR-104, RULE-103 | V1, V2 | QA tạo traffic, latency và Redis fail/restore; authorized scrape | Parser đọc 4 families đúng types/units; bounded labels; redis_up chuyển 0/1; duration observations hợp request; không tăng visit; deny viewer operational access |
| AC-107 | FR-105 | V1, V2 | Chạy image/config/probe target trong test riêng; slowstart/missing config | Non-root; startup budget≈50 s bằng startupProbe; ready timeout 3 s; missing config notready; backup/restore/access plan xác nhận; không suy target đã có trong manifest |
| AC-108 | FR-106 | V1 basic, V2 full | Reset/reload bootstrap 3 Agents rồi valid start | Dashboard đúng ID/name/state/task và Simulated; V1 Idle/Working, V2 four states |
| AC-109 | FR-107 | V1 basic, V2 full | Demo chạy đủ events rồi Reset/unmount | Events cách 5–8 s khi có transition; ≤1 running/Agent; ≤30 tasks/run; new run/counter không lẫn; unmount stop; V2 thêm Success/Failure/Recovery; V1 finish proposal chờ Q-107 |
| AC-110 | FR-108, RULE-105 | V1 basic, V2 full | Valid result; thử assign vào busy Agent và cross run/ref sai | Atomic agent+task; basic guards V1; V2 terminal states/ref reset/full guards; không task 31 |
| AC-111 | FR-109/110, RULE-107 | V1 basic, V2 full | Render 3 chibi từ snapshot | V1 rest/typing; V2 success/error/recovery poses; label text, animation không đổi state |
| AC-112 | FR-111, RULE-108 | V2 only | 21 accepted events rồi Reset/reload | 20 mới nhất seq giảm, bỏ cũ nhất; new run empty; V1 không yêu cầu panel/buffer Recent |
| AC-113 | FR-107/108/111, RULE-106 | V1 basic, V2 full | Re-deliver seq k, gap k+2, invalid refs | V1 không corrupt snapshot hoặc double assign; V2 full matrix/diagnostics, no invalid activity; FR-111 part chỉ V2 |
| AC-114 | FR-100/106/109 | V1, V2 | WebGL/3D fail hoặc empty snapshot; dùng keyboard | Text Dashboard fallback đúng state, empty text; Reset Demo thao tác được; không chỉ màu/animation; không tự nhận WCAG certified |

## 6. NFRs và verification

| NFR | Parent / source | Target / Delivery Stage | Verification / residual |
|---|---|---|---|
| NFR-100 | BR-104, E-104/E-109 | V1, V2: Next Fullstack non-root, UID 10001:10001 configured, runtime config ngoài image | Build/run riêng; không tự sửa Dockerfile |
| NFR-101 | BR-102, E-109 | V1, V2: Redis check 2 s, readiness probe 3 s, startup budget≈50 s | Fault/duration/endpoints tests; Platform xác nhận tuple/depth/drain |
| NFR-102 | BR-105/106, E-109 | V1 basic, V2 full: 3 Agents, 5–8 s events, 30 tasks/run | Browser profile; FPS/memory/device thresholds còn Q-104 |
| NFR-103 | BR-104/105, E-109 | Viewer product; operational/tools infra/admin; không login V1, không real execution/credentials | Proxy/CNI/monitoring grants+deny tests; enforcement Q-102 |
| NFR-104 | BR-101/105, E-109 | Total no TTL, request dedup 600 s, no auto reset; persistence/backup/recovery required; demo transient | Atomicity/restart/restore/TTL tests; RPO/RTO/storage/retention Q-103 |
| NFR-105 | BR-103/104, E-109 | 4 metric families, bounded labels, no CPU/RAM/K8s duplication; graceful drain | Parser/load/scrape/routing checks; buckets/deadlines Q-106/Q-104 |
| NFR-106 | BR-100/106, E-109 | Text Dashboard fallback, keyboard, không màu/animation-only | Manual browser/keyboard review; qualification standard Q-105 |

## 7. Traceability và findings

[BRD](BRD.md) sở hữu BR/stages; [API](api-contract.yaml) map FR-101→getVisitorCount/registerPageView, FR-102/103/104→getLiveness/getReadiness/getApplicationMetrics. FR-100 HTML ngoài JSON, FR-105 packaging, FR-106..111 browser-only (FR-111 V2). [Data](data-contract.md) ENT-100 counter/dedup, ENT-101..103 demo; [Architecture](architecture.md) controls cho đủ NFRs. Quyết định đã giải không còn OPEN toàn bộ; residuals tại[registry](README.md).

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-102 | Trace/stage / major | 12 FRs cùng parents, FR-111 V2, 5 operations hợp FR | Không orphan/không scope creep | Cross check / Web+QA | Document check; runtime pending |
| VAL-103 | Counter / major | Q-101 đã chốt; contract có idempotency window/exception boundary | Không còn visit definition blocker | Implement/fault test / Web+QA | Decisions RESOLVED; atomicity untested |
| VAL-104 | NFR / major | Timing/limits/fallback đã chốt; storage/access/buckets/performance qualification còn TBD | Không coi targets tested | Platform/QA confirm residuals | Partial residual gates; không OPEN ba timing targets |
