# BRD — AI Agent Office Monitor

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| PT-BRD | 0.1.0 | DRAFT | 2026-11-05 | Web Fullstack Dev; authority nghiệm thu TBD | E-100..E-108 trong [report](evaluation-report.md) | Yêu cầu practical evaluation của người dùng; shared standard 1.0.0 |

Change log 0.1.0: tạo bộ thử nghiệm độc lập; không thay smoke/validation trước đó. IDs bắt đầu từ 100 để không tái sử dụng IDs của bài test cũ. Toàn bộ diễn giải mới là proposed; “mandatory” là nghĩa vụ do người dùng cung cấp, chưa được đối chiếu rubric học phần.

## Context và business problem

Người dùng cần một giao diện tập trung để quan sát agents, tasks và các sự kiện liên quan (E-100, user-provided). Hiện chưa có bằng chứng về quy trình theo dõi thực tế, số lượng người dùng, thời gian mất khi đọc logs hoặc tổn thất định lượng. Không khẳng định nhóm đang vận hành AI agents thật. Vấn đề là khả năng hiểu và trình bày trạng thái công việc; văn phòng 3D là một phương án thể hiện, không phải nguyên nhân nghiệp vụ.

Đồng thời nhóm cần một Web App có hành vi quan sát được để tích hợp và trình diễn đồ án NT548: lượt truy cập, khả năng phục vụ và số liệu ứng dụng. README/WBS nêu trách nhiệm Web Fullstack; source hiện tại chỉ có starter UI và hai probe handlers (E-101..E-104). Khoảng cách giữa dự kiến và source quan sát được là finding, chưa phải bằng chứng về lỗi production.

Workflow dự kiến: người trình diễn mở web → quan sát khả năng ứng dụng → QA kiểm tra kết quả và cung cấp minh chứng. Nếu extension được chọn, simulator cung cấp hoạt động tổng hợp để người xem hiểu agent/task state; không có việc giao task cho một AI thật.

## Goals và business success

| Goal | Nhu cầu / source | Success evidence | Baseline | Target / conditions | Owner |
|---|---|---|---|---|---|
| G-100 | Trình diễn Web App phù hợp phần việc NT548, E-100/E-101 | UI, counter và kết quả operational tests gắn commit | Starter UI, hai probes code-observed | Mandatory behaviors được kiểm chứng; định nghĩa visit Q-101 | Web Dev + QA |
| G-101 | Hiểu trạng thái công việc mô phỏng, E-100 | Demo chỉ rõ agent nào làm task nào và kết quả gì | Chưa có dashboard/simulator | Conditional MVP; thang đo hiểu đúng và đối tượng đánh giá TBD Q-100/Q-104 | Web owner |
| G-102 | Giữ khối lượng phù hợp thời gian đồ án, E-100/E-102 | Scope checklist và quyết định chọn/bỏ extension | WBS nêu hạn 05/12/2026; không kiểm chứng tiến độ thực tế | Mandatory trước; extension chỉ sau quyết định | Web owner + Platform Lead |

Không đặt KPI giảm thời gian hoặc SLA không có baseline. Hoàn tất tài liệu DRAFT không chứng minh đạt các goals.

## Stakeholders và scope authority

| Role | Interest / responsibility | Source | Authority |
|---|---|---|---|
| Web Fullstack Dev — Trần Hồng Phúc | UI, business logic, Redis, integration ứng dụng | README §1.2; WBS phân công | Người dùng cung cấp intent; quyền baseline/acceptance TBD Q-100 |
| Platform Lead — Ngô Tiến Sỹ | Contracts với container, ingress, probes, scrape | Cùng nguồn | Phối hợp integration; không mặc định duyệt sản phẩm |
| QA/Observability — Điền Quốc Huy | Test hành vi và thu thập số liệu | Cùng nguồn | Chứng minh kết quả, chưa có sign-off matrix |
| Documentation/Demo — Đặng Thế Long | Minh chứng báo cáo và demo | Cùng nguồn | Không tự đổi scope Web App |
| Người xem demo / người đánh giá | Hiểu trạng thái được trình bày | E-100; danh tính chi tiết chưa có | TBD Q-100; không bịa quyền quản trị |

## Scope và constraints

| Class | Nội dung | Commitment | Implementation / dependency |
|---|---|---|---|
| Mandatory | Web interface; Redis visitor counter; liveness; readiness; Prometheus-compatible application metrics; container integration | Requested obligation theo E-100; tài liệu vẫn DRAFT | UI/probes code-observed; counter/metrics planned; Docker configured |
| Proposed MVP Extension | Dashboard agents/tasks; bốn agent states; simulator; office 3D với 2–3 chibi; state-animation mapping; recent activity | Proposed, chưa có quyết định chọn release Q-100 | Chưa thấy code; [FRD](02-FRD.md) mô tả conditional behavior |
| Optional | SSE; 2D fallback; event history/filtering | Deferred khỏi candidate MVP hiện tại | Không tự sinh endpoints, retention hay realtime guarantees |
| Future | Real agent execution; Codex/Claude/Gemini sessions; auth/multi-user; Express → Laravel | Deferred | Không thuộc nghiệm thu NT548; migration chỉ feasibility |
| External | K3s, Tailscale, Traefik, ArgoCD, GitHub Actions, NetworkPolicy, monitoring platform, load reports | Integration constraints | Owner ngoài Web App; không đặc tả/rebuild hạ tầng |

Next.js 16, Node/Express dự kiến, Redis, Three.js, Docker là technology constraints/proposals. README nêu Express/Node 24; WBS và source là Next.js, Docker base Node 26.13.0. Giữ cả hai nguồn, không hợp thức hóa Express thành implemented (C-100). My Office chỉ là design evidence E-108, không phải business requirement.

## Business requirements

