# BA Official — AI Agent Office Monitor

| Document ID | Document version | Status | Date | Owner role | Sources / upstream |
|---|---|---|---|---|---|
| WEB-INDEX | 1.1.0 | review | 2026-11-07 | Web owner; Platform/QA phối hợp | Official 1.0.0 tại `cb25b4a4f0096796fbca2c797844f3d44fdec42f`; quyết định E-109 |

Change log 1.1.0: chốt Mandatory + AI Office, stages V1/V2, Next Fullstack, page-view/idempotency, TTL, probe timeouts, fallback và metrics. Giữ IDs và Validation. Sáu document versions cùng 1.1.0; API tăng 0.1.0→**0.2.0**, OpenAPI vẫn 3.1.1. Domain simulator giữ logical v1 và stage applicability.

## 1. Điều hướng và trách nhiệm nội dung

| Tài liệu | Định nghĩa chính |
|---|---|
| [BRD](BRD.md) | Goals, stakeholder, scope và Delivery Stage |
| [FRD](FRD.md) | FR/RULE/AC/NFR, workflow/state machine V1/V2 |
| [API Contract](api-contract.yaml) | Operations, schemas, validation/errors và metric catalog |
| [Architecture](architecture.md) | Next Fullstack, routing/readiness impact, controls và ADRs |
| [Data Contract](data-contract.md) | Counter/dedup storage, atomicity, lifecycle, demo data và recovery |
| [Migration Plan](migration-plan.md) | Định hướng thay server/API tương lai từ baseline Next; không đòi Express source |

Trace: BR→FR/RULE/AC→operationId hoặc HTTP N/A→ENT/storage; NFR→control→verification. Registry E/A/C/Q chung tại đây. [Practical test](../validation/practical-test/evaluation-report.md) và [reference analysis](../validation/practical-test/07-reference-analysis.md) là lịch sử giữ nguyên, không sở hữu quyết định release hiện hành.

## 2. Delivery Stage đã chốt

| Stage | Phạm vi | Chưa thuộc stage |
|---|---|---|
| V1 — Integration Release | FR-100..FR-105 đầy đủ; FR-106..FR-110 basic: 3 Agents trong dải 2–3, Idle/Working, simulator/reducer tối thiểu, 3D/animation đơn giản; Reset Demo, Text Dashboard/keyboard | FR-111; full Success/Failure/Recovery scenarios/validation/animations |
| V2 — Full AI Office | Hoàn thiện FR-106..FR-111; bốn states, scenarios/validation/animations đầy đủ; Recent Activity 20 events | Không tự thêm real agents, login/multi-user, SSE/shared history |

Simulator cadence 5–8 s/event, 1 running task/Agent, 30 tasks/run. Reset/reload tạo run mới; Recent 20 chỉ V2. Chi tiết V1 completion được xử lý tường minh tại FRD/Q-107, không âm thầm thêm full Success/Failure vào V1.

## 3. Trạng thái và quyền truy cập

| Dimension | Cách hiểu |
|---|---|
| Decision | `accepted` cho nội dung E-109; `design` cho lựa chọn contract/triển khai dẫn xuất, không phải code hoặc Platform approval |
| Document | `review`: bản Official để review; không tự nghiệm thu phần mềm |
| Implementation | code-observed/configured/planned/tested tách biệt; code/config không tự thành tested |
| Question | RESOLVED phần đã chốt; PARTIALLY RESOLVED chỉ chi tiết còn liệt kê. Không giữ OPEN toàn bộ quyết định đã giải quyết |
| Check/gate | PASS/FAIL/BLOCKED/N/A luôn kèm phạm vi; tài liệu PASS không chứng minh runtime/migration |

Stakeholder không tự mang quyền Admin. Viewer xem website/Office; operational endpoints/tools chỉ infra/authorized admin. Không thêm login V1. Text Dashboard là fallback bắt buộc, không phải một renderer 2D mới.

## 4. Evidence và assumptions

