# Data Contract — Page views, idempotency và demo V1/V2

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-DATA | 1.1.0 | review | 2026-11-07 | Web Dev; Platform recovery; QA verification | E-103/E-104/E-109 tại [registry](README.md) | WEB-FRD/ARCH1.1.0; WEB-API document 1.1.0/API 0.2.0; WEB-DATA 1.0.0 |

Change log 1.1.0: giữ ENT-100..ENT-103 và logical schema v 1; thêm receipt/dedup mapping trong ENT-100, total no TTL, dedup 600 s, no auto-reset; stage-specific simulator limits và Recent 20 V2. TTL values đã accepted; storage/persistence/backup details chưa tự approve. Nguồn [PT-DATA0.1.0](../validation/practical-test/05-data-contract.md) giữ nguyên.

## 1. Entities và ownership

| ENT | Meaning / identity | Source of truth / writer / reader | Delivery Stage / lifecycle |
|---|---|---|---|
| ENT-100 VisitorCounter | Một total cho app/environment; requestId là identity một page-view registration, không identity người dùng | Redis; Counter Use Case writer duy nhất qua atomic operation; Next API read/serialize | V1, V2; total no TTL; receipts dedup 600 s; không auto-reset |
| ENT-101 Agent | Synthetic worker ID unique trong demoRunId | Browser snapshot; reducer writer; UI/scene read | V1 Idle/Working, V2 four states; 3 Agents/run; clear khi Reset/reload |
| ENT-102 Task | Một assignment mô phỏng, ID unique/run, đúng một Agent | Cùng snapshot/reducer | Tối đa 30 created tasks/run, 1 running/Agent; giữ task records đến new run |
| ENT-103 SimEvent | Một thay đổi simulator; identity=(demoRunId, seq) | Simulator tạo, reducer validate; không external ingestion | 5–8 s/event khi có transition; V1 minimal, V2 full; Recent projection chỉ V2 |

Agent/Task/Event không là AI sessions, commands hoặc hooks. Không thu IP/cookie/account/PID/paths/tokens/prompts. UUID requestId chống retry trùng, không bảo đảm unique visitor hoặc chống bot/abuse; không mở thêm tracking/auth feature.

## 2. Field dictionary — counter và logical demo v 1

Wire schema canonical tại API 0.2.0. Tổng được truyền bằng decimal string để không mất chính xác khi qua JS/PHP/JSON; đây là lựa chọn contract design dẫn xuất, không thay page-view business meaning.

