# Data Contract — application state

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| PT-DATA | 0.1.0 | DRAFT | 2026-11-05 | Web Fullstack Dev; recovery policy phối hợp Platform | E-100/E-103/E-104; reference không quyết định entity | PT-FRD/PT-API/PT-ARCH 0.1.0; shared standard 1.0.0 |

Change log 0.1.0: logical Agent/Task/Event cho conditional browser simulator; Redis chỉ selected cho visitor counter. Không có data implementation đã kiểm chứng trong source.

## Entities, identity và relationships

| ENT | Grain / identity / source | Source of truth / writer / reader | Relationships / deletion |
|---|---|---|---|
| ENT-100 VisitorCounter | Một total cho phạm vi site/environment TBD Q-101; BR-101/FR-101 | Redis selected theo E-100; counter use case writer, UI reader qua API TBD | Không lưu IP/cookie/user; reset authority Q-103 |
| ENT-101 Agent | Một synthetic worker trong demoRunId, ID string; FR-106..110 | Browser snapshot proposed ADR-101; reducer là writer duy nhất, UI/Scene read | currentTaskId null khi idle; ref task hiện tại khi working/terminal; xóa cùng run |
| ENT-102 Task | Một lần giao việc mô phỏng, task ID unique trong run; FR-108 | Browser snapshot, reducer writer | Belongs to đúng agent; running→completed/failed; không delete task còn được ref; clear toàn bộ khi new run |
| ENT-103 SimEvent | Một thay đổi được simulator đề nghị; identity (demoRunId,seq); FR-107/108/111 | Simulator tạo; reducer validate; recent buffer chỉ events accepted | Ref đúng agent/task cùng run; duplicate không tạo thêm record; buffer removal không delete task |

Agent không phải Claude session/process, Task không phải command/job thực thi, Event không phải hook. Không dùng directory, PID, API key, prompt transcript hoặc provider account. Tên agents/task labels là synthetic demo content.

## Field dictionary — proposed domain schema v1

Browser object types dưới đây là logical/internal, không phải public API schemas. Q-100 chưa chọn extension; enums/rules canonical tại FRD RULE-104..108. Không tồn tại agents API để giả định wire mapping đã agreed.

| Field | Meaning / encoding | Required / nullable / default | Invariant / lifecycle |
|---|---|---|---|
| VisitorCounter.total | Redis integer encoded decimal string; logical nonnegative count | Required nếu known; không dùng null/0 thay unavailable | Upper bound và JSON encoding TBD Q-103; chưa có wire schema |
| Agent.id | Opaque nonempty string unique/run | Required, non-null; simulator tạo | Không derive từ real username/path; escaping Redis N/A |
| Agent.name | Synthetic display name, nonempty string | Required/non-null | Max length TBD Q-107; render escaped text |
| Agent.state | idle/working/completed/failed | Required/non-null, bootstrap idle | Theo transition table FRD |
| Agent.currentTaskId | Task ID string hoặc null | Required, nullable, bootstrap null | working/terminal ref task hợp agent; idle null |
| Task.id / agentId | Nonempty string identity/ref | Required/non-null | Unique/run; FK logical đến Agent.id |
| Task.label | Synthetic task description, nonempty string | Required/non-null | Không HTML/command; length limit Q-107 |
| Task.status | running/completed/failed | Required/non-null, created running | Terminal matches result event |
| SimEvent.demoRunId | Opaque nonempty string identity scope | Required/non-null | New run tạo ID mới; không merge events giữa runs |
| SimEvent.seq | Positive integer trong JS safe integer range | Required/non-null, bắt đầu 1 | Tăng đúng 1 cho mỗi accepted event; đạt MAX_SAFE_INTEGER thì cần new run, không wrap |
| SimEvent.type | task.started/task.completed/task.failed/agent.reset | Required/non-null | Phân biệt task result với agent reset |
| SimEvent.agentId | Nonempty string | Required/non-null | Agent đã bootstrap cùng run |
| SimEvent.taskId | Nonempty string hoặc null | Required/nullable | task.* bắt buộc string; agent.reset null; result phải current task |
| SimEvent.occurredAt | UTC RFC3339 string với Z | Required/non-null | Browser clock, không dùng để sắp event; seq canonical order |
| SimEvent.taskLabel | Label cho task mới | Required/non-null chỉ task.started; absent ở type khác | Input tạo Task.label; không nullable placeholder |
| RecentActivity | Derived projection của accepted SimEvents | Có thể empty array | Seq giảm dần; capacity TBD Q-107; không persistent |

