# Migration plan thử nghiệm — discovery trước khi thay backend

> SANDBOX. Áp dụng `backend-migration-planning` để kiểm tra xử lý thiếu đầu vào. **Cutover readiness: BLOCKED.** Không thực thi migration, không coi Next frontend là Express source.

| Document ID | Version | Status | Date | Owner role | Source ref / target intent | Upstream versions |
|---|---|---|---|---|---|---|
| TEST-MIG | 0.1.0 | draft | 2026-11-05 | Web Dev + Platform; cutover authority TBD Q-06 | Project `2110edd`; Express source missing Q-04; target TBD Q-06 | TEST-BRD, TEST-FRD, TEST-API, TEST-ARCH, TEST-DATA đều 0.1.0 |

Change log 0.1.0: tạo discovery/parity gates có điều kiện, không tạo executable-ready plan. Follow-up QA: viết đầy đủ từng AC/ENT ID trong parity matrix để tra cứu không phụ thuộc cách hiểu ID viết gọn; revision hash lưu tại execution log. Không có user-approved migration intent/target trong yêu cầu hiện tại. Laravel chỉ là ví dụ trong description của Skill và prompt boundary test, không phải release commitment của đồ án.

## Rationale, scope và baseline confidence

Mục tiêu **lần test** là xem Skill có đòi evidence source/target và bảo toàn contracts hay tự điền template. Rationale business cho việc thay backend chưa có nguồn trong phiên này, nên không bịa lợi ích/cost saving/deadline migration. Đây là partial draft/discovery response hợp lệ khi minimum inputs thiếu, không là quyết định migrate.

Current evidence: Next.js starter + two Next handlers + Redis manifests. Express là intent trong README, không có backend entry/router/tests để pin. Không thể dùng contract hai probe của Next như baseline đầy đủ cho Express. Nếu sau này có replacement Express, Next frontend và consumer boundary phải được giữ/đánh giá riêng; thay UI framework là scope khác.

Baseline documents đều draft/proposed 0.1.0, chưa accepted. Consumers có thể gồm UI và kubelet theo nguồn; actual backend consumers/auth/webhooks/background jobs/streams chưa inventory Q-04/Q-06. Không dùng script fixtures Queue Board của bundle làm business parity evidence NT548.

## Contract invariants và parity matrix

Mỗi hàng là nghĩa vụ kiểm tra **có điều kiện nếu migration được yêu cầu**, không là kết quả đã chạy. Compare enums/types/required/null/meaning; uptime/timestamp thay đổi tự nhiên không cần equality byte-for-byte.

| Invariant | Old evidence / baseline | Target obligation có điều kiện | Verification / pass condition | Status / owner |
|---|---|---|---|---|
| BR-01/FR-01/RULE-01/AC-01/AC-02 | Intent README/WBS; semantics TBD | Không tự đổi cách tính lượt xem; chốt baseline trước replacement | Characterization + concurrent/retry/failure tests sau Q-02/Q-05 | not run; BLOCKED / Web + QA |
| BR-02/FR-02/RULE-02/AC-03/AC-04 | E-05, API0.1.0 getHealth của **Next**, không chứng minh Express | Giữ behavior nếu endpoint nằm trong approved replacement scope; nếu giữ Next thì N/A migration với lý do | Shape/status/enum/nonnegative uptime/UTC timestamp; Redis outage không bị biến thành health dependency | not run; ownership Q-03/Q-04 / Web + Platform |
| FR-03/RULE-03/AC-05/AC-06 | E-06, API0.1.0 getReadiness của Next; current 200 | Không âm thầm đổi 200 thành 503 như framework replacement; target ready change là proposal riêng | Probe/consumer contract tests và dependency fault characterization | not run; BLOCKED Q-03/Q-04 / Web + QA |
| FR-04/RULE-04/AC-07/AC-08 | README metrics intent, payload chưa có | Chốt schema/labels/access/limits trước bảo toàn metrics | Scrape/load failure + missing-data tests với definitions được chốt | not run; BLOCKED Q-04/Q-07 / QA |
| ENT-01, ENT-02 transient mappings | Data0.1.0, API HealthReport/ReadinessReport | Không convert numbers thành strings, không thêm null/đổi enums; time UTC, reports không thành durable records tự ý | Schema/sample tests và source/runtime comparison; không compare exact time/uptime | not run target; BLOCKED / Web + QA |
| ENT-03 / NFR-02 / CTL-02 | Key/TTL/ownership/consistency TBD | Giữ baseline keys/types/TTL/encoding khi có; không đặt TTL hoặc dual writes mới để “migrate” | Reader/writer compatibility + restore/concurrency/reconciliation test | not run; BLOCKED Q-02/Q-05 / Web + Platform |
| NFR-01 / CTL-01 | Next container hardening config E-07/E-08 | Target deployment cần evidence least privilege tương thích khi component bị thay | Config review + runtime UID/capabilities/consumer checks | not run target; BLOCKED / Platform |
| NFR-03 / CTL-04 | Thresholds/window TBD Q-07 | Đo dưới cùng điều kiện đã chốt, không lấy target tự ý | Before/after load/error/latency measurement | not run; BLOCKED / QA |
| NFR-04 / CTL-05 | README/config mismatch C-04; offline render có | Giữ intended access policy được chốt, không dựa tên folder | Namespace render + live allow/deny evidence trước cutover | not run live; BLOCKED / Platform |
| BR-03 | Non-software evidence collection | Migration evidence bổ sung, không thay nghiệm thu đồ án | Log gắn commit/test/owner và approval authority nguồn | not run / Documentation + nhóm |

