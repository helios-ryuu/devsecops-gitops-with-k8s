# Traceability và cross-document review

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| TEST-TRACE | 0.1.0 | draft | 2026-11-05 | Codex review; Web/QA/Platform resolve | Sáu smoke outputs, evidence register | TEST-BRD/FRD/API/ARCH/DATA/MIG đều 0.1.0 |

Change log 0.1.0: follow-up sau đủ sáu steps. Review ở đây là tự review có hướng dẫn trong cùng phiên, không reviewer độc lập. Mọi requirement commitment là proposed; document status draft. Trace không làm các scope trở thành accepted.

## Business → behavior → API → data

| BR | FR | Interaction | Operations | Entity | Gap / non-software reason | Commitment |
|---|---|---|---|---|---|---|
| BR-01 | FR-01 | UI/data-source chưa chốt | NONE | ENT-03 candidate | Q-02/Q-04/Q-05; chưa định nghĩa counter hoặc business API | proposed |
| BR-02 | FR-02 | HTTP operational | getHealth | ENT-01 transient | None cho code-aligned response slice; access/runtime chưa test Q-04 | proposed |
| BR-02 | FR-03 | HTTP operational | getReadiness | ENT-02 transient | Q-03 target semantics; current contract không Redis-ready | proposed |
| BR-02 | FR-04 | HTTP intended, contract thiếu | NONE | NONE | Q-04/Q-07; metrics chưa có definitions/implementation | proposed |
| BR-03 | NONE | Non-software outcome | NONE | NONE | Log/ảnh/nghiệm thu do nhóm thực hiện, không tạo HTTP FR giả | proposed |

FRD canonical owns FR/RULE/AC; API canonical owns wire; Data canonical maps fields và lifecycle. BR-01/02 đều được FR trace nhưng **full behavioral coverage vẫn BLOCKED**. Matching IDs không đủ để nói đầy đủ nghiệp vụ. BR-03 không phải orphan BR vì có non-software disposition rõ.

| Check / severity | Actual content comparison, không chỉ IDs | Result / evidence | Correction / owner |
|---|---|---|---|
| Parent/scope / major | FR-01 về hiển thị lượt xem đúng BR-01; FR-02/03/04 hỗ trợ quan sát BR-02; không có FR logistics/analytics vô nguồn; proposed giữ xuyên chain | PASS trong slice; BRD/FRD/trace rows | Scope authority trước accepted / Q-01 |
| FR-operation coverage / major | getHealth/getReadiness link FR-02/03; FR-01 counter và FR-04 metrics thiếu operation được ghi rõ, không fabricate full contract | PASS declared slice; BLOCKED full API | Q-02/Q-04/Q-07 / Web + QA |
| Types/required/null/enums/time / major | health.status=ok; uptime number giây; ready.status=ready; timestamps UTC ISO. Không response 503 Redis hoặc null fallback ở code; Data giữ nguyên canonical wire sources | PASS code/static slice; HTTP runtime BLOCKED | Web/QA contract tests sau review |
| Access/errors / major | Không auth check ở handlers ≠ approved public access; không có error envelope được code định nghĩa; proxy/framework errors unknown | BLOCKED full security/error contract, không bịa statuses | Q-04 / Web + Platform |
| Field/source/lifecycle / major | API có 3 HealthReport fields, 2 ReadinessReport fields; mỗi field map nguồn transient đúng handler; không lưu reports ở Redis | PASS slice; API/Data 0.1.0 và source | Không áp field map này cho counter chưa có schema |
| Concurrency/retention/recovery / major | Counter definition/key/TTL/retry/ownership chưa có; cả FRD/Data/Architecture/Migration cùng BLOCKED, không tài liệu nào âm thầm đặt no expiry | BLOCKED; RULE-01/ENT-03/NFR-02/CTL-02/MIG-03 | Q-02/Q-05 / Web + Platform |
| NFR realization / major | NFR-01 config hardening có source; NFR-04 namespace discrepancy có offline render; performance/recovery controls chỉ proposed với gaps | PASS về reporting controls/gaps; BLOCKED về NFR achievement; C-04 source agreement FAIL | Q-05/Q-07 và live tests / Platform + QA |
| Migration invariants / blocker | Next probes không bị đổi nhãn thành Express; target chưa chốt; parity chưa chạy; post-cutover writes và unsafe rollback được đặt gate | PASS về xử lý thiếu evidence; plan completeness/cutover BLOCKED | Q-04/Q-06 / Web + Platform |
| Version/evidence / major | Sáu drafts 0.1.0, source pin giữ nguyên, không lấy dirty bundle notes hoặc fixture làm target requirements; artifacts/log hash có capture | PASS structural checks; không có approval | Reviewer xác nhận nguồn/rules trước official docs |

Nguồn còn contradictions C-01/C-04/C-06/C-07; sandbox không che hoặc sửa README/WBS. C-02/C-03/C-05 là giới hạn functional/storage evidence. C-08 status tương lai chưa có bằng chứng độc lập. Chi tiết severity, locations, impact và owner tại [registry](evidence-register.md).

## Change propagation cases

Nếu Q-03 quyết định `/ready` phải check Redis và trả failure response: sửa RULE-03/AC-05/06 tại FRD, định nghĩa status/schema tại API, dependency/failure control tại Architecture, xác định Data access nếu cần, rồi cập nhật migration parity và consumer/probe tests. Không tự áp thay đổi này từ template migration.

Nếu Q-02/Q-05 chốt counter cần durability: FRD sở hữu definition/expected failures, API sở hữu representation/operations, Data sở hữu keys/TTL/concurrency/recovery, Architecture giải thích control/trade-off. Re-run affected checks thay vì chỉ thêm IDs. Đổi persistence/TTL sau cutover phải kiểm tra old/new writers và rollback boundary.

Nếu backend Express nằm ở ref khác: pin source riêng rồi inventory, giữ Next UI/probes hiện tại đúng vị trí cho đến khi có quyết định chuyển ownership. Không coi README dùng từ “2 tầng” là bằng chứng chỉ có hai processes hoặc Next thay backend.

## Unchecked scope

Không có độc lập fresh-session invocation/blind routing eval, full OpenAPI-aware validator, rendered Mermaid, app HTTP/Redis integration/load tests, live K3s/NetworkPolicy/ArgoCD hoặc target-runtime parity. Các phần này là BLOCKED/chưa chạy, không lấy checker bundle/document hay diagram source làm PASS. [Document checks](document-checks.json) chỉ xác nhận những điều kiện được mô tả trong script.