Bootstrap agents là init snapshot, không bắt buộc phát event bootstrap ngoài enum đã nêu. Snapshot chứa runId, lastSeq, agents, tasks và recent accepted events; schema version v1 là metadata logical, không tự thêm field vào wire API.

## API mapping — canonical wire definitions tại OpenAPI 0.1.0

| operationId / schema pointer | API field | Storage / derivation | Required/null/time / consistency |
|---|---|---|---|
| getLiveness / #/components/schemas/Liveness | status | Constant ok khi handler trả lời | Required/non-null, không Redis |
| getLiveness / Liveness | uptime | Process monotonic lifetime seconds | Required number >=0, fractional allowed; transient |
| getLiveness / Liveness | timestamp | Response generation clock | Required UTC string, UtcTimestamp schema; transient |
| getReadiness / #/components/schemas/Readiness | status, timestamp | Init/check/drain logic + response clock | Required/non-null; dependency check không write business key |
| getReadiness / #/components/schemas/Error | error.code/message | Dependency/init/drain outcome | Required/non-null; no host, credential, stack trace |
| getApplicationMetrics / text/plain | Exposition series | Registry per process; uptime và completed HTTP hooks | String, not JSON business data; restart reset process counters |
| getApplicationMetrics / Error | error.code/message | METRICS_UNAVAILABLE | No Redis read required |
| FR-101 / route and schema TBD | Counter total | ENT-100 | BLOCKED Q-101/Q-103; chưa chọn number vs decimal string wire |
| FR-106..111 / HTTP N/A | Agent/Task/Event | ENT-101..103 | Internal browser objects; không dựng API schemas vô căn cứ |

Error enum dùng chung nhưng từng operation chỉ được trả applicable code mô tả ở API. Unknown response fields allowed; required fields không null; domain-only nullable task refs không làm thay schema probe.

## Access patterns và Redis mapping

| Pattern / FR | Read/write / cardinality | Atomic boundary / retry |
|---|---|---|
| Visit registration FR-101 | Increment total; trigger, identity và dedupe TBD | Redis INCR candidate atomic một key; response timeout sau write ambiguous; không blind retry |
| Counter display FR-101 | Read one total | Missing key không đủ để phân biệt first use với data loss; policy Q-103 |
| Readiness FR-103 | Dependency check | Proposed PING không tạo/reset counter; timeout Q-104 |
| Simulator FR-107/108 | One event, one reducer transaction trên browser snapshot | Validate rồi replace snapshot gồm agent+task+buffer+lastSeq; views chỉ đọc snapshot đã commit |
| Activity FR-111 | Latest C accepted events/run | Bounded in-memory buffer; C TBD, không pagination/filter |

Redis là selected cho counter; key dưới đây **proposed**, không key đã implemented. Agent state store Redis **chưa selected** theo ADR-101; không tạo key agents/tasks/events cho một nhu cầu chưa có.

| Key pattern | Type / role | Readers / writers | TTL / start / reset | Missing / expired / recovery | Concurrency |
|---|---|---|---|---|---|
| `nt548:<env>:web:v1:visitor:total` (proposed) | Redis string integer, authoritative total trong giới hạn loss policy được chốt | Counter use case write; API adapter read | **TBD Q-103**; không phải no-expiry. Nếu duyệt no-expiry sẽ ghi explicit null/no expiry, không EXPIRE; hiện chưa chọn TTL | Missing→unavailable/needs initialization theo policy TBD; không tự 0. Sau approved first-use init mới INCR-create; restore/reset authority TBD | Single-key INCR linearizable trên Redis primary cho writes được xác nhận; không read-modify-write trong app |