| Field | Meaning / encoding | Required / nullable / default | Invariant / stage |
|---|---|---|---|
| VisitorCounter.total | Nonnegative integer, Redis decimal string; API string pattern 0 hoặc digits không leading zero | Required khi known; không null/0 để thay unavailable | Total no TTL/no auto-reset; max/init authority Q-103 |
| VisitorCounter.requestId | UUID từ browser document load | Required/non-null trên register; newF5 new ID; retries giữ ID | Không user/session identity; không metric label |
| VisitorCounter.receipt.total | Total tại original committed registration, decimal string | Required trong valid stored receipt | Replay trả đúng total này, không bắt buộc bằng latest global total |
| VisitorCounter.receipt.requestId | Registration identity | Required/non-null | Khớp UUID trong key và response |
| VisitorCounter.receipt.expiry | Redis-managed expiry 600 s từ first commit | Required TTL 600 khi tạo; replay không refresh | Không no expiry; restore không tùy ý kéo dài retention |
| VisitorCounter.replayed | Response boolean, không business count | Required; false first success, true replay | Derived từ lookup; replay không increment |
| Agent.id | Opaque nonempty string, unique/run | Required/non-null, simulator tạo | Không derive real username/path |
| Agent.name | Synthetic display text | Required/non-null | Escaped text; max string length còn Web design |
| Agent.state | idle/working/completed/failed | Required/non-null, bootstrap idle | V1 chỉ idle/working; V2 đủ 4 states |
| Agent.currentTaskId | Task ID string hoặc null | Required/nullable, bootstrap null | Working đúng running task; V2 terminal giữ ref đến reset; V1 finish proposal xem FRD |
| Task.id / agentId | Nonempty identity/logical foreign key | Required/non-null | Unique/run, ref đúng Agent |
| Task.label | Synthetic task text, không HTML/command | Required/non-null | String limit chưa chốt, không thực thi |
| Task.status | running/completed/failed | Required/non-null, created running | V1 basic completion đề xuất chỉ internal completed; V2 full results |
| SimEvent.demoRunId | Opaque run scope | Required/non-null | Reset/reload tạo ID mới, không cross-run merge |
| SimEvent.seq | Positive JS safe integer, bắt đầu 1 | Required/non-null | Next accepted seq tăng 1; không wrap; run mới trước overflow |
| SimEvent.type | task.started/task.completed/task.failed/agent.reset | Required/non-null | V1 basic types theo FRD; task.failed/terminal recovery V2 |
| SimEvent.agentId | Nonempty string | Required/non-null | Agent bootstrap cùng run |
| SimEvent.taskId | Task ID hoặc null | Required/nullable | task.* phải ID; agent.reset null; result đúng current task |
| SimEvent.occurredAt | UTC RFC3339 Z string | Required/non-null | Chỉ display; seq quyết định order |
| SimEvent.taskLabel | Label cho assignment mới | Required/non-null chỉ task.started, absent types khác | Input tạo Task.label, không nullable placeholder |
| RecentActivity | Derived accepted events | V2 required array, initial empty; V1 không triển khai FR-111 | 20 mới nhất, seq giảm; transient |

Snapshot chứa runId, lastSeq, agents, tasks. V2 thêm recent buffer; V1 không buộc lưu/render Recent Activity. Schema v 1 là logical/internal, không thêm agent/task public API.

## 3. API-to-data mapping

| Operation / canonical schema | Wire field / source | Persistence / rule |
|---|---|---|
| getVisitorCount / VisitorTotal | total→ENT-100.total | GET đọc latest snapshot; không write/init/increment |
| registerPageView / PageViewRequest | requestId→dedup identity | Validate UUID/body trước Redis; exclude all non-page view callers |
| registerPageView / PageViewReceipt | requestId, total, replayed | New commit increment+receipt; replay original receipt, no increment; TTL không refresh |
| getLiveness / Liveness | status=ok, uptime seconds, timestamp UTC | Transient process report, không Redis |
| getReadiness / Readiness | status=ready, timestamp | Target init/config/bounded Redis check/drain; không business key write |
| getReadiness / Error | DEPENDENCY_UNAVAILABLE hoặcNOT_READY | Sanitized, no host/secret; check timeout 2 s |
| getApplicationMetrics / text/plain | 4 families tại API | Registry process-local, last check redis_up; không app business history |
| Counter Error | INVALID_REQUEST, COUNTER_UNAVAILABLE, COUNTER_NOT_INITIALIZED, VISIT_OUTCOME_UNKNOWN, COUNTER_LIMIT_REACHED, INTERNAL_ERROR | Applicable status/code tại API; không fallback total 0 |
| FR-106..FR-111 / HTTP N/A | ENT-101..ENT-103 | Browser local; FR-111 V2 only, không API mutation/stream |

Required response fields không null; response additional fields được phép. Request registration không additional fields. App-generated errors khác perimeter denial/network timeout chưa có app response; không tự bổ sung login/401 API.

## 4. Redis key contract

Giữ total key proposal có sẵn; bổ sung request receipt key vì Q-101/Q-103 đã chốt idempotency. Đây là target design, chưa key/client implementation. `<env>` từ config allowlist, không raw URL/user input và không chứa separator `:`.

