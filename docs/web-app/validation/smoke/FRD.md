# FRD thử nghiệm — Web demo NT548

> SANDBOX. Áp dụng `frd-authoring` trên BRD thử nghiệm; chưa là functional baseline.

| Document ID | Version | Status | Date | Owner role | Sources | Upstream versions |
|---|---|---|---|---|---|---|
| TEST-FRD | 0.1.0 | draft | 2026-11-05 | Web Dev / QA; approval TBD Q-01 | E-01..E-11; [registry](../evidence-register.md) | TEST-BRD 0.1.0 |

Change log 0.1.0: tạo FR-01..04, RULE-01..04, AC-01..08, NFR-01..04. Mọi scope/commitment trong draft là proposed, kể cả khi code-observed. Không nâng BR proposed thành FR accepted.

## Actors, boundary, flows

| Actor | Parent BR / goal | Allowed actions / nguồn access | Boundary |
|---|---|---|---|
| Người mở web demo | BR-01, xem thông tin lượt truy cập | Chưa có chính sách user/auth được chốt Q-04 | UI; không giả định danh tính/unique visitor |
| Kubelet / nhóm kiểm tra vận hành | BR-02, quan sát probes | Deployment khai báo probes; không thấy auth check ở hai handlers; public exposure chưa được duyệt | HTTP operational |
| QA/Observability | BR-02/03, thu thập bằng chứng | Phân công README/WBS, không suy ra quyền quản trị cluster | Kiểm tra/ghi kết quả |

Luồng counter dự kiến: mở web → hệ thống lấy số liệu theo quy tắc Q-02 → hiển thị. Khi dữ liệu thiếu/Redis lỗi/requests đồng thời, hành vi còn TBD, không tự hiển thị 0 hoặc tự tăng số. Chưa đủ pre/postconditions để baseline counter. Probe hiện có: nhận GET → sinh giá trị tại handler → trả JSON 200; không thay dữ liệu nghiệp vụ. Process không nhận request được thì handler không có phản hồi; không biến tình huống đó thành JSON error do app phát ra.

## Functional requirements

### FR-01 — Hiển thị lượt truy cập

- Parent: BR-01. Actor/trigger: người mở trang web demo. Precondition: nguồn số liệu/định nghĩa lượt xem phải được chốt Q-02/Q-05.
- Inputs: hành vi truy cập; identity/dedup/retry semantics TBD. Output: lượt truy cập hiển thị theo định nghĩa đã chốt; chưa cam kết type/initial value.
- Alternate/failure/concurrency: thiếu dữ liệu, Redis mất kết nối, refresh, nhiều request và retry đều cần quyết định Q-02/Q-05. Không suy “exactly once” từ Redis.
- RULE-01; AC-01/02. Interaction: UI với data source chưa xác định; HTTP operation gap Q-02/Q-04, không tạo `/visits` hoặc GET-mutates-counter. Chưa có thao tác người dùng chỉnh/reset counter.
- Priority proposed high; source-stated project scope, smoke slice; commitment proposed. E-01/E-02 là intent, E-04 là starter UI. Implementation planned/unverified.

### FR-02 — Phản hồi health của tiến trình

- Parent: BR-02. Actor/trigger: operational caller gửi GET `/healthz`; precondition request tới được handler.
- Inputs: không có business body/path/query parameters được handler đọc. Code không validate query/body lạ; không hứa trả 400 khi chưa có code.
- Output: HTTP 200 JSON theo `getHealth` trong API 0.1.0; dữ liệu transient, không truy cập Redis. Uptime là thời gian sống tiến trình, không phải thời gian sẵn sàng toàn hệ thống.
- Access: không có auth check trong handler; chính sách expose/ingress TBD Q-04. Failure/denied-access ở proxy hoặc framework nằm ngoài lát cắt response contract, chưa kiểm thử. Concurrent reads không cập nhật counter.
- RULE-02; AC-03/04; interaction HTTP `getHealth`. Priority proposed high; same project scope/proposed commitment. E-05/E-08 code/config-observed; chưa runtime-tested.

### FR-03 — Phản hồi ready theo handler hiện tại