| BR | Need / outcome | Rationale / source | Priority / class | Commitment | Business success evidence | Implementation |
|---|---|---|---|---|---|---|
| BR-100 | Người xem truy cập được giao diện demo Web App | G-100, E-100/E-102 | High / Mandatory | Requested; đặc tả proposed | QA mở giao diện với nội dung phù hợp release | Starter code-observed, chưa tested |
| BR-101 | Nhóm trình bày được lượng truy cập theo một định nghĩa thống nhất | G-100, E-100/E-101 | High / Mandatory | Requested; quy tắc visit TBD | Kịch bản visit và số hiển thị được đối chiếu | Planned, chưa Redis client |
| BR-102 | Nhóm vận hành phân biệt được app sống và đủ điều kiện phục vụ | G-100, E-100/E-101 | High / Mandatory | Requested; dependency semantics proposed | Probe cases bình thường/mất Redis/phục hồi có evidence | Handlers observed; readiness chưa dependency-aware |
| BR-103 | QA có số liệu hoạt động ứng dụng cho phần quan sát | G-100, E-100/E-101 | High / Mandatory | Requested; metric set proposed | Scrape/parser + traffic scenario có kết quả | Planned, chưa metrics route |
| BR-104 | Web App có thể bàn giao để đóng gói và tích hợp với nhóm | G-100/G-102, E-100/E-102 | High / Mandatory | Requested | Container/integration checklist được nhóm kiểm chứng | Docker/configured; chưa build/run trong test |
| BR-105 | Người xem hiểu trạng thái agents và tasks mô phỏng trong một nơi | G-101, E-100 | Medium / MVP extension | Proposed conditional | Dashboard và task kết quả khớp kịch bản simulator | Proposed |
| BR-106 | Người xem phân biệt hoạt động và sự kiện bằng hình ảnh văn phòng dễ theo dõi | G-101, E-100 | Medium / MVP extension | Proposed conditional | 2–3 nhân vật, state và recent activity nhất quán | Proposed |
| BR-107 | Theo dõi từ xa, xem lịch sử hoặc dùng thiết bị yếu khi có nhu cầu được xác nhận | E-100 Optional | Low / Optional | Deferred | TBD khi chọn enhancement | Unknown |
| BR-108 | Kết nối agent thật và mở rộng nền tảng về sau khi có lý do đầu tư | E-100 Future | Future | Deferred | Business case, quyền truy cập và parity gates sau này | Chưa có baseline migration |

## Quality expectations, alternatives và risks

Ứng dụng phải cung cấp trạng thái trung thực khi dependency lỗi (BR-101/102), dữ liệu mô phỏng phải được ghi nhãn (BR-105), và không đưa secrets/logs nhạy cảm vào demo (BR-104). FRD refine thành NFR-100..NFR-106. Performance, recovery, accessibility và đối tượng thiết bị chưa có thresholds; xem Q-104/Q-105.

Alternative tối thiểu: giữ counter web và operational endpoints để hoàn thành mandatory. Candidate extension: thêm simulator chỉ trong trình duyệt, không thêm backend mutations hay stream. Phương án simulator server + SSE chỉ xem lại khi cần chia sẻ state giữa nhiều clients; hiện làm tăng rủi ro consistency/scale mà chưa có nhu cầu chốt.

| Risk / dependency | Impact | Response / owner |
|---|---|---|
| Extension chiếm thời gian mandatory | Trượt kế hoạch nguồn | Gate mandatory trước; Web owner chọn scope Q-100 |
| Visit chưa định nghĩa | Counter/API/AC không thể baseline | Chốt đơn vị tính, refresh/bots/retries; Web owner Q-101 |
| Redis recovery chưa chốt | Hiểu sai total là bền vững | Phân biệt atomicity và durability, Q-103 Web + Platform |
| Reference rất rộng, coupling nhiều | Copy kéo theo CLI/credentials và nhiều dependencies | Chọn module qua matrix, audit license trước reuse |

## Facts, assumptions, decisions và questions

Facts: E-100 là intent người dùng; E-103/104 là code/config quan sát, không runtime test. A-100 (proposed): demo simulator ở browser đủ cho candidate MVP, không cần shared state. ADR-100..ADR-104 thuộc [Architecture](04-architecture.md). C-100..C-103 và Q-100..Q-108 được quản lý tại [Evaluation Report](evaluation-report.md); không dùng assumptions để đóng questions.

## Traceability và validation

| BR | Downstream coverage | Non-coverage reason |
|---|---|---|
| BR-100 | FR-100 | — |
| BR-101 | FR-101; Data ENT-100 | HTTP route/visit semantics BLOCKED Q-101 |
| BR-102 | FR-102/103; getLiveness/getReadiness | Readiness delta proposed |
| BR-103 | FR-104; getApplicationMetrics | Metric vocabulary cần duyệt Q-106 |
| BR-104 | FR-105; NFR-100/105 | Build/deploy ngoài bài docs-only |
| BR-105 | FR-106/107/108 | Conditional MVP, chưa selected |
| BR-106 | FR-109/110/111 | Conditional MVP, chưa selected |
| BR-107/108 | Không tạo FR active | Optional/Future deferred; migration feasibility không thêm FR |

Checked: nhu cầu trước stack, authority, scope và forward coverage tại v0.1.0. Unchecked: business outcomes thực tế và rubric độc lập.

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|
| VAL-100 | Business scope / major | BR-100..108 và FRD 0.1.0: optional/future giữ deferred | Tránh scope creep | Giữ gate Q-100 / Web owner | PASS nội dung |
| VAL-101 | Authority / blocker | BRD 0.1.0 Q-100: chưa có release decision/rubric | Chưa baseline | Xác nhận owner và release / người dùng | BLOCKED nghiệm thu |