| Key pattern | Type / contents | Writer / reader | TTL / reset | Missing/invalid |
|---|---|---|---|---|
| `nt548:<env>:web:v1:visitor:total` | String decimal nonnegative integer | Atomic registration writes; GET/POST handler reads | **No expiry / TTL=null**, không EXPIRE và không auto-reset | Runtime missing→COUNTER_NOT_INITIALIZED; không tự coi 0 hoặc INCR-create để che mất dữ liệu |
| `nt548:<env>:web:v1:visitor:request:<requestId>` | String encoded receipt `{requestId,total}`; không JS/Lua float coercion của total | Cùng atomic registration boundary | **600 seconds**, từ first commit; replay không refresh | Absent có thể new ID hoặc expired/lost receipt; không claim dedup vượt window; malformed receipt fail closed, outcome unknown |

| Step | Atomic registration behavior / required invariant |
|---|---|
| 1 | Validate UUID, env, key types, total existence/range và receipt format trước writes; không tự init missing total |
| 2 | Nếu valid receipt còn tồn tại:trả original total, replayed=true; không increment hoặc refresh expiry |
| 3 | Nếu new ID và trạng thái hợp lệ:increment total và lưu receipt 600 s trong cùng server-side atomic unit; return decimal-string total, replayed=false |
| 4 | Error/timeout/uncertain write→sanitized exception mapping; không total reset hoặc new requestId retry; fault tests phải chứng minh supported failure behavior |

