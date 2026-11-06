# Data Contract — Dữ liệu, tính nhất quán và vòng đời

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-DATA | 1.0.0 | review | 2026-11-06 | Web Fullstack Dev; recovery phối hợp Platform | E-100/E-103/E-104 tại [registry](README.md) | WEB-FRD/WEB-ARCH1.0.0; WEB-API document1.0.0/API0.1.0; nguồn PT-DATA0.1.0 |

Change log 1.0.0: biên tập [Data practical](../validation/practical-test/05-data-contract.md) theo hai nhóm counter Redis và demo browser-local; giữ entities, field meanings, key proposal, TTL unknown và consistency/recovery rules. Logical schema simulator vẫn `v1`; không đổi public wire schema.

## 1. Dữ liệu nằm ở đâu và ai cập nhật?

| ENT | Grain / identity / parent | Source of truth / writer / reader | Relationships / deletion |
|---|---|---|---|
| ENT-100 VisitorCounter | Một total cho site/environment scope còn Q-101; BR-101/FR-101 | Redis selected theo E-100; Counter Use Case write; UI read qua API TBD | Không lưu IP/cookie/user; init/reset authority Q-103 |
| ENT-101 Agent | Synthetic worker trong demoRunId, ID string; FR-106..FR-110 | Browser snapshot proposed ADR-101; reducer là writer duy nhất; UI/Scene read | currentTaskId null khi idle, ref current task khi working/terminal; xóa cùng run |
| ENT-102 Task | Một assignment mô phỏng, task ID unique/run; FR-108 | Cùng browser snapshot/reducer | Đúng một agent; running→completed/failed; không xóa task đang được ref; new run clear |
| ENT-103 SimEvent | Một thay đổi do simulator đề nghị, identity=(demoRunId,seq); FR-107/FR-108/FR-111 | Simulator tạo, reducer validate; recent buffer chỉ nhận accepted events | Ref agent/task cùng run; duplicate không thêm record; bỏ buffer item không xóa task |

Agent/Task/Event là dữ liệu demo tổng hợp, không phải AI session, command/job hoặc hook. Không sử dụng real username, host path, PID, API key, prompt transcript hay provider account. Reference My Office không quyết định entities hoặc identity của ứng dụng.

```text
VisitorCounter → Redis total                    [mandatory; contract decisions còn mở]
DemoRun → Agents → currentTaskId → Tasks         [extension conditional; browser-local]
Simulator → SimEvent → Reducer → Snapshot
                                  ├→ Dashboard / Scene
                                  └→ RecentActivity
```

## 2. Field dictionary — logical schema v1

Các object simulator là internal browser objects, không phải public API resources. FRD RULE-104..RULE-108 sở hữu enums/transitions; Data sở hữu representation và integrity. Extension vẫn chờ Q-100.

| Field | Meaning / encoding | Required / nullable / default | Invariant / lifecycle |
|---|---|---|---|
| VisitorCounter.total | Redis integer encoded decimal string; logical nonnegative count | Required khi known; không dùng null/0 thay unavailable | Max và JSON wire encoding Q-103; chưa wire schema |
| Agent.id | Opaque nonempty string, unique/run | Required/non-null; simulator tạo | Không derive từ real username/path; Redis escaping N/A |
| Agent.name | Synthetic display name, nonempty string | Required/non-null | Render escaped text; max length Q-107 |
| Agent.state | idle/working/completed/failed | Required/non-null; bootstrap idle | Theo FRD state machine |
| Agent.currentTaskId | Task ID string hoặc null | Required/nullable; bootstrap null | Working/terminal ref task đúng agent; idle null |
| Task.id / agentId | Nonempty string identity/ref | Required/non-null | Unique/run; logical foreign key tới Agent.id |
| Task.label | Synthetic description, nonempty string | Required/non-null | Không HTML/command; length Q-107 |
| Task.status | running/completed/failed | Required/non-null; tạo running | Terminal khớp result event |
| SimEvent.demoRunId | Opaque nonempty string scope | Required/non-null | New run tạo ID mới; không merge cross-run events |
| SimEvent.seq | Positive integer trong JS safe integer range | Required/non-null; bắt đầu 1 | Accepted event tăng đúng 1; đạt MAX_SAFE_INTEGER cần new run, không wrap |
| SimEvent.type | task.started/task.completed/task.failed/agent.reset | Required/non-null | Phân biệt result và reset |
| SimEvent.agentId | Nonempty string | Required/non-null | Agent đã bootstrap cùng run |
| SimEvent.taskId | Nonempty string hoặc null | Required/nullable | task.* phải string; agent.reset null; result đúng current task |
| SimEvent.occurredAt | UTC RFC3339 string, đuôi Z | Required/non-null | Browser clock để display; không quyết định event order |
| SimEvent.taskLabel | Label cho task mới | Required/non-null chỉ với task.started; absent ở type khác | Input tạo Task.label; không null placeholder |
| RecentActivity | Projection của accepted SimEvents | Có thể empty array | Seq giảm dần, capacity Q-107, không persistent |

