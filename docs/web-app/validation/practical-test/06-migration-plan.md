# Migration feasibility draft — intended Express → Laravel

| Document ID | Version | Status | Date | Owner role | Source / target intent | Upstream |
|---|---|---|---|---|---|---|
| PT-MIG | 0.1.0 | DRAFT | 2026-11-05 | Web owner; migration authority TBD Q-100 | E-100 future direction; target source 2110eddec91bc3e34137c86fef693095c4afb677 | PT-BRD/FRD/API/ARCH/DATA 0.1.0; shared standard 1.0.0 |

Change log 0.1.0: intent-only feasibility và discovery gates; không runnable cutover plan. **Source-baseline discovery: BLOCKED. Migration readiness: BLOCKED.**

## Rationale, scope và baseline confidence

Người dùng yêu cầu đánh giá định hướng Express→Laravel tương lai, chưa có business case định lượng, ngân sách hoặc approval thực thi. BR-108 deferred; không là điều kiện nghiệm thu NT548. Không triển khai Laravel, không chuyển Next route handlers thành “Express baseline”. Current source là Next, chưa tìm thấy Express dependency/server/routes/tests (E-103). Laravel version/runtime/extensions/dependencies chưa chọn; không đưa PHP version/library claim chưa xác minh.

Consumers dự kiến: frontend counter UI (contract còn blocked), probes và scraper bên ngoài. Simulator theo ADR-101 ở browser nên không chuyển thành Laravel worker. Optional SSE, real agents/auth đều ngoài parity baseline hiện tại.

| Baseline inventory | Observed / gap | Consequence |
|---|---|---|
| Source Express routes/middleware | Không tồn tại trong inspected app | MIG-100 blocked; cần repo/ref implementation và tests sau |
| Next probes | Success JSON code-observed; readiness always 200 | Evidence discovery input, không dùng làm proof Express parity |
| API 0.1.0 | Partial DRAFT, readiness/metrics có proposed delta | Phải accept/version baseline trước migration |
| Data 0.1.0 | Logical/proposed; counter semantics/TTL chưa chốt | Chưa có storage compatibility guarantee |
| Tests/production traffic/volumes | Chưa có characterization evidence | Không đặt cutover date/window/rollback time |

## Contract invariants và parity matrix

| FR / AC / invariant | Old evidence | Target obligation nếu migration được duyệt | Verification / pass condition | Status / owner |
|---|---|---|---|---|
| FR-102, AC-103, getLiveness | Next handler E-103; Express missing | 200 body status/uptime/timestamp theo accepted API; Redis independent | Golden response + Redis down + schema/units/time tests | BLOCKED old baseline / Web+QA |
| FR-103, AC-104/105, getReadiness | Next always 200 khác proposed semantics | Preserve accepted readiness rules, 200/503/error codes/deadline | Dependency failure/restore/init/drain cases equivalent | BLOCKED Q-104 + Express / Web+Platform |
| FR-104, AC-106, getApplicationMetrics | No source implementation | Text format/names/types/labels/process reset semantics giống baseline | Prometheus parser, traffic deltas và scraper integration | BLOCKED Q-106 / Web+QA |
| FR-101, AC-101/102, ENT-100 | Counter route/key absent | Preserve visit trigger, idempotency policy, integer encoding, key/TTL | Concurrent visits, timeout ambiguity, restore/restart characterization | BLOCKED Q-101/Q-103 / Web |
| JSON/error edge cases | Framework behavior chưa captured | Explicit 404/405/validation envelopes/status; absent/null; ID string; UTC; empty [] vs {} | Consumer fixtures positive/negative; không chấp nhận Laravel defaults làm bằng chứng | BLOCKED discovery / Web+QA |
| Access/origin/security | Q-102 chưa chốt | Auth middleware nếu baseline có; CORS, CSRF, cookies, route slash/method behavior tương đương | Browser/probe/scraper integration tests, denied cases nếu áp dụng | BLOCKED / Web+Platform |
| FR-106..111, RULE-104..108 | Proposed browser demo | Backend migration không đổi simulator states/animations/task rules | Frontend regression scenarios AC-108..114 | Conditional; extension selection Q-100 |
| NFR-100..106 | No runtime evidence | Non-root packaging, readiness, capacity, recovery, data access, labels, text usability | QA compare tại cùng workload/environment, thresholds được duyệt | BLOCKED thresholds/tests |