Không dùng client `GET→INCR→SET` tách rời hoặc per-pod memory dedup vì có 2 replicas. Candidate Redis script/function phải prevalidate, không interleave requests; atomic execution không tự chứng minh rollback giữa lỗi ghi, durability hoặc exactly-once qua state loss. [Redis scripting documentation](https://redis.io/docs/latest/develop/programmability/eval-intro/) là nguồn technical semantics; implementation phải test memory/type/permission/partial-failure cases. Nếu state inconsistency không thể phân giải, fail closed và điều tra, không tự increment vì receipt mất.

Redis Cluster chưa selected. Hai key phải cùng atomic routing boundary; future Cluster cần cùng hashslot/compatibility design trước khi đổi keyspace. Không thêm multi-store/event log/idempotency service ngoài yêu cầu này.

## 5. Request lifecycle, retry và exception handling

```text
New document / F5 -> new requestId
  -> POST registration
     -> new commit: total+1, receipt TTL600s, replayed=false
     -> same ID retry <600s: original receipt, no increment, replayed=true
     -> Redis/unknown failure: unavailable/outcome unknown, same ID retry only in window
  -> GET reads total without mutation
Reset Demo -> browser run only, NOT counter reset or visit
```

ID được giữ trong document lifetime kể cả hydration/remount effect retries; không reuse ID quaF5 hoặc dùng ID mới chỉ để retry failure. Client tính retry window bảo thủ từfirstattempt, dừng automatic retry sau 600 s; không retry vô hạn khi server receipt đã expired. Retry body không thay ID; không có API reset total hoặc delete receipt cho Viewer.

Nếu Redis đã commit nhưng HTTP response mất, retry cùng ID trong window trả receipt gốc. Receipt.total có thể nhỏ hơn latest total do visits khác; GET trả latest. Không hứa response byte-for-byte vì `replayed` đổi; business increment vẫn một lần trong điều kiện window/state intact. Sau expiry hoặc state loss, lặp ID có thể bị xem new; không exactly-once vô hạn.

Total 0 chỉ hợp lệ sau approved bootstrap một environment mới; candidate bootstrap SET-if-absent 0 có authority riêng, không nằm trong GET/POST/readiness và không chạy tự động mỗi restart. Init authority và xác minh first use vs loss còn Q-103. Max counter/wire đã decimal string nhưng giới hạn capacity policy cần Web/Platform chốt; overflow không wrap/reset, return error.

## 6. Persistence / backup / recovery plan — required, chưa approved configuration

| Control | Candidate / phương án | Chưa được duyệt / owner |
|---|---|---|
| Persistent storage | Persistent volume/PVC phù hợp node/failure model cho Redis data | StorageClass, size, access mode, node recovery / Platform |
| Redis persistence | Chọn và review AOF/fsync và/hoặc RDB snapshot policy | Chưa chọn mode, cadence, loss budget; không suy image defaults đã đủ / Platform+Web |
| Backup | Backup tách khỏi pod/volume, consistent snapshot, checksum, quyền hạn và restore procedure | Location, cadence, retention, encryption/grants / Platform |
| Restore rehearsal | Restore isolated Redis, tổng/receipt encoding/remaining expiry nhất quán rồi verify API | Environment, approval, RPO/RTO và đo thực tế / Platform+QA |
| Failure handling | Không recreate missing total thành 0; stop/triage uncertain state, restore approved point | Reconciliation cho confirmed views sau backup còn TBD; không claim lossless |
| Eviction/memory | Bảo vệ total/dedup trước expiry; monitor capacity | Memory/eviction policy, chưa mặc định no eviction hoặc guarantee / Platform |

Recovery workflow dự kiến: ngừng business writes khi cần → chọn backup/recovery point đã duyệt → restore cô lập → verify total, receipts và expiry còn lại → reconcile post-backup confirmed writes trong approved loss budget → test counter/dedup/readiness → cho traffic trở lại sau khi người có thẩm quyền xác nhận. Không restore stale total làm mất writes mới mà tự xem đạt; không refresh mọi receipt lại 600 s khi restore. Nếu không có evidence để reconcile, phải công khai data loss/unknown và chặn nghiệm thu recovery.

No TTL không đồng nghĩa durability. Total/dedup phải được xét cùng recovery point; restore một mà không cái kia có thể undercount/duplicate. RPO/RTO, cadence/retention/storage vẫn Q-103, chưa là values đã tested. Source Redis manifest hiện không volume/PVC; không thay manifest trong lượt này.

## 7. Demo lifecycle theo stage

3 Agents bootstrap Idle; max 1 running task/Agent; max 30 created tasks/run, không chỉ 30 current tasks. Synchronous reducer validate/commit cùng snapshot, không await giữa hai bước. V1 basic finish-to-Idle là design proposal FRD/Q-107; không tự accepted. V2 task completed/failed đưa Agent terminal, giữ ref đến agent.reset; Reset Demo global discard run khác agent reset.

V1 không FR-111 buffer. V2 recent 20 accepted events seq giảm; event 21 bỏ event cũ nhất, không xóa task. seq/timestamp khác nhau:seq order, timestamp display. Duplicate seq<=lastSeq no-op; gap/invalid ref reject+diagnostic; full cases V2, basic integrity V1 vẫn cần. Đạt 30 tasks:ngừng assignment mới, cho in flight finish, chờ Reset; không auto reset counter/run. Reset/reload clear old timers/snapshot/receipts của demo (không Redis visitor receipts), new runId rồi bootstrap.

Không retained history/replay/SSE. Unmount/remount guards ngăn engines trùng. Keyboard Reset/Text Dashboard dùng cùng snapshot; renderer failure không tạo failed task. String lengths/browser performance qualification còn Web/QA, không bịa limit mới ngoài 3/5–8/20/30 đã chốt.

## 8. Evolution, classification và findings

Aggregate counter không user identity; UUID là request identity, không ghi labels. Demo synthetic/browser-local, không credentials. Metrics operational access hạn chế theo Q-102; monitoring retention không business event history. Future migration giữ total key/type/no TTL, receipt key/600 s/original total/retry meaning; không dùng framework cache prefix/default serialization thay contract.

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-107 | Wire/domain / major | API 0.2.0 fields map ENT-100 và transient reports; demo HTTP N/A/stages rõ | Không lẫn domain/wire | Cross check / Web+QA | Document mapping; runtime pending |
| VAL-108 | Lifecycle/recovery / blocker | Total no TTL/dedup 600/no reset đã chốt; storage/init/backup/restore/RPO/RTO chưa approve | Không còn TTL decision blocker; chưa recovery ready | Platform/Web/QA duyệt và diễn tập | PARTIAL residual gate; không claim durability |
