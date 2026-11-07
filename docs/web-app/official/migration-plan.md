# Migration Plan — Định hướng thay server/API từ baseline Next Fullstack

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-MIG | 1.1.0 | review | 2026-11-07 | Web owner; Platform/QA phối hợp | E-103/E-104/E-109 và [registry](README.md) | WEB-BRD/FRD/ARCH/DATA1.1.0; WEB-API document 1.1.0/API 0.2.0; WEB-MIG 1.0.0 |

Change log 1.1.0: cập nhật source baseline thành Next.js Fullstack thực tế, không yêu cầu tìm/dựng Express. Laravel chỉ còn candidate tương lai nếu có quyết định riêng; không target release hiện tại. Giữ MIG-100..MIG-105 và ADR-105, bổ sung V1/V2, page-view/idempotency 600 s, no TTL, readiness và metric invariants. [PT-MIG0.1.0](../validation/practical-test/06-migration-plan.md) là lịch sử đã được E-109 thay về stack.

## 1. Mục đích và phạm vi

V1/V2 dùng Next cho UI và server-side API, Redis là dịch vụ riêng. Không Express release. Tài liệu này chỉ hướng dẫn đánh giá một thay đổi runtime/server API trong tương lai, ví dụ tách API sang Laravel trong khi giữ Next UI. Chưa có business case, target version, budget, window hoặc approval thực hiện migration. BR-108 vẫn deferred; migration không là điều kiện nghiệm thu V1/V2.

Không chuyển UI/Office simulator sang framework/backend khác chỉ vì một migration server/API. Browser run, state/stage rules và rendering contracts phải được bảo toàn. Không dựng Express như bước trung gian hoặc dùng thiếu Express source làm blocker.

## 2. Baseline thật và gaps

| Baseline | Observed / accepted | Phần chưa chứng minh |
|---|---|---|
| Current implementation | E-103: Next starter, /healthz, /ready handlers; ready luôn 200 | Counter, metrics, target ready và Office chưa có runtime evidence |
| Target contracts | E-109 và API 0.2.0:V1 counter/operations, Office basic; V2 full | Chưa là acceptance-tested implementation baseline |
| Data | Total no TTL/no auto reset, receiptTTL600 s; browser run transient | Atomic registration/restart/restore/init/backup/RPO/RTO chưa verified |
| Integration | Next standalone/configured Redis | Probe 2 s/3 s/startup≈50 s/access enforcement còn implementation/Platform confirmation |
| Future target | Không chọn runtime/version cho migration hiện tại | Chỉ mở MIG-101 sau business approval; Laravel là ví dụ, không commitment |

MIG-100 phải characterize Next implementation khi V1/V2 thực sự được triển khai, pin source/ref và consumer fixtures. Không lấy bảng target hoặc current always 200 làm bằng chứng rằng cảAPI0.2.0 đã chạy đúng.

## 3. Parity matrix theo Delivery Stage

| Invariant / trace | Obligation khi migration được duyệt | Verification / pass condition | Stage / current status |
|---|---|---|---|
| FR-101, AC-101/102, ENT-100, getVisitorCount/registerPageView | F5 new ID, same-ID retries; GET không ghi; receipt original total, replayed semantics; total decimal string, no TTL/no reset; dedup 600 s không refresh | Concurrent requests across replicas; commit-response loss; expiry boundary; init/missing/type/overflow/error cases | V1, V2; target defined, implementation parity BLOCKED |
| FR-102, AC-103, getLiveness | Process-only 200, uptime seconds, UTC; Redis-independent | Redis down và process timeout cases | V1, V2; current handler observed, chưa golden runtime |
| FR-103, AC-104/105, getReadiness | Init/config, Redis 2 s, probe 3 s, startup≈50 s; 200/503/error codes; no business writes | Fault/timeout/restore/drain/startup và routing tới Office | V1, V2; target pending implementation |
| FR-104, AC-106, getApplicationMetrics | Four names/types/units/labels; duration histogram; redis_up 0/1; process resets; no app CPU/RAM/K8s duplication | Prometheus parser, latency/traffic deltas, last-check semantics, scrape target khi NotReady | V1, V2; buckets/wiring và runtime chưa chứng minh |
| FR-100/105, AC-100/107 | UI/counter errors trung thực; fullstack integration/non root/access boundary | Image/config/probes/authorized+denied consumers và UI smoke | V1, V2; Platform/QA pending |
| FR-106..110, RULE-104..107, AC-108..111/113/114 | V1 basic 3 Agents/Idle Working, Text Dashboard/keyboard; V2 four states/full validation/animations; 5–8 s, 1 running/Agent, 30 tasks/run, Reset/reload | Frontend/reducer/lifecycle regressions theo stage; không chuyển simulator thành server worker | V1 basic, V2 full; V1 finish detail Q-107 |
| FR-111, RULE-108, AC-112/113 | Recent 20 accepted events transient, seq order, not persisted history | 21 events, duplicate/gap/reset; không bắt V1 có panel/buffer | V2 only |
| NFR-100..106 | Non root, accepted timings/access/fallback/limits và approved performance/recovery thresholds | Cùng workload/device/environment; counter/dedup/storage restore đồng nhất | Residual qualification và parity BLOCKED |