| ID | Nguồn | Claim / giới hạn |
|---|---|---|
| E-100 | Brief tại [practical evaluation](../validation/practical-test/evaluation-report.md) | Intent ban đầu; E-109 cập nhật scope/stack |
| E-101 | [README snapshot](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/README.md) | Phân công/đồ án, Express wording cũ; không là stack release hiện tại |
| E-102 | [WBS snapshot](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/WBS.md) | Lịch nguồn, done labels không chứng minh runtime |
| E-103 | [Package](../../../app/package.json), [UI](../../../app/src/app/page.tsx), [healthz](../../../app/src/app/healthz/route.ts), [ready](../../../app/src/app/ready/route.ts) đọc lại tại HEAD `cb25b4a` | Next starter và hai handlers; ready luôn 200; target counter/metrics/demo chưa thấy implementation |
| E-104 | [Dockerfile](../../../app/Dockerfile), [Next config](../../../app/next.config.ts), [Deployment](../../../k8s-manifests/base/deployment.yaml), [Redis](../../../k8s-manifests/database/redis.yaml), root Kustomize | Non-root standalone/Redis configured; chưa startupProbe/explicit timeout 3 s hoặc Redis volume/PVC trong source được đọc; chưa live verification |
| E-105 | [Validation trước đó](../validation/README.md) | Lịch sử thử nghiệm, không scope hiện hành |
| E-106 | Sáu BA Skills/shared standard/templates | Author/review workflow, không feature evidence |
| E-107 | Practical verification record | Bảo toàn file ở lượt cũ, không runtime evidence lượt mới |
| E-108 | My Office commit `77fdd1371ea1f3a78bd905880b5681deec3b7a45` tại reference analysis | Design evidence, không copy toàn bộ scope/source hoặc license assumptions |
| E-109 | Quyết định Q-100..Q-108 người dùng cung cấp ngày 2026-11-06 | Authority cho release/stack/values đã chốt; không implementation/test evidence |

**A-100:** giữ thiết kế demo browser-local, mỗi browser một run; không shared/persistent agents (ADR-101). UUID requestId, decimal-string total và atomic Redis registration là thiết kế dẫn xuất tại API/Data/Architecture, không gắn nhãn người dùng đã quyết định từng wire field.

## 5. Contradictions sau quyết định mới

| ID | Status / nội dung | Impact / owner |
|---|---|---|
| C-100 | RESOLVED release stack: Next Fullstack, không Express V1/V2; wording cũ là lịch sử | Không dùng thiếu Express làm blocker hiện tại; Web triển khai Next API |
| C-101 | README Node 24 khác Docker node 26.13.0 string | Version/build verification theo component còn Platform/Web |
| C-102 | README database namespace khác root production-app | Platform xác minh render/live policy; không sửa manifests ở lượt này |
| C-103 | Target timing đã chốt nhưng current ready 200/probe config chưa khớp | Implementation gap; Web/Platform/QA thực hiện sau |

## 6. Q registry — phần đã chốt và residual

| Q | Accepted theo E-109 | Chi tiết còn lại / owner | Status |
|---|---|---|---|
| Q-100 | Mandatory + Office; V1 FR-100..105 full, 106..110 basic; V2 106..111 full | Rubric/sign-off evidence nếu cần nghiệm thu / nhóm + QA | RESOLVED release |
| Q-101 | F5 là page view mới; requestId/idempotency, exception handling; exclude probes/metrics/static assets | Kiểm chứng lifecycle/request retry theo API/AC / Web + QA | RESOLVED behavior; untested |
| Q-102 | Viewer product access; operational/tools infra hoặc authorized admin; không login V1 | Allowlist/proxy/CNI grants, origin/deny enforcement cụ thể / Platform + QA | PARTIALLY RESOLVED; policy accepted |
| Q-103 | Total no TTL/no auto-reset; dedup 600 s; cần persistence/backup/recovery | Storage/PVC, AOF/RDB, backup cadence/location/retention, restore, RPO/RTO, init authority/max count / Platform + Web + QA | PARTIALLY RESOLVED; TTL/reset RESOLVED |
| Q-104 | Redis check 2 s, probe 3 s, startupProbe budget≈50 s | Probe timing tuple proposal, check depth, counter command budget, drain/load/FPS/memory/device targets / Platform + QA | PARTIALLY RESOLVED; ba timing targets RESOLVED |
| Q-105 | Text Dashboard fallback, keyboard, text ngoài màu/animation | Browser/accessibility qualification / Web + QA | RESOLVED functional; qualification TBD |
| Q-106 | Bốn metrics V1; CPU/RAM/K8s dùng hạ tầng; bounded labels | Histogram buckets, registered route vocabulary, scrape wiring, fault-check method / Web + QA + Platform | PARTIALLY RESOLVED; metric set RESOLVED |
| Q-107 | 3 Agents, 5–8 s, 1 running/Agent, recent 20 V2, 30 tasks/run, Reset/reload new run; basic V1/full V2 | Quy tắc V1 finish-to-Idle nêu tại FRD; các values không còn TBD / Web + QA | PARTIALLY RESOLVED chỉ chi tiết V1 |
| Q-108 | Next Fullstack UI/server API, Redis riêng, không Express release | Chỉ migration future: business case/target version/window/authority / người dùng + Web + Platform | RESOLVED current; future DEFERRED |

