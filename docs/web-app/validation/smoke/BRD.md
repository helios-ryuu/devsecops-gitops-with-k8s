# BRD thử nghiệm — Web demo NT548

> SANDBOX. Lát cắt kiểm thử `brd-authoring`, không thay BRD chính thức.

| Document ID | Version | Status | Date | Owner role | Sources | Upstream versions |
|---|---|---|---|---|---|---|
| TEST-BRD | 0.1.0 | draft | 2026-11-05 | Web Fullstack Dev / Documentation; authority TBD Q-01 | E-01, E-02, E-03..E-11; yêu cầu test hiện tại | Project `2110edd`; shared standard 1.0.0 |

Change log 0.1.0: tạo draft ban đầu; BR-01..BR-03 là proposed, không có dấu xác nhận accepted. [Nguồn và questions](../evidence-register.md) là registry chung cho cả sandbox.

## Context và vấn đề

README §2 và WBS 3.3/4.2/4.3/4.4 mô tả nhóm sinh viên cần một ứng dụng demo để kiểm chứng luồng triển khai, quan sát và nghiệm thu đồ án. Vấn đề có bằng chứng trực tiếp trong snapshot là khoảng cách giữa khả năng web được mô tả và code hiện có: trang chính còn starter; probes có handler; bộ đếm/metrics chưa có implementation quan sát được (E-03..E-06). Điều này để lại phần kiểm chứng demo chưa được chứng minh. Chưa có bằng chứng định lượng về thời gian tiết kiệm, tỷ lệ lỗi hoặc ảnh hưởng người dùng ngoài nhóm; không giả định đang có sự cố production.

Workflow mong muốn theo nguồn: thành viên phát triển web → nhóm triển khai và quan sát → QA thu thập kết quả → nhóm trình bày minh chứng nghiệm thu. Workflow hiện tại chỉ được nguồn mô tả; không có phiên chạy/biên bản nghiệm thu trong lượt test. Stack là ràng buộc/giải pháp được tài liệu nêu, không phải lý do kinh doanh độc lập.

## Mục tiêu và thành công

| Goal | Vấn đề / source | Success evidence | Baseline | Target / conditions | Verification / owner |
|---|---|---|---|---|---|
| G-01 | Demo quan sát được khả năng web theo WBS 3.3 | QA ghi nhận giao diện và hành vi lượt xem theo định nghĩa đã chốt | Starter code quan sát được, chưa chạy | Quy tắc lượt xem TBD Q-02; không đặt KPI tự ý | QA + Web Dev, test sau khi chốt scope |
| G-02 | Nhóm cần phân biệt app hoạt động, đủ điều kiện phục vụ và có dữ liệu quan sát, README §2.2/§7 | Bộ test operational và số liệu được thu thập | Hai probes code-observed, metrics chưa thấy | Ngưỡng tải/freshness/ready criteria TBD Q-03/Q-07 | QA/Observability + Platform |
| G-03 | WBS 4.4/5.1 yêu cầu minh chứng cho demo/báo cáo | Log/ảnh/biên bản chỉ ra bước nào thực sự đã kiểm tra | Không kiểm chứng hiện trạng chạy trong lượt này | Deadline nguồn: nghiệm thu 05/12/2026; không phải cam kết mới | Documentation + nhóm; quyền nghiệm thu Q-01 |

## Stakeholders và authority

| Role | Interest / responsibility | Source | Acceptance authority |
|---|---|---|---|
| Web Fullstack Dev (Phúc) | Web demo và tích hợp ứng dụng | README §1.2; WBS phân công | TBD Q-01 |
| Platform & DevOps Lead (Sỹ) | Delivery, vận hành và cấu hình hạ tầng | Cùng nguồn | TBD Q-01 |
| QA & Observability (Huy) | Test và minh chứng quan sát | Cùng nguồn | TBD Q-01 |
| Documentation & Demo (Long) | Báo cáo và demo nghiệm thu | Cùng nguồn | TBD Q-01 |
| Người đánh giá học phần | Vai trò suy ra từ nghiệm thu; danh tính/quyền cụ thể chưa có rubric | Assumption A-01, source WBS 5.3 | Chưa xác minh, không gán approval |

## Scope và constraints

| Item | Scope class / release | Commitment | Authority/source | Dependency |
|---|---|---|---|---|
| Counter UI và health/ready/metrics phục vụ demo | Source-stated project scope; sandbox chỉ đề xuất lát cắt | proposed | README; WBS 3.3/2.4/4.2 | Q-02..Q-05 |
| Thu thập minh chứng demo | Source-stated project scope, kết quả ngoài phần mềm | proposed trong sandbox | WBS 4.4/5.1 | Runtime testing chưa chạy |
| Deadline nghiệm thu 05/12/2026 | Source-stated project constraint; chưa có rubric bên ngoài | proposed interpretation | README §6; WBS phần đầu | Q-01; lịch không chứng minh hoàn thành |
| Next.js frontend; Express Backend/API; Redis | Constraint/solution intent, không biến thành BR | Chưa chốt topology trong sandbox | E-01/E-02 khác cách mô tả; E-03..E-11 quan sát snapshot | Q-04 |
| Hạ tầng GitOps/security tổng thể | Ngoài lát cắt smoke; tiếp tục thuộc đồ án theo README | deferred coverage trong test | README §2 | Không viết đặc tả hạ tầng chính thức |
| AI office, agent execution, SSE, auth nghiệp vụ, Laravel migration | Excluded khỏi release scope của smoke | Không tạo commitment | Không có đầu vào được phê duyệt cho lượt này | Migration chỉ đánh giá gaps |

