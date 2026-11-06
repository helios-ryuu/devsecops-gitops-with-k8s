# BRD — Mục tiêu và phạm vi AI Agent Office Monitor

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-BRD | 1.0.0 | review | 2026-11-06 | Web Fullstack Dev; quyền nghiệm thu yêu cầu theo Q-100 | E-100..E-108 tại [registry chung](README.md) | PT-BRD 0.1.0; yêu cầu chuyển sang Official được người dùng phê duyệt |

Change log 1.0.0: biên tập từ [BRD practical](../validation/practical-test/01-BRD.md); làm rõ mục tiêu, phạm vi và đường dẫn truy vết. Giữ G/BR IDs và ý nghĩa yêu cầu; không chọn thêm extension hoặc thay commitment. Quy ước trạng thái và registry Q/E/C/A ở [mục lục Official](README.md).

## 1. Vấn đề cần giải quyết

Người dùng cần một giao diện tập trung để hiểu agent nào đang làm task nào và kết quả công việc ra sao (E-100). Văn phòng 3D là một cách trình bày đề xuất để hỗ trợ việc quan sát; nhu cầu chính là hiểu trạng thái công việc. Chưa có bằng chứng về thời gian theo dõi hiện tại, số lượng người dùng, tổn thất định lượng hoặc việc nhóm đang vận hành AI agents thật. Vì vậy tài liệu không đưa ra KPI tiết kiệm thời gian hoặc lợi ích định lượng chưa có nguồn.

Song song với mục tiêu đó, nhóm cần Web App phục vụ đồ án NT548: giao diện truy cập được, bộ đếm lượt truy cập, probes và số liệu ứng dụng để tích hợp, kiểm tra và trình diễn. Phân công Web Fullstack nằm ở README/WBS (E-101/E-102). Source đã đọc mới cho thấy Next starter và hai probe handlers; bộ đếm, metrics và simulator chưa được chứng minh hoạt động. Đây là khoảng cách giữa ý định và code quan sát được, không phải bằng chứng sự cố production.

## 2. Kết quả mong muốn

| Goal | Nhu cầu / source | Bằng chứng thành công cần thu thập | Baseline và điều kiện | Owner |
|---|---|---|---|---|
| G-100 | Web App phù hợp phần việc NT548, E-100/E-101 | UI, counter và operational tests gắn với commit/kịch bản cụ thể | Starter UI và hai probes code-observed; định nghĩa visit Q-101 phải chốt | Web Dev + QA |
| G-101 | Người xem hiểu trạng thái agents/tasks mô phỏng, E-100 | Demo chỉ rõ agent, task và kết quả khớp kịch bản | Conditional MVP; chưa có dashboard/simulator; thang đo hiểu đúng và đối tượng đánh giá Q-100/Q-104 | Web owner |
| G-102 | Khối lượng phù hợp thời gian đồ án, E-100/E-102 | Scope checklist và quyết định chọn/bỏ extension | WBS nêu hạn 05/12/2026; không chứng minh tiến độ thực tế. Mandatory trước, extension sau quyết định | Web owner + Platform Lead |

Việc hoàn tất tài liệu không chứng minh đã đạt các goals. Performance/SLA chỉ được định nghĩa khi có baseline, điều kiện đo và authority phù hợp.

## 3. Người liên quan và trách nhiệm

| Role | Trách nhiệm / nhu cầu | Nguồn và quyền quyết định |
|---|---|---|
| Web Fullstack Dev — Trần Hồng Phúc | UI, business logic, Redis và application integration | E-101/E-102; cung cấp intent; baseline/acceptance authority Q-100 |
| Platform Lead — Ngô Tiến Sỹ | Container, ingress, probes và scrape integration | E-101/E-102; phối hợp integration, không mặc định phê duyệt sản phẩm |
| QA/Observability — Điền Quốc Huy | Test hành vi và thu thập số liệu | E-101/E-102; chứng minh kết quả; sign-off matrix chưa có |
| Documentation/Demo — Đặng Thế Long | Báo cáo, minh chứng và demo | E-101/E-102; không tự thay scope Web App |
| Người xem demo / người đánh giá | Hiểu trạng thái ứng dụng/công việc được trình bày | E-100; danh tính và authority cụ thể Q-100; không suy ra quyền quản trị |