Bootstrap agents là init snapshot, không cần thêm event bootstrap vào enum. Snapshot chứa runId, lastSeq, agents, tasks và recent accepted events. Logical schema version v1 không tự thêm field vào operational API.

| Ký hiệu dễ nhầm | Ý nghĩa |
|---|---|
| Required nhưng nullable | Field phải xuất hiện nhưng có thể mang `null`, ví dụ currentTaskId khi idle |
| Absent | Không có field trong object, khác `null`; taskLabel absent ở events không phải task.started |
| `seq` khác `occurredAt` | Seq xác định thứ tự; timestamp chỉ dùng hiển thị. Clock thay đổi không đảo thứ tự events |
| Transient / recent buffer | Chỉ tồn tại trong run/browser; không phải retained history hoặc nguồn replay |

## 3. Mapping với API

[OpenAPI API0.1.0](api-contract.yaml) sở hữu kiểu/required/null/errors trên wire. Các mappings dưới đây liên kết nguồn dữ liệu, không thay wire definitions.

| Operation / canonical schema | Field | Storage / derivation | Serialization / consistency |
|---|---|---|---|
| getLiveness / #/components/schemas/Liveness | status | Constant ok khi handler trả lời | Required/non-null; không Redis |
| getLiveness / Liveness | uptime | Monotonic process lifetime, giây | Number>=0, fractional allowed; transient |
| getLiveness / Liveness | timestamp | Response creation clock | Required UTC string theo UtcTimestamp; transient |
| getReadiness / #/components/schemas/Readiness | status, timestamp | Target init/check/drain outcome + response clock | Required/non-null; check không write business key |
| getReadiness / #/components/schemas/Error | error.code/message | Target dependency/init/drain failure | Required/non-null; không host/credentials/stack trace |
| getApplicationMetrics / text/plain | Exposition series | Process-local registry; uptime/completed-request hooks | String, không JSON business data; restart reset counters |
| getApplicationMetrics / Error | error.code/message | METRICS_UNAVAILABLE | Không cần Redis read |
| FR-101 / route+schema TBD | Counter total | ENT-100 | BLOCKED Q-101/Q-103; chưa chọn JSON number hay decimal string |
| FR-106..FR-111 / HTTP N/A | Agent/Task/Event | ENT-101..ENT-103 | Internal browser objects theo ADR-101, không fabricate API schemas |

Error enum được dùng chung nhưng operation chỉ trả applicable codes được mô tả tại API. Operational response cho phép compatible additional fields; required fields không null. Nullable task refs nội bộ không thay schema probes.

## 4. Access patterns và Redis mapping

| Pattern / FR | Read/write / cardinality | Atomic boundary / retry |
|---|---|---|
| Visit registration / FR-101 | Increment một total; trigger/identity/dedupe Q-101 | Single-key Redis INCR candidate; timeout sau write ambiguous, không blind retry |
| Counter display / FR-101 | Read một total | Missing key chưa phân biệt first use với data loss; Q-103 |
| Readiness / FR-103 | Bounded dependency check | PING proposed không tạo/reset counter; Q-104 |
| Simulator / FR-107/FR-108 | Một event, một reducer update | Validate rồi replace agent+task+buffer+lastSeq trong snapshot; views chỉ đọc sau commit |
| Recent activity / FR-111 | Latest C accepted events/run | In-memory buffer, C Q-107; không pagination/filter |

Redis được chọn cho counter. Key dưới đây là **proposed**, chưa code-observed; Redis chưa được chọn cho agent/task/event state.

| Thuộc tính key | Định nghĩa / điều kiện |
|---|---|
| Pattern | `nt548:<env>:web:v1:visitor:total` — proposed |
| Type / role | Redis string integer, authoritative total trong loss policy sẽ được chốt |
| Writer / reader | Counter Use Case write; API adapter read |
| TTL / start / reset | **TBD Q-103**. Chưa chọn expiry hoặc no expiry; không tự thêm EXPIRE |
| Missing/expired behavior | Unavailable/needs initialization theo policy Q-103; không tự total=0. Chỉ sau approved first-use init mới cho INCR-create |
| Atomicity | Confirmed single-key INCR linearizable trên primary; không app read-modify-write |
| Recovery | Restore/reset authority, backup/persistence và max/wire encoding Q-103 |