Framework defaults không chứng minh parity. Characterize serialization decimal strings/UUID/UTC, required/null, unknown fields, 400/500/503/error codes, 404/405, origins/CORS và authorized access. Không thêm auth/CSRF/cookies nếu baseline không có; chỉ bảo toàn security contract đã triển khai. Uptime/timestamps không cần equal byte-for-byte giữa process, nhưng type/meaning/range phải đúng.

Readiness always 200 hiện tại→target dependency-aware 503 là thay đổi contract phải triển khai/kiểm chứng cho V1 trước khi nó trở thành migration baseline, không ngụy trang thành framework parity. API 0.2.0 target không đồng nghĩa deployed API version.

## 4. Strategy và phases

| ADR / status | Alternatives | Proposed approach / trade-off |
|---|---|---|
| ADR-105 / proposed, future-only | Single cutover, incremental routes, shadow reads | Sau approved target/baseline, chọn một routing cutover và giữ Redis contracts; shadow chỉ read-only, không register visit hai lần. Không selected strategy khi chưa business approval/window |

Single active writer ở đây là logical ownership của mutation path/old-vs-new version trong cutover, không ép current Next chỉ được một pod. Current nhiều replicas phải cùng dùng atomic Redis registration. Không dual-write total hoặc shadow POST để so sánh.

| MIG | Entry / dependencies | Deliverable / owner | Exit evidence / date |
|---|---|---|---|
| MIG-100 Discovery | Có business request tương lai; pin Next implementation/ref | Inventory Next routes/runtime/config/middleware/Redis script/metrics/consumers và stage scope / Web+QA | Accepted contracts + characterized runtime fixtures; TBD, không deadline NT548 |
| MIG-101 Target adapter feasibility | MIG-100 đạt, approved target choice | Đánh giá server/API target candidate/version/dependencies; HTTP/domain/Redis seams; Next UI retained nếu scope vậy / Web | Target feasibility được review; không mặc định Laravel version |
| MIG-102 Parity verification | Target implementation từ nhiệm vụ được ủy quyền riêng | Schema/error/serialization/idempotency/TTL/timing/metric/frontend stage tests / Web+QA | Matrix hết FAIL/BLOCKED và approved thresholds đạt |
| MIG-103 Staging/recovery rehearsal | MIG-102 + approved backup/window/policy | Route/drain/writer fence, backup/restore, reconcile total+receipts / Platform+Web+QA | Đo recovery và data loss trong limits đã duyệt |
| MIG-104 Controlled cutover | G0..G4 đạt, authority/window xác nhận | Freeze schema, fence old mutations, route new target, verify / Platform executes, Web validates | Counter/API/probe/metrics/UI stage invariants đúng |
| MIG-105 Observe/retire | Cutover đạt, rollback compatible | Observe rồi retire old runtime theo sign-off / authority TBD | Window/threshold/retention approved, consumer acceptance |