Dedup 600 s chỉ bảo vệ trong retention window khi Redis còn state; không exactly-once vô hạn hoặc qua mất dedup key sớm. Chi tiết chưa duyệt phải giữ TBD/proposed, không biến thành approval Platform.

## 7. Version và change propagation

WEB-BRD/FRD/API/ARCH/DATA/MIG cùng document 1.1.0. API 0.2.0 thêm getVisitorCount/registerPageView cho FR-101; giữ getLiveness/getReadiness/getApplicationMetrics. Consumers/probes/scraper cần review semantics/errors/metrics trước triển khai; đây chưa là deployed baseline. Giữ tất cả BR/FR/RULE/AC/NFR/ENT/ADR/MIG IDs, bổ sung stage thay vì renumber.

Khi residual được chốt: ghi decision/source/date ở canonical owner, update versions/trace và kiểm tra downstream. Chỉ `official/` thay đổi; không app/infra/Validation/CI/CD/migration execution/main merge.

## 8. Validation 1.1.0

Đã kiểm tra bản 1.1.0 ngày **2026-11-07**: **8 nhóm PASS, 0 FAIL**. Kết quả bản 1.0.0 là lịch sử, không dùng thay lượt này. Lượt kiểm tra đầu phát hiện separator của một bảng FRD thừa một cột; đã sửa và chạy lại.

| Nhóm kiểm tra | Kết quả thực thi / giới hạn |
|---|---|
| Phạm vi chỉnh sửa | Chỉ 7 file trong `official/` thay đổi; 81 file tracked ngoài khu vực này giữ nguyên SHA-256, gồm app/manifests/CI/CD/Validation; branch/HEAD không đổi |
| OpenAPI specification | API 0.2.0/OpenAPI 3.1.1 hợp lệ với openapi-spec-validator 0.9.0; YAML parse bằng PyYAML 6.0.3 |
| Refs và examples | 14 local refs resolve; 19 request/response examples qua JSON Schema Draft202012 và format checks với jsonschema 4.26.0 |
| Negative examples | 10 ca sai bị từ chối, gồm UUID, body fields, decimal total, null, ready state, time và error code sai operation |
| IDs, trace và stages | 9 BR, 12 FR-parent pairs, 9 RULE, 15 AC, 7 NFR, 4 ENT; giữ ADR/MIG IDs; 5 operation mappings; FR-111/AC-112 chỉ V2 |
| Counter/data/access | POST registration và GET read tách rõ; UUID, decimal-string total, dedup 600 s không refresh, total no TTL; operational access classes hạn chế |
| Timings/metrics/fallback/architecture | Redis 2 s/probe 3 s/startup≈50 s; đúng 4 metric families; Text Dashboard/keyboard; Next Fullstack và ảnh hưởng Office khi NotReady; future migration từ baseline Next |
| Metadata/links/Q registry | Document 1.1.0/status review, API 0.2.0, local links/table columns/fences và 9 Q statuses nhất quán; phần đã chốt không còn OPEN toàn bộ |

**Residual cần xác nhận:** Q-102 enforcement/grants/origins; Q-103 bootstrap/storage/AOF-RDB/backup/restore/RPO-RTO và giới hạn counter; Q-104 probe timing tuple/check depth/drain/performance qualification; Q-105 browser/accessibility qualification; Q-106 histogram buckets/scrape wiring/freshness; Q-107 basic finish-to-Idle của V1 là proposal chưa được người dùng xác nhận. Các numeric targets và release/stack đã chốt vẫn RESOLVED, không mở lại vì residual này. Migration target/window/business approval vẫn future-deferred.

Giới hạn: cùng agent biên tập và review, chưa là đánh giá ngữ nghĩa độc lập; Mermaid chỉ kiểm tra văn bản, chưa render. Không chạy app/Redis/concurrency/recovery/live probes/ingress/load/simulator hoặc migration parity. Samples `text/plain` qua schema không thay Prometheus parser/scrape integration. Không dùng các PASS tài liệu để tuyên bố implementation hoặc nghiệm thu.