Changing always-200 readiness into dependency-aware readiness là product/operational contract change trước baseline, không được ngụy trang thành migration parity. Nếu parity migration bắt đầu từ một khác biệt như vậy, ghi separate breaking-change proposal và consumers phê duyệt.

## Strategy và alternatives

| ADR / status | Alternatives | Proposed approach / rationale | Cost / revisit |
|---|---|---|---|
| ADR-105 / proposed (migration-owned) | Single routing cutover; incremental routes; shadow reads | Một cutover sau staging parity, giữ nguyên Redis schema và single active writer để nhỏ gọn | Có maintenance/drain requirement TBD; incremental tăng routing ownership; shadow chỉ read-only và không tính thêm visits |

Chưa “selected” strategy do thiếu old system và downtime tolerance. Không dual-write counter để so sánh, vì sẽ tăng hai lần hoặc split authority. Không shadow mutating endpoint. Khi topology/traffic/risk thay đổi cần review ADR trước runbook.

## Phases và gates — planned, dates TBD

| MIG | Dependencies / entry | Deliverable / owner | Exit evidence / date |
|---|---|---|---|
| MIG-100 Discovery | Verified Express source/ref thiếu → BLOCKED | Inventory routes, middleware, config, storage, registry, auth và consumers / Web | Runtime source có characterization tests; API/Data accepted versions; TBD, không dùng hạn NT548 |
| MIG-101 Laravel adapter feasibility | MIG-100 passed, business approval | Version/dependencies compatibility review; HTTP/domain/Redis adapter design / Web | Demo contract fixtures và dependency feasibility được review; TBD |
| MIG-102 Parity verification | Target implementation có trong nhiệm vụ khác | Golden fixtures/error/default serialization/concurrency/failure tests / QA+Web | Matrix parity không còn FAIL/BLOCKED; approved NFR targets đạt; TBD |
| MIG-103 Staging/recovery rehearsal | MIG-102; Platform window/backup policy | Rehearsal route switch, drain, Redis backup/restore, read/write compatibility / Platform+Web+QA | Recovery time/data-loss đo được trong giới hạn approved; TBD |
| MIG-104 Controlled cutover | G0..G4 pass, authority/window xác nhận | Single writer route switch và verify / Platform executes, Web validates | Correct API, ready, scrape, counter invariants; TBD |
| MIG-105 Observe/retire | Cutover đạt; rollback còn an toàn | Observe và retire old runtime sau sign-off / authority TBD | Window/threshold TBD Q-108, consumer acceptance, rollback artifact retained; TBD |

Không tự chuyển gate sang PASS vì document đủ headings. Gate business authority G0=Q-100; baseline G1=MIG-100; contract G2=MIG-102; recovery G3=MIG-103; operations G4=Q-102/Q-104/Q-108 đã chốt.

## Data compatibility và recovery boundary

| Data | Readers/writers | Transformation / writer authority | Reversal / recovery gate |
|---|---|---|---|
| ENT-100 Redis counter | Old Express hoặc new Laravel writer, không đồng thời; readers tương thích same encoding | Preserve actual key/type/TTL đã approved, không derive từ Laravel cache prefix defaults | Post-cutover increments phải old reader đọc được; không restore snapshot cũ làm mất increments mới |
| ENT-101..103 browser | Browser reducer v1 | Không move vào SQL/Laravel ORM trong migration | Frontend assets/version compatibility; không data copy cần thiết |
| Operational metrics | Per-process registry, external scraper | Giữ names/types/labels; restart reset documented | Không restore process uptime/counters như business data |