`<env>` phải đến từ allowlist config (ví dụ dev/staging/prod chỉ là examples), không nhận raw URL/user input; separator `:` không được xuất hiện trong env token. Key không chứa identity cá nhân. Redis Cluster không selected; single-key operation không cần multi-key slot assumptions. Nếu chọn multi-key idempotency hoặc shared state, phải thiết kế hash slots/atomic boundary sau.

## Lifecycle, failure và recovery

ENT-100: create/init authorization, persistence, eviction, memory policy, backup/restore cadence, retention và max count đều TBD Q-103. Manifest Redis được đọc không có volume/PVC hoặc persistence command; không thể promise giữ total qua pod replacement. Không suy default Redis image configuration thành durability guarantee. Đếm đúng khi concurrency không đồng nghĩa không mất dữ liệu khi crash. Redis replication/restore lag không được giả định bằng 0.

Nếu INCR succeeded nhưng response mất, client không biết kết quả. Policy retry/dedupe phải chốt Q-101 trước contract. Nếu triển khai counter bằng explicit registration mutation, cần request identity/idempotency decision; chưa tạo duplicate store/TTL ở đây. Readiness failed không reset count. UI unavailable khác total=0; không che dependency failure bằng cache bịa.

ENT-101..103: bootstrap 2–3 agents; accepted events update snapshot atomic theo synchronous reducer, không await giữa validate/commit. Một active engine/mount, cleanup timers khi unmount; React remount cần lifecycle guard, không assume reference start-once an toàn. Duplicate seq<=lastSeq no-op; seq>lastSeq+1 hoặc invalid ref reject + diagnostic; new run clear trước bootstrap. Event timestamp chỉ display; seq quyết định order. Terminal task còn trong tasks map tới new run; task count/run limit TBD Q-107 để tránh memory growth ngoài recent buffer.

Replay/SSE retention N/A vì Optional deferred. Recent buffer không phải retained event log; Pub/Sub không được thêm để hứa replay. Nếu cần history, phải chốt store/retention/access/cursor/gap response rồi revise FRD/API/Architecture/Data.

## Classification, evolution và migration

| Group | Classification / access | Retention / deletion authority | Evolution / old-new compatibility |
|---|---|---|---|
| Visitor total | Aggregate, không thu personal identifiers trong proposal | TTL/reset/restore Q-103 Web+Platform | Preserve key/type/encoding/TTL khi backend thay thế; không tự đổi prefix v1→v2 |
| Synthetic domain | Demo-only, browser-local; không credentials | Clear run/reload; lifecycle limits Q-107 | Internal schema v1; adapter không lấy My Office sess/ts(ms) làm wire chuẩn |
| Operational responses/metrics | Operational information, exposure Q-102 | Metrics history do external scraper owner; không lấy monitoring retention làm app history | API status/type/time phải giữ qua Express/Laravel; process counters reset semantics giữ rõ |

Không có real prompts, host paths, PID hoặc tokens nên không cần thiết kế kho transcript. Nếu đổi sang real sessions, phải có business approval/security/data minimization riêng; không mở rộng fields hiện tại.

## Evidence, decisions, questions và validation

Facts E-103/E-104 chứng minh thiếu client/key implementation và chỉ có config. A-100/ADR-101 là proposed browser-state choice; logical keys/data không được ghi là implemented. Q-101/103/107 canonical ở report. Schema mapping đã so với API 0.1.0, enum/state với FRD 0.1.0 và Redis role với Architecture 0.1.0; không chạy persistence/concurrency tests.

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|
| VAL-107 | Wire/domain mapping / major | API probe fields mapped đầy đủ; ENT-101..103 HTTP N/A nhất quán ADR-101 | Không lẫn domain với wire | Giữ explicit partial API / Web Dev | PASS logical mapping |
| VAL-108 | Lifecycle / blocker | ENT-100 TTL/init/recovery Q-103, FR-101 semantics Q-101 mở | Counter contract chưa baseline | Chốt retention/first-use/timeout policy / Web+Platform | BLOCKED |