Chưa có nguồn độc lập cho yêu cầu bắt buộc của môn học, pháp lý hoặc SLA. Không gắn nhãn mandatory external obligation từ README của nhóm.

## Business requirements

| BR ID | Need / outcome | Rationale / goal | Source | Priority | Scope class / release | Commitment | Business success evidence | Implementation |
|---|---|---|---|---|---|---|---|---|
| BR-01 | Nhóm có thể trình diễn khả năng theo dõi lượt truy cập trên web | G-01; làm khả năng demo quan sát được | E-01 §1.2; E-02 3.3, source-stated | proposed high | Project scope nêu ở nguồn; smoke slice | proposed | QA đối chiếu lượt hiển thị với kịch bản đã thống nhất Q-02 | Planned; E-04 chỉ có starter UI |
| BR-02 | Nhóm vận hành/QA đánh giá được trạng thái phục vụ và quan sát hoạt động web | G-02; hỗ trợ demo/đo kiểm | E-01 §2.2/§7; E-02 2.4/4.2/4.3 | proposed high | Cùng phạm vi nguồn; smoke slice | proposed | Bộ test trạng thái và dữ liệu quan sát có nguồn/điều kiện rõ | Hai probes code-observed; dependency-aware ready/metrics chưa được chứng minh |
| BR-03 | Nhóm có minh chứng tái kiểm tra được cho báo cáo và nghiệm thu | G-03; tránh dựa vào tuyên bố chưa kiểm chứng | E-02 4.4/5.1 | proposed high | Non-software project outcome | proposed | Log/ảnh gắn commit, kịch bản, kết quả thực tế | Unknown; không chạy demo ở đây |

Các hàng là Fact về ý định nguồn + đề xuất diễn giải BR; provenance source-stated, không phải tested. Không có requirement nào được accepted bởi việc tạo tài liệu thử nghiệm.

## Chất lượng, alternatives và risks

Kỳ vọng chất lượng từ README: chạy non-root, giới hạn truy cập Redis và hỗ trợ quan sát. FRD sẽ refine thành NFR; durability/performance targets chưa có nguồn (Q-05/Q-07). Hai cách tiếp cận demo: giữ web đơn giản như mô tả để kiểm chứng delivery, hoặc mở rộng nghiệp vụ. Lát cắt này dùng cách thứ nhất (Decision ADR-01 proposed, canonical tại Architecture) vì source hiện tại chỉ hỗ trợ mức đó; không dùng lựa chọn này để bác bỏ roadmap chưa được cung cấp.

Risks: mô tả stack không đồng nhất (C-01); readiness bị hiểu nhầm là Redis-ready (C-02); dữ liệu Redis có thể mất khi thay pod do chưa cấu hình volume trong manifest được đọc (C-05). Đây là rủi ro suy ra từ source, không phải outage đã đo. Owner giải quyết tương ứng: Web/Platform; Web/QA; Web/Platform. Không có baseline định lượng để đặt tỷ lệ lợi ích.

Evidence: E-01..E-11 code/source/config, E-12 runtime skill catalog. Assumptions: A-01/A-02; Questions: Q-01..Q-07, ghi đủ tác động và resolution role tại registry chung. Không coi notes/PR chưa merge ở repository khác là authority của main.

## Traceability và validation

| BR | FRD 0.1.0 coverage | Ngoài phần mềm / gap | Downstream |
|---|---|---|---|
| BR-01 | FR-01 | Counter semantics/API/storage chưa chốt | API/Architecture/Data 0.1.0; Q-02/Q-05 |
| BR-02 | FR-02, FR-03, FR-04 | Probes mô tả code, metrics chỉ gap | Cùng versions 0.1.0 |
| BR-03 | N/A có lý do | Log/ảnh/nghiệm thu là outcome nhóm; không bịa FR | Migration parity/readiness cần evidence, không thay báo cáo môn học |

Khi tạo BRD đầu tiên, kiểm tra downstream còn BLOCKED vì chưa có tài liệu. Bảng trên là follow-up sau sáu bước, cùng phiên bản initial draft 0.1.0; không ghi là đã có upstream khi chưa tạo. [Execution log](../execution-log.json) ghi đúng thứ tự.

| Finding | Check / severity | Locations + IDs | Expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|---|
| VAL-01 | Need khác solution / major | BR-01..03 | BR là outcome; stack chỉ constraint | Tránh technical choice thành business need | Giữ cách tách / BA reviewer | PASS trong smoke |
| VAL-02 | Authority/rubric / major | Q-01; BRD control | Không có approved scope/rubric | Chưa baseline-ready | Nhóm cung cấp nguồn / scope owner TBD | BLOCKED |
| VAL-03 | Coverage / major | BRD/FRD/API/Data 0.1.0 | BR-01 còn gaps rõ; BR-03 có non-software reason | Không đủ bộ chức năng hoàn chỉnh | Resolve Q-02/Q-05 / Web Dev | BLOCKED về full coverage; trace slice được kiểm tra riêng |