TTL, Redis integer vs PHP/JSON number coercion, null/empty và key prefix là parity invariants. Nếu cần change schema: reader/writer compatibility, reversible transform, backup/restore, reconciliation của writes sau cutover và forward recovery phải được duyệt trước. Không chạy transform/backup trong bài test này.

## Cutover concept — không được thực thi từ draft

| Order | Preconditions / authority | Planned action | Signal / abort |
|---|---|---|---|
| 1 | G0..G4 passed; Platform+Web xác nhận | Freeze schema, record baseline total/metrics/errors và compatible recovery point | Thiếu evidence hoặc access → abort |
| 2 | New service staging-ready | Stop accepting old mutations, mark old not ready và drain requests theo deadline approved | In-flight writes chưa rõ/ambiguous → hold; không launch second writer |
| 3 | Single writer fenced; target config verified | Platform đổi routing ownership sang new service theo agreed integration | New ready đúng, counter read/write/operational parity smoke đạt; mismatch → rollback gate |
| 4 | Signals đạt | Quan sát window/thresholds được duyệt | Error/latency/data mismatch vượt thresholds → decision rollback |

SSE không selected nên connection drain streaming N/A hiện tại. Nếu baseline sau này thêm SSE, MIG-100 phải inventory active connections, reconnect/cursor/replay/resnapshot, proxy buffering/timeouts và drain timeout trước gate G2/G4. Không promise reconnect giữ events khi retention chưa có.

## Rollback và forward recovery

| Trigger | Decision role / action | Post-cutover writes / verification | Time/loss limit / unsafe boundary |
|---|---|---|---|
| Contract/schema/data invariant mismatch; readiness sai | Authority TBD với Web+Platform; stop new mutations, drain, route về compatible old runtime | Đọc cùng Redis key mới nhất; đối chiếu increments được xác nhận, không ghi đè snapshot trước cutover | RTO/RPO/observation threshold TBD; thiếu limits chặn G3 |
| Capacity/error metrics vượt approved target | Cùng role; route rollback sau fence single writer | Probe/counter/metrics/client checks; xác minh no dual writer | Thresholds TBD Q-104; chưa được nghiệm thu |
| Incompatible data writes đã diễn ra | Không rollback image đơn thuần | Freeze writes, reconcile journal/authoritative records theo plan được duyệt; forward fix hoặc reversible transform | Nếu không có retained evidence, không thể chứng minh lossless recovery → cấm cutover trước |

Restoring a stale backup làm mất post-cutover increments là hành vi không được tự chấp nhận. Retirement chỉ sau observation và consumer sign-off; giữ old artifact/config và accepted contracts theo retention TBD. Không có self-approval hoặc ngày retirement tự đặt.

## Risks, questions và validation

Rủi ro chính: chưa có Express baseline, default errors/middleware thay đổi wire, Laravel cache client tự thêm prefix/serialize khác, accidental dual writer, readiness mismatch và reset metrics interpretation. Owner Web+QA giải parity; Platform giải routing/window; người dùng giải business scope. Questions Q-100/101/102/103/104/106/108 tại report; upstream đều DRAFT nên chưa usable migration baseline.

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|
| VAL-109 | Source identity / blocker | PT-MIG 0.1.0 MIG-100: Express intended, only Next source observed | Không migration-ready | Source-baseline discovery sau có source / Web | BLOCKED |
| VAL-114 | Upstream invariants / major | Matrix covers five upstream drafts; parity tests chưa có | Feasibility planning thôi | Resolve gates và characterize / Web+QA+Platform | PASS plan coverage; BLOCKED execution |

Plan completeness ở mức intent-only: PASS có giới hạn. Source-baseline discovery, implementation parity và cutover readiness: **BLOCKED**. Không xem migration là nhiệm vụ nghiệm thu đồ án.
