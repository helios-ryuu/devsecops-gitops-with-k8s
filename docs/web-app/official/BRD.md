# BRD — Mục tiêu và Delivery Stage V1/V2

| Document ID | Document version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| WEB-BRD | 1.1.0 | review | 2026-11-07 | Web owner; Platform/QA phối hợp | E-100..E-109 tại [registry](README.md) | WEB-BRD 1.0.0; E-109 chốt release/stack |

Change log 1.1.0: giữ G-100..G-102 và BR-100..BR-108; chọn Mandatory + Office, chia V1/V2, Next Fullstack, page-view/fallback/metrics đã chốt. Scope accepted không đồng nghĩa implementation tested. Nguồn [PT-BRD0.1.0](../validation/practical-test/01-BRD.md) giữ nguyên.

## 1. Vấn đề và goals

Người xem cần hiểu agent nào làm task nào và kết quả công việc. Office 3D là cách trình bày; hoạt động là mô phỏng, không chạy AI thật. Chưa có baseline định lượng về lợi ích/thời gian/users, nên không bịa KPI.

Web phục vụ đồ án NT548 với UI, counter, probes/metrics và integration. Source hiện có mới chứng minh Next starter, hai handlers và cấu hình; target counter/metrics/demo/recovery chưa test. Quyết định release không biến chúng thành features đã có.

| Goal | Outcome / source | Success evidence | Stage / conditions | Owner |
|---|---|---|---|---|
| G-100 | Web tích hợp phần việc đồ án, E-100/E-109 | UI, page-view/idempotency, probes/metrics/integration cases gắn commit | V1 FR-100..FR-105 full; recovery cần Platform | Web + QA + Platform |
| G-101 | Hiểu Agent/Task mô phỏng, E-109 | Dashboard/scene chung snapshot, stage-specific ACs | V1 basic 3 Agents/Idle/Working; V2 full states/scenarios/recent | Web + QA |
| G-102 | Kiểm soát delivery, E-102/E-109 | Checklist V1/V2, không kéo future vào V1 | WBS nêu 05/12/2026, không chứng minh tiến độ/migration date | Web owner + nhóm |

## 2. Stakeholders khác quyền Admin

| Role | Trách nhiệm | Access / authority |
|---|---|---|
| Web Dev — Trần Hồng Phúc | UI/API/domain/Redis integration | Không tự là Admin; triển khai accepted scope |
| Platform Lead — Ngô Tiến Sỹ | Container/routing/policy/probe/scrape/recovery | Quyền monitoring/admin được cấp riêng |
| QA/Observability — Điền Quốc Huy | Testcases, bằng chứng acceptance/load | Không mặc định quyền quản trị |
| Documentation/Demo — Đặng Thế Long | Báo cáo/minh chứng | Không tự đổi scope hoặc thành Admin |
| Viewer | Xem website/Office | Không operational endpoints/monitoring tools |
| Hạ tầng / authorized admin | Probes, scrape, monitoring | Network/monitoring authorization do Platform; không thêm login V1 |

Role source E-101/E-102; access E-109/Q-102. Release đã chốt; rubric/sign-off evidence nếu cần nghiệm thu vẫn do nhóm/QA xác nhận.

## 3. Scope và delivery

| Class | Stage | Nội dung accepted / disposition |
|---|---|---|
| Mandatory | V1; duy trì V2 | FR-100..FR-105 full: web, Redis page views, liveness/readiness, bốn metrics, packaging |
| Office Extension selected | V1 basic | FR-106..FR-110: 3 Agents trong dải 2–3, Idle/Working, minimal simulator/reducer, 3D/animation đơn giản, Reset/reload, Text Dashboard/keyboard |
| Office Extension selected | V2 full | FR-106..FR-111 full, bốn states, scenarios/validation/animations, Recent Activity 20 events |
| Optional | Deferred | SSE, full 2D renderer, persisted history/filter/remote shared state. Text fallback đã mandatory, không còn optional |
| Future | Deferred | Real agents/sessions, auth/multi-user, thay server/API nếu có business case; không điều kiện nghiệm thu V1/V2 |
| External | V1 integration | K3s/Tailscale/Traefik/ArgoCD/CI/policy/monitoring infrastructure; không rebuild trong Web scope |

Next.js Fullstack giữ UI và server-side API; Redis dịch vụ riêng. Không Express trong release. Three.js/adapters là giải pháp, không business need tự thân; E-108 chỉ design reference.

## 4. Business requirements và traceability