`<env>` lấy từ config allowlist; dev/staging/prod chỉ là ví dụ, không nhận raw URL/user input. Token không được chứa separator `:`; key không chứa personal identity. Redis Cluster chưa selected. Single-key operation không cần giả định multi-key slots; nếu thêm idempotency keys/shared state phải thiết kế slots và atomic boundary riêng.

| Thuật ngữ | Cách hiểu cần giữ |
|---|---|
| TTL | Thời gian key được giữ trước khi hết hạn. `TBD` là chưa quyết định; `null/no expiry` chỉ dùng khi đã chọn giữ không hết hạn |
| Atomicity | Một operation được thực hiện nguyên khối; không đồng nghĩa request end-to-end exactly-once |
| Durability | Dữ liệu còn giữ được khi process/pod/node lỗi; cần persistence/recovery policy và kiểm chứng riêng |
| RPO / RTO | Giới hạn dữ liệu có thể mất / thời gian phục hồi mục tiêu; còn Q-103, không tự gán số |

## 5. Lifecycle, failure và recovery

### ENT-100 — VisitorCounter

Init authorization, reset, TTL, eviction/memory policy, persistence, backup/restore cadence, max count và retention đều còn Q-103. Manifest được đọc không có volume/PVC hoặc persistence command; không suy Redis defaults thành bảo đảm survive pod replacement. Concurrent increment đúng không đồng nghĩa crash không mất dữ liệu hoặc replication lag bằng 0.

Nếu INCR đã thành công nhưng response mất, client không biết kết quả. Chốt retry/dedupe Q-101 trước counter contract. Nếu sau này dùng explicit registration mutation, phải chọn request identity/idempotency; chưa tạo duplicate store/TTL ở đây. Readiness lỗi không reset count. Unavailable khác total=0; không che dependency failure bằng cache bịa.

### ENT-101..ENT-103 — Một demo run trong browser

1. Tạo runId mới, clear run cũ rồi bootstrap 2–3 agents idle.
2. Một active simulator engine/mount phát event theo logical schema v1.
3. Reducer validate run/seq/ref/transition rồi synchronous commit snapshot; không `await` giữa validate và commit.
4. Dashboard/scene/recent panel đọc cùng snapshot. Timestamp để display, seq để order.
5. Unmount dừng timers; React remount cần lifecycle guard, không assume reference start-once đã an toàn.

Duplicate `seq<=lastSeq` là no-op; `seq>lastSeq+1` hoặc ref sai bị reject và diagnostic. Terminal tasks được giữ đến new run; task count/run limit Q-107 vẫn cần chốt để tránh memory growth ngoài buffer. Bỏ event khỏi recent buffer không xóa Task.

Replay/SSE retention N/A vì Optional deferred. Nếu cần history, phải chốt store/retention/access/cursor/gap response và revise FRD/API/Architecture/Data; Pub/Sub không tự cung cấp replay.

## 6. Classification và compatibility

| Data group | Classification / access | Retention / deletion | Evolution / migration |
|---|---|---|---|
| Visitor total | Aggregate, proposal không thu personal identifiers | TTL/reset/restore Q-103, Web + Platform | Giữ actual key/type/encoding/TTL khi thay backend; không tự đổi prefix v1→v2 |
| Synthetic domain | Demo-only, browser-local, không credentials | Clear run/reload; limits Q-107 | Logical schema v1; không copy My Office sess hoặc epoch-ms ts làm wire chuẩn |
| Operational responses/metrics | Operational info, exposure Q-102 | History do external scraper owner; không biến monitoring retention thành app history | Giữ status/type/time và process reset semantics qua Express/Laravel |

Không thiết kế transcript store hoặc tự thêm real session fields. Real agents cần business approval, security và data-minimization decision riêng. Counter JSON encoding cần tránh JS/PHP numeric conversion sai khi target được chốt; migration không thay loss policy bằng framework cache defaults.

## 7. Evidence, traceability và review

E-103/E-104 là source/config snapshot, không runtime proof. A-100/ADR-101 proposed; questions tại [registry](README.md). FRD sở hữu state/rules, API sở hữu wire, Architecture sở hữu component/port boundaries; Data không thay các định nghĩa đó.

| Finding | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-107 | Wire/domain mapping / major | Probe fields được map; ENT-101..ENT-103 HTTP N/A theo ADR-101 | Không lẫn domain schema với wire | Giữ partial API rõ / Web Dev | Logical mapping của nguồn được bảo toàn; chưa runtime-test |
| VAL-108 | Lifecycle / blocker | ENT-100 TTL/init/recovery Q-103; FR-101 semantics Q-101 | Counter contract chưa baseline | Chốt first-use/retention/timeout policy / Web + Platform | BLOCKED |

Field/table đầy đủ không chứng minh đã chạy concurrency, persistence, recovery hoặc migration parity tests.