Nếu target sau này là Laravel, inventory phải bao gồm route normalization/trailing slash, 404/405, validation error envelope/status, absent vs null, IDs string/number, JSON empty object vs array, auth/CORS/CSRF, serialization/time và middleware defaults. Hiện chưa biết endpoint/auth/mutations thực tế của Express, nên không áp framework defaults như baseline. Không giả định có SSE hoặc background job để viết parity giả.

## Strategy và gates

| Choice / status | Alternatives | Proposal / cost / revisit trigger |
|---|---|---|
| Discovery-first / proposed test response, theo ADR-01/02 | Single cutover; incremental routes; shadow reads | Chưa chọn rollout strategy khi source/target/consumers thiếu. Sau Q-04/Q-06, so sánh operation boundary, downtime và test capacity. Tránh shadow/dual writes cho counter vì có thể nhân đôi lượt đếm |

| MIG ID | Entry gate | Deliverable / owner | Exit gate | Dates |
|---|---|---|---|---|
| MIG-01 | Có migration intent/target/authority Q-06 | Pin Express repo/ref, routes/consumers/auth/errors/storage/tests, baseline contracts; Web + QA | Inventory có nguồn; gaps đóng hoặc được scope authority ghi deferred, không fake acceptance | TBD; không lấy deadline môn học làm migration date |
| MIG-02 | MIG-01 + approved behavior/Data baseline | Target adapter/characterization/parity suite được thiết kế; Web + QA | FR/operation/entity/NFR coverage và compatibility pass có log thực tế | TBD |
| MIG-03 | MIG-02 + recovery/data compatibility evidence | Staging rehearsal, routing/drain/monitor/rollback procedure; Platform + Web + QA | Chứng minh old/new readers/writers, backup/restore/reconciliation; thresholds/time window/authority chốt | TBD |
| MIG-04 | MIG-03 + explicit decision authority và review | Controlled cutover → observe → retire có điều kiện; Platform + scope owner TBD | Signals đạt và sign-off có nguồn; retirement không trước acceptance | TBD |

Tất cả gates hiện **BLOCKED**, không có phase nào đã triển khai. Work/deliverable trong bảng là kế hoạch tương lai để định nghĩa sau review, không là lệnh cho lượt này.

## Data compatibility và recovery boundary

ENT-01/02 không có durable data transform; cần giữ API meaning nếu operation nằm trong migration scope. ENT-03 chưa biết old writer/key/type/TTL/reset nên chưa có safe dual-reader/writer hoặc reverse migration. **Không đề xuất dual writes** như cách so sánh counter. Nếu sau cutover có writes với schema/type/TTL không đọc được bởi phiên cũ, image rollback có thể làm mất/lệch dữ liệu. Chặn MIG-03/04 cho tới khi có reversible transform hoặc forward-recovery/reconciliation path đã diễn tập. Backup/restore/RPO/RTO đều TBD Q-05/Q-07; không hứa phục hồi bằng git revert.

## Conditional cutover / rollback checklist, không executable runbook

| Order | Preconditions / authority | Planned decision/action | Signal / abort condition |
|---|---|---|---|
| 1 | MIG-01..03 đạt, scope owner Q-06 xác định | Quyết định routing switch, drain và active writer ownership theo strategy đã chốt | Abort nếu thiếu parity/data/recovery evidence hoặc thresholds chưa chốt |
| 2 | Quyền thay traffic đã được cấp riêng, thresholds Q-07 đã chốt | Thực hiện switch ở nhiệm vụ triển khai tương lai; theo dõi consumer/probe/business/data signals | Abort nếu vượt ngưỡng đã chốt; current ready/200 không đủ chứng minh counter khỏe |
| 3 | Nếu có regression, rollback authority đã xác định | Chỉ switch về old runtime khi old reader/writer tương thích mọi post-cutover writes | Không tương thích → dừng theo recovery plan, reconcile/forward recovery đã diễn tập; không chỉ image revert |
| 4 | Observation window và approval đã có evidence | Xác nhận ổn định và quyết định retire old service riêng | Chưa có observation/sign-off thì không retire |

Hiện cả thresholds, observation duration, rollback time/data-loss limit, routing commands, source/target artifacts và authority đều TBD. Vì vậy bảng chỉ kiểm tra logic gates; chưa có đủ thông tin để chạy migration an toàn hay đầy đủ.

Evidence/A/Q canonical tại [registry](../evidence-register.md). Risks: nhầm Next với Express (C-01), ready báo 200 nhưng counter có thể lỗi (C-02), durability chưa chứng minh (C-05). Resolve Q-04/Q-06 trước source-specific readiness, Q-02/Q-05 trước data parity, Q-07 trước performance gates. Scope/requirements thay đổi phải được sửa tại BRD/FRD/API/Data/Architecture canonical owners, không lén đổi khi migrate.

## Validation và readiness

**Plan completeness: BLOCKED. Implementation/parity evidence: BLOCKED. Cutover readiness: BLOCKED.** Hành vi Skill xử lý thiếu đầu vào được chấm riêng; không gọi partial plan này hoàn chỉnh hoặc tested.

| Finding | Check / severity | Locations + versions / IDs | Expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|---|
| VAL-16 | Source/target identity / blocker | README, E-03..07, Q-04/Q-06 | Express source/target intent/authority chưa xác minh | Không thể executable-ready | Cung cấp source/ref/target decision / Web + nhóm | BLOCKED |
| VAL-17 | Baseline scope/parity / major | Năm upstream0.1.0, matrix trên | Draft có trace/gaps, chưa accepted hoặc runtime tested | Không đủ migration acceptance | Baseline characterization và contract tests / QA | BLOCKED |
| VAL-18 | Data rollback / blocker | ENT-03/NFR-02/MIG-03/04 | Chưa có compatibility/recovery evidence sau writes | Chặn cutover/retirement | Test restore/reconcile và threshold nguồn / Web + Platform | BLOCKED |