| BR | Need / outcome | Goal / source | Commitment | Delivery Stage / coverage | Success evidence / implementation |
|---|---|---|---|---|---|
| BR-100 | Viewer mở được giao diện | G-100, E-109 | High/accepted scope | V1, V2 / FR-100 | UI/text fallback/keyboard ACs; starter observed, target planned |
| BR-101 | Trình bày lượng page views đúng nghĩa | G-100, E-109/Q-101/Q-103 | High/accepted behavior | V1, V2 / FR-101, ENT-100 | F5 mới tăng, retry cùng request 600 s không tăng, operational/assets excluded; chưa code counter |
| BR-102 | Phân biệt sống và đủ điều kiện phục vụ | G-100, E-109/Q-104 | High/accepted target | V1, V2 / FR-102/FR-103 | Ready 2 s/probe 3 s/startup≈50 s có fault/recovery evidence; current ready 200 |
| BR-103 | Có số liệu ứng dụng cho QA/operations | G-100, E-109/Q-106 | High/accepted set | V1, V2 / FR-104 | Bốn metrics scrape, bounded labels, CPU/RAM/K8s từ hạ tầng; chưa route |
| BR-104 | Bàn giao app đóng gói/tích hợp | G-100/G-102, E-109 | High/accepted scope | V1, V2 / FR-105, NFR-100/NFR-105 | Fullstack container/config/probes/access/recovery verified; hiện configured only |
| BR-105 | Hiểu Agents/Tasks mô phỏng | G-101, E-109 | Selected/accepted stages | V1 basic, V2 full / FR-106/107/108 | 3 Agents, 1 running/Agent, 5–8 s, 30 tasks/run; planned |
| BR-106 | Hiểu hoạt động/sự kiện qua Office | G-101, E-109 | Selected/accepted stages | V1 FR-109/110 basic; V2 thêm FR-111 | Animation+text chung state, recent 20 V2, fallback; planned |
| BR-107 | Mở rộng khả năng theo dõi khi có nhu cầu | E-100/E-109 | Optional/deferred | Không active FR; fallback chuyển sang FR-100/109, NFR-106 | Criteria khi chọn enhancement; unknown |
| BR-108 | Mở rộng real execution/nền tảng khi có lý do | E-100/E-109 | Future/deferred | Không active FR; Migration future | Business case/access/parity trước thay đổi; chưa approval target |

## 5. Workflow nghiệp vụ

**V1:** tải/F5 trang → register một page view → xem counter và 3 Agents/Office cơ bản → simulator/reducer cập nhật Idle/Working → Reset Demo/reload tạo run mới. Reset Demo không ghi visit hoặc reset total; reload/F5 là page view mới. Probe/scrape/assets không là visits.

**V2:** giữ V1 → hoàn thiện Completed/Failed/Recovery scenarios → dashboard/animations/recent 20 events cùng snapshot → giới hạn 30 tasks/run và Reset/reload áp dụng. Không biến run thành shared retained history.

Khi Redis lỗi, browser đã load có thể hiện counter unavailable và demo tiếp tục. Nhưng readiness failed có thể khiến Kubernetes rút toàn bộ Next pod khỏi serving endpoints, viewer mới có thể không tải Office. Không cam kết Office online độc lập Redis; Architecture nêu trade-off.

## 6. Quality và risks

| Risk / expectation | Response / decision | Owner / residual |
|---|---|---|
| Retry/request duplicate | requestId+atomic registration, dedup 600 s; không exactly-once vô hạn | Web/QA fault tests |
| Mất total do expiry/reset | Total no TTL/no auto reset; persistence/backup/recovery có phương án | Platform/Web approve storage/policy/RPO/RTO |
| 3D fail | Text Dashboard fallback, keyboard, text ngoài màu | Web/QA device/accessibility qualification |
| Redis ready ảnh hưởng Office | 2 s app check, 3 s probe, ≈50 s startup; live không phụ thuộc Redis | Platform/QA routing/fault tests |
| Scope creep | V1/V2 rõ, không login/real agents/SSE/history API | Web owner; BR-107/108 deferred |

[FRD](FRD.md) sở hữu NFR-100..106; [API](api-contract.yaml) wire; [Data](data-contract.md) storage/lifecycle; [Architecture](architecture.md) A-100/ADRs; [registry](README.md) decisions/residuals.

## 7. Findings

| ID | Check / severity | Locations / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-100 | Scope/stages / major | BR-100..108 ↔ FRD1.1.0; FR-111 chỉ V2 | Giữ accepted stage boundary | Check trace/stage / Web+QA | Decision coverage; runtime chưa test |
| VAL-101 | Authority / major | E-109 giảiQ-100 release; rubric/sign off evidence thiếu | Không còn release selection blocker; chưa nghiệm thu | Acceptance evidence riêng / nhóm+QA | Scope RESOLVED; test pending |