- Parent: BR-02. Actor/trigger: operational caller GET `/ready`; precondition request tới được handler.
- Inputs: không business params/body được đọc; output HTTP 200 JSON theo `getReadiness` API 0.1.0.
- Current behavior: trả ready mà không kiểm tra Redis hoặc nguồn counter. Desired dependency-aware readiness là question Q-03, không thay current contract thành 503.
- Access/failure/concurrency: cùng giới hạn nguồn như FR-02; Redis down vẫn không có nhánh failure trong handler. Không bảo đảm HTTP call thật thành công khi process/proxy đang lỗi.
- RULE-03; AC-05/06; HTTP `getReadiness`. Priority proposed high; project scope/proposed. E-06/E-08 code/config-observed; chưa runtime-tested.

### FR-04 — Cung cấp dữ liệu quan sát hoạt động web

- Parent: BR-02. Actor/trigger: hệ thống scrape/QA quan sát theo kế hoạch README. Precondition: metric definitions, quyền truy cập, transport/owner phải được chốt Q-04/Q-07.
- Output dự kiến: metrics phục vụ theo dõi HTTP hoạt động; danh sách metric names/labels/types/retention chưa có nguồn. Source nêu `/metrics` và prom-client, không chứng minh implementation.
- Failure/concurrency: scrape lỗi/mất mẫu/cardinality/retention TBD; không coi thiếu metric là zero traffic. Không đề xuất SSE vì không có yêu cầu live UI stream.
- RULE-04; AC-07/08. HTTP intended `/metrics`, operation gap, chưa có `operationId` trong API thử nghiệm.
- Priority proposed high; source-stated scope/proposed. E-01 L53/L76, E-02 4.2/4.3; implementation planned/unverified E-03.

## Canonical rules và transitions

| RULE ID | Canonical rule | Source / parent | FRs | Status |
|---|---|---|---|---|
| RULE-01 | Định nghĩa lượt xem, ghi nhận/retry/concurrency/reset TBD Q-02/Q-05; không đặt rule thay nguồn | E-01/E-02; BR-01 | FR-01 | proposed, BLOCKED |
| RULE-02 | Health phản ánh process: status ok, uptime process, timestamp lúc handler tạo response; không phụ thuộc counter | E-05; BR-02 | FR-02 | code-observed, proposed contract |
| RULE-03 | Ready hiện tại không có dependency check; target rule cần Q-03 | E-06; BR-02 | FR-03 | code-observed; target BLOCKED |
| RULE-04 | Metric definitions/labels/access/failure handling TBD Q-04/Q-07 | E-01; BR-02 | FR-04 | planned, BLOCKED |

Probe reports không phải entity có trạng thái lưu, nên không có transition pending→ready hoặc persisted state machine. Counter transitions/guards và forbidden concurrent outcomes chưa xác định Q-02/Q-05; ghi BLOCKED thay vì tự bịa state model.

## Acceptance criteria

| AC ID | FR / RULE | Given | When | Then / observable result | Case / readiness |
|---|---|---|---|---|---|
| AC-01 | FR-01 / RULE-01 | Quy tắc Q-02/Q-05 đã chốt, nguồn số liệu xác định | Mở trang | Giá trị UI khớp nguồn và định nghĩa đã chốt | Success; BLOCKED đến khi có expected value |
| AC-02 | FR-01 / RULE-01 | Có simultaneous visits, retry hoặc nguồn dữ liệu lỗi | Chạy kịch bản được chốt | Kết quả theo rule đã được chốt; không có expected behavior được bịa ở đây | Boundary/failure; BLOCKED |
| AC-03 | FR-02 / RULE-02 | Handler nhận request, process sống | GET health | 200 JSON, status ok, uptime number không âm, timestamp UTC date-time | Success; specification/code-reviewed, not run |
| AC-04 | FR-02 / RULE-02 | Dependency counter không truy cập được, handler vẫn chạy | GET health | Không có Redis read hoặc branch lỗi Redis trong code; contract health không khẳng định Redis khỏe | Dependency boundary; chưa test fault injection |
| AC-05 | FR-03 / RULE-03 | Handler nhận request | GET ready | 200 JSON status ready và timestamp UTC date-time | Success current snapshot; not run |
| AC-06 | FR-03 / RULE-03 | Redis unavailable nhưng handler vẫn nhận request | GET ready | Current code vẫn tạo response ready/200; desired 503 là Q-03, không là baseline | Failure boundary code review; not run |
| AC-07 | FR-04 / RULE-04 | Metric definitions và owner đã chốt | Scrape theo protocol | Payload đáp ứng definitions/conditions Q-07 | Success; BLOCKED |
| AC-08 | FR-04 / RULE-04 | Scrape không thành công | Thu thập/report | Cách biểu thị lỗi/missing-data cần chốt, không tự báo zero | Failure; BLOCKED |