## 4. Phạm vi và ràng buộc

| Scope class | Nội dung | Cam kết / điều kiện | Implementation theo nguồn |
|---|---|---|---|
| Mandatory | Web interface; Redis visitor counter; liveness/readiness; application metrics tương thích Prometheus; container integration | Requested obligation theo E-100. Cách đặc tả và các quyết định còn mở được ghi ở FRD/API/Data | UI/probes code-observed; Docker configured; counter/metrics planned |
| Proposed MVP Extension | Dashboard agents/tasks; bốn agent states; simulator; office 3D với 2–3 chibi; state-animation mapping; recent activity | Proposed, chỉ triển khai khi được chọn release Q-100 | Chưa thấy implementation |
| Optional | SSE, 2D fallback, event history/filtering | Deferred khỏi candidate MVP hiện tại; không tự sinh endpoint hoặc retention/realtime guarantee | Chưa selected |
| Future | Real agent execution; Codex/Claude/Gemini sessions; auth/multi-user; Express → Laravel | Deferred; không thuộc nghiệm thu NT548. Migration hiện chỉ feasibility | Chưa baseline migration |
| External | K3s, Tailscale, Traefik, ArgoCD, GitHub Actions, NetworkPolicy, monitoring platform và load reports | Ràng buộc tích hợp do các vai trò ngoài Web App sở hữu | Không đặc tả lại hoặc rebuild hạ tầng trong bộ yêu cầu Web |

Next.js 16, Node/Express dự kiến, Redis, Three.js và Docker là lựa chọn/ràng buộc giải pháp. README nêu Express/Node24, trong khi WBS/source thể hiện Next và Docker node26.13.0 string. Giữ rõ C-100/C-101, không coi Express đã implemented hoặc Next đã thay Express. My Office (E-108) là nguồn tham khảo thiết kế, không là business requirement.

## 5. Workflow ở mức nghiệp vụ

**Phần bắt buộc:** người trình diễn mở web → quan sát nội dung và lượt truy cập → nhóm kiểm tra khả năng phục vụ/số liệu ứng dụng → QA thu thập minh chứng theo commit và kịch bản.

**Nếu chọn extension:** người xem vào demo có nhãn mô phỏng → simulator tạo hoạt động tổng hợp → dashboard và văn phòng hiển thị cùng trạng thái agent/task → recent activity giải thích thay đổi vừa xảy ra. Không có bước giao việc cho AI thật trong phạm vi này.

Chi tiết lỗi, transitions và expected results được sở hữu tại [FRD](FRD.md), không định nghĩa lại trong BRD.

## 6. Business requirements

| BR | Nhu cầu / outcome | Rationale / source | Priority / class | Commitment | Bằng chứng thành công | Implementation |
|---|---|---|---|---|---|---|
| BR-100 | Người xem truy cập được giao diện demo Web App | G-100, E-100/E-102 | High / Mandatory | Requested; đặc tả proposed | QA mở được giao diện với nội dung phù hợp release | Starter code-observed, chưa tested |
| BR-101 | Nhóm trình bày được lượng truy cập theo một định nghĩa thống nhất | G-100, E-100/E-101 | High / Mandatory | Requested; visit rule TBD | Đối chiếu số hiển thị với kịch bản visit đã chốt | Planned, chưa Redis client |
| BR-102 | Nhóm vận hành phân biệt app sống và đủ điều kiện phục vụ | G-100, E-100/E-101 | High / Mandatory | Requested; dependency semantics proposed | Có evidence cho bình thường, Redis lỗi và phục hồi | Handlers observed; ready chưa dependency-aware |
| BR-103 | QA có số liệu ứng dụng để quan sát hoạt động | G-100, E-100/E-101 | High / Mandatory | Requested; metric set proposed | Scrape/parser và traffic scenario có kết quả | Planned, chưa metrics route |
| BR-104 | Web App bàn giao được để đóng gói và tích hợp với nhóm | G-100/G-102, E-100/E-102 | High / Mandatory | Requested | Nhóm kiểm chứng container/integration checklist | Docker configured, chưa build/run trong evaluation |
| BR-105 | Người xem hiểu trạng thái agents/tasks mô phỏng tại một nơi | G-101, E-100 | Medium / MVP extension | Proposed conditional | Dashboard và kết quả task khớp simulator scenario | Proposed |
| BR-106 | Người xem phân biệt hoạt động và sự kiện bằng hình ảnh văn phòng dễ theo dõi | G-101, E-100 | Medium / MVP extension | Proposed conditional | 2–3 nhân vật, state và recent activity nhất quán | Proposed |
| BR-107 | Theo dõi từ xa, xem lịch sử hoặc dùng thiết bị yếu khi nhu cầu được xác nhận | E-100 Optional | Low / Optional | Deferred | TBD khi chọn enhancement | Unknown |
| BR-108 | Kết nối agent thật và mở rộng nền tảng khi có lý do đầu tư | E-100 Future | Future | Deferred | Business case, quyền truy cập và parity gates trong tương lai | Chưa migration baseline |