| Gate | Requirement | Current disposition |
|---|---|---|
| G0 | Business approval, scope, target/authority cho migration | DEFERRED; Q-100 release đã giải, không là migration approval |
| G1 | MIG-100 verified Next baseline | BLOCKED implementation/characterization, không Express absence |
| G2 | MIG-102 contract/stage parity | Chưa target/tests |
| G3 | MIG-103 recovery/compatibility | Storage/backup/RPO/RTO còn Q-103 |
| G4 | Access, timings, route/drain/window/rollback ownership | Release policies đã chốt, operational proof còn Platform/QA |

## 5. Data compatibility và post-cutover writes

| Data | Required compatibility | Unsafe rollback boundary |
|---|---|---|
| ENT-100 total | Actual key/type/decimal encoding, no TTL, no auto reset; old/new readers đọc newest committed total | Không restore stale backup để mất post-cutover page views |
| ENT-100 request receipts | Same requestId scope, original total, replayed meaning, 600 s và không refresh; old/new writer dùng chung dedup boundary | Không đổi prefix/serialize hoặc reset expiry để replay tăng trùng; total/receipt restore phải cùng point |
| ENT-101..103 | Browser schema/run/stage guards, 30 tasks cap; V2 recent 20 | Không chuyển sang SQL/backend store nếu không có scope approval |
| Operational metrics | Same 4 families và reset semantics, authorized scrape | Không restore process counters như dữ liệu nghiệp vụ |

Future client/framework không được tự ép total thànhfloat/intJSON, mặc định cache prefix hoặc set TTL lên total. Giữ remaining dedup expiry khi restore, không refresh thành 600 s mới để che lịch sử. Incompatible data/schema transform cần reader/writer compatibility, reversible transform hoặc forward-recovery/reconciliation đã diễn tập trước cutover.

## 6. Cutover concept — không thực thi từ tài liệu này

| Order | Precondition | Planned action | Abort / evidence |
|---|---|---|---|
| 1 | G0..G4 đạt | Freeze schemas, ghi baseline total/receipt state, metrics/errors và recovery point | Missing access/backup/accepted limits→abort |
| 2 | Target staging-ready | Ngừng old mutations, drain/fence in-flight writes | Unknown writes chưa phân giải→hold, không second mutation path |
| 3 | Writer ownership/config verified | Platform đổi routing tới target server/API | Ready, counter/read/retry/metrics/UI stage smoke phải đúng |
| 4 | Signals đạt | Observe trong approved window | Contract/error/latency/data mismatch→rollback decision |

SSE không selected nên streaming drain N/A. Nếu future approved scope thêm SSE, mới inventory connections/cursor/retention/replay và revise contracts; không promise replay từ transient buffer.

## 7. Rollback / forward recovery

| Trigger | Decision / action | Data verification / limits |
|---|---|---|
| API/idempotency/data/ready mismatch | Authorized Web+Platform decision:stop new mutations, drain, fence, route compatible old runtime | Old reader đọc latest total và valid receipts; không snapshot overwrite; RPO/RTO approved |
| Latency/error vượt approved target | Sau fence chọn rollback và verify consumers | Check metrics 4 families, probe 2 s/3 s/routing/UI stage; không dual writer |
| Đã có incompatible writes | Không rollback image đơn thuần; freeze, reconcile/forward fix theo approved plan | Không retained evidence để chứng minh lossless thì cấm cutover từ trước; không claim 600 s dedup đủ restore history |

Retire chỉ sau observation/consumer sign-off, giữ artifacts/config/contracts theo retention được duyệt. Không self-approval hoặc ngày retirement tự đặt.

## 8. Findings và readiness

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-109 | Source identity / major | E-109 chốt Next Fullstack, source Next observed; Express không prerequisite | Baseline framework đã rõ, full V1/V2 runtime chưa characterized | MIG-100 pin Next implementation / Web+QA | Identity RESOLVED; characterization BLOCKED |
| VAL-114 | Upstream parity / major | Five upstream docs 1.1.0/API 0.2.0; stages/TTL/timings/metrics đã định nghĩa | Future feasibility, không execution-ready | Business case, target, tests, recovery / Web+Platform+QA | Plan ở mức future; cutover BLOCKED |

Migration vẫn deferred direction; không là công việc triển khai V1/V2 hoặc điều kiện nghiệm thu đồ án. Không application/Kubernetes/CI/CD/Validation changes trong lượt này.