AC-04/06 là nhận định control-flow ở code được pin, chưa phải kết quả runtime. Các AC còn TBD được giữ visible để review, không được coi là bộ acceptance test đầy đủ.

## Non-functional requirements

| NFR ID | BR / constraint source | Attribute | Metric / target | Conditions | Verification | Commitment / question |
|---|---|---|---|---|---|---|
| NFR-01 | BR-02; README runtime security; E-07/E-08 | Least privilege | Config app UID/GID 10001, non-root, drop ALL trong Pod | Next app container đã cấu hình; chưa kết luận Express runtime | Read config + runtime id/Pod security evidence sau review | proposed; config-observed, runtime BLOCKED |
| NFR-02 | BR-01/02; data dependency derived concern | Integrity/recovery | Consistency, loss bound, reset, RPO/RTO TBD Q-02/Q-05 | Counter + Redis khi implementation tồn tại | Concurrent/restart/recovery tests sau decisions | proposed, chưa có target nguồn; BLOCKED |
| NFR-03 | BR-02; WBS 4.2/4.3 | Performance/observability | Load, latency/error-rate targets, window TBD Q-07 | Môi trường/traffic dataset cần ghi | QA load + scrape evidence, không chạy ở đây | proposed, BLOCKED |
| NFR-04 | BR-02; README namespace isolation E-01, config E-10 | Network access boundary | Source intent chỉ Web được vào Redis TCP6379; canonical namespace target còn C-04 | Policy trong namespace thực tế; label không là identity/auth nghiệp vụ | Offline render + policy review; live allow/deny tests sau review | proposed; config observed, intended cross-namespace claim FAIL |

## Traceability, evidence và validation

| BR | FR / RULE / AC | API operationIds / gap | Data entity | Architecture control |
|---|---|---|---|---|
| BR-01 | FR-01 / RULE-01 / AC-01,02 | UI/data gap Q-02/Q-04 | ENT-03 candidate, storage TBD | CTL-02 proposed |
| BR-02 | FR-02 / RULE-02 / AC-03,04 | getHealth | ENT-01 transient | CTL-01/03 |
| BR-02 | FR-03 / RULE-03 / AC-05,06 | getReadiness | ENT-02 transient | CTL-01/03 |
| BR-02 | FR-04 / RULE-04 / AC-07,08 | /metrics intended, no contract operation Q-04/Q-07 | N/A metric model missing, Q-07 | CTL-04 proposed |
| BR-03 | N/A | Non-software evidence collection; không tạo HTTP FR | N/A | N/A |

Evidence/A/Q/C canonical tại [registry](../evidence-register.md). A-02 giới hạn slice; Q-02/Q-05 chặn counter; C-02 chặn suy diễn ready; C-04 là source/config inconsistency. Risk: tiêu chí còn TBD không thể nghiệm thu, owner Web/QA/nhóm scope.

| Finding | Check / severity | Locations + versions | Expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|---|
| VAL-04 | Parent/scope/commitment / major | BRD/FRD 0.1.0, BR-01/02→FR-01..04 | Không orphan; proposed được giữ | Không tạo approved scope giả | Review semantic links / BA | PASS cho slice |
| VAL-05 | Acceptance completeness / major | AC-01/02/07/08; Q-02/Q-05/Q-07 | Expected values còn TBD | Chưa testable toàn bộ | Chốt rules/targets / Web + QA | BLOCKED |
| VAL-06 | Contract agreement / major | FR-02/03, API/Data 0.1.0 | Hai probes khớp current code; metrics/counter gaps explicit | Full HTTP/data coverage chưa đủ | Hoàn thiện sau Q resolution / Web | PASS probe slice; BLOCKED full coverage |