## 7. Chất lượng, lựa chọn và rủi ro

Ứng dụng cần trình bày trung thực khi dependency lỗi (BR-101/BR-102), ghi nhãn dữ liệu mô phỏng (BR-105) và tránh secrets/logs nhạy cảm trong demo (BR-104). [FRD NFR-100..NFR-106](FRD.md) cụ thể hóa các kỳ vọng này. Thresholds về performance, recovery và accessibility còn Q-103/Q-104/Q-105/Q-106.

Phương án tối thiểu là counter web và operational endpoints. Candidate extension dùng simulator trong browser để tránh backend mutation/stream khi chưa cần shared state (A-100/ADR-101 proposed). Server simulator + SSE chỉ xem lại khi cần nhiều clients quan sát cùng state; lựa chọn đó kéo theo consistency/scale và contracts khác.

| Rủi ro / dependency | Tác động | Response / owner |
|---|---|---|
| Extension chiếm thời gian mandatory | Trượt kế hoạch nguồn | Gate mandatory trước; Web owner quyết scope Q-100 |
| Visit chưa được định nghĩa | Counter/API/AC chưa baseline | Chốt đơn vị, refresh/bots/retries; Web owner + QA Q-101 |
| Redis recovery chưa chốt | Hiểu sai atomic counter là bền vững | Chốt loss/restore policy Q-103; Web + Platform |
| Reference rộng và coupling nhiều | Reuse kéo theo CLI/credentials/dependencies ngoài scope | Dùng ma trận chọn module, audit license trước reuse; Web owner |

## 8. Traceability và điểm cần review

| BR | Coverage tại Official | Gap / điều kiện |
|---|---|---|
| BR-100 | [FR-100](FRD.md) | UI runtime acceptance chưa chạy |
| BR-101 | FR-101; [ENT-100](data-contract.md) | Visit semantics và counter HTTP contract BLOCKED Q-101/Q-103 |
| BR-102 | FR-102/FR-103; [getLiveness/getReadiness](api-contract.yaml) | Readiness dependency check/503 là proposed delta |
| BR-103 | FR-104; getApplicationMetrics | Metric vocabulary cần Q-106 |
| BR-104 | FR-105; NFR-100/NFR-105 | Container/operational tests chưa chạy |
| BR-105 | FR-106/FR-107/FR-108 | Extension chưa selected Q-100 |
| BR-106 | FR-109/FR-110/FR-111 | Cùng gate extension |
| BR-107/BR-108 | Không tạo active FR; Migration là feasibility | Optional/Future giữ deferred |

Evidence E-100..E-108, A-100, C-100..C-103 và Q-100..Q-108 tại [registry Official](README.md). ADR-100..104 thuộc [Architecture](architecture.md). Việc chuyển Official không đóng questions hoặc biến assumptions thành accepted decisions.

| Finding | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-100 | Business scope / major | BR-100..BR-108 ↔ FRD1.0.0: optional/future giữ deferred, extension conditional | Tránh scope creep | Giữ Q-100 và trace downstream / Web owner | PASS về phân loại/trace của nguồn được bảo toàn; chưa là runtime outcome |
| VAL-101 | Authority / blocker | Q-100 còn release/rubric/requirement acceptance; tổ chức Official đã được duyệt riêng | Yêu cầu chưa có toàn bộ acceptance decisions | Ghi nguồn quyết định khi chốt / người dùng + nhóm | BLOCKED về nghiệm thu yêu cầu |
