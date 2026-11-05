# Evidence, assumptions và contradictions

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| TEST-EVIDENCE | 0.1.0 | draft | 2026-11-05 | Codex kiểm tra; Web/Platform giải quyết gaps | README/WBS, source/config được pin; catalog runtime | Project `2110eddec91bc3e34137c86fef693095c4afb677`; bundle `3f0127b33bc6612f743c1aec4862079eea3adb9e` |

Change log 0.1.0: chụp source/hash, ghi disagreements không tự chọn một nguồn làm accepted truth. Registry này là canonical cho evidence/A/Q/C trong sáu smoke documents; không phải Data contract hoặc kiến trúc chính thức.

## Evidence register

[evidence.json](evidence.json) chứa Git refs, hash SHA256/blob và source lines được đánh số. Các path dưới đây tính từ repository root; links mở source đang đọc. Commit pin ở trên giúp tránh hiểu path `main` là bất biến.

| ID | Nguồn / vị trí | Quan sát và giới hạn |
|---|---|---|
| E-01 | [README](../../../README.md), §1.2/2/3/5/6/7; đặc biệt L53,72,74,76,172..176 | Source-stated: Express/Redis/counter/probes/metrics và mục tiêu DevSecOps; §5 lại mô tả Next. Không chứng minh runtime |
| E-02 | [WBS](../../../WBS.md), L8,20,26,30..36 và 4.2..5.3 | Source-stated: Next UI + Redis, task status/deadline; không có authority phê duyệt hoặc test output |
| E-03 | [package](../../../app/package.json), L5..24; pnpm lockfile hash | Next 16.4.3/React 19.3.0; next dev/build/start. Không có direct dependency Express, Redis client hoặc prom-client |
| E-04 | [page](../../../app/src/app/page.tsx), L1..72; [layout](../../../app/src/app/layout.tsx) | Starter UI và metadata; chưa có counter hiển thị trong các file đọc |
| E-05 | [healthz](../../../app/src/app/healthz/route.ts), L1..10 | Code-observed GET trả status ok, uptime process, timestamp ISO, HTTP 200; chưa gọi HTTP thực tế |
| E-06 | [ready](../../../app/src/app/ready/route.ts), L1..9 | Code-observed GET trả ready/timestamp/200 vô điều kiện; không kiểm tra Redis |
| E-07 | [Next config](../../../app/next.config.ts), L3..17; [Dockerfile](../../../app/Dockerfile), L7/19/33/51..58 | Standalone Next build/runtime được cấu hình, Node image string 26.13.0; không chứng minh build/image khả dụng hay runtime đã chạy |
| E-08 | [ConfigMap](../../../k8s-manifests/base/configmap.yaml), L6..8; [Web deployment](../../../k8s-manifests/base/deployment.yaml), L16..58 | REDIS_HOST/PORT có cấu hình; app web 2 replicas, UID/GID 10001, probes. Không chứng minh app đọc biến/đã kết nối Redis |
| E-09 | [Redis](../../../k8s-manifests/database/redis.yaml), L1..57 | Deployment/Service và redis-cli ping được khai báo; không thấy PVC/volume, không có counter key/lifecycle/TTL code. Không kết luận về persistence của cluster đang chạy |
| E-10 | [root Kustomization](../../../k8s-manifests/kustomization.yaml), L4..9; [NetworkPolicy](../../../k8s-manifests/security/network-policy.yaml), L1..20; child kustomizations | Root khai báo production-app, gom base/database/security; policy có podSelector app:web, không namespaceSelector. Kết quả render kiểm tra riêng, không suy từ tên folder database |
| E-11 | [ArgoCD app](../../../argocd/app.yaml), L10..25 | source main/path k8s-manifests, prune/selfHeal; không khai báo directory recurse trong file này. Không có live sync evidence |
| E-12 | [Runtime catalog snapshot](runtime-discovery.json) | 6 names/descriptions/paths đã được runtime quảng bá cho phiên, trước đọc SKILL.md. Bản chép agent, không phải raw registry API export; chưa blind routing |
| E-13 | [Bundle run](bundle-results.json) | Chạy lại checker: 22 PASS/0 FAIL trên bundle và fixtures Queue Board. Không chứng minh output NT548 hoặc runtime skill selection |
| E-14 | [Document checks](document-checks.json) | Kiểm tra artifact NT548 được chạy sau tạo docs; phạm vi và negative mutations được checker ghi. Không chứng minh semantic review độc lập |

Quét implementation có phạm vi: `git ls-files` toàn snapshot; đọc toàn `app/src/app` hiện có, package/lock và config liên quan; `rg -n -i --glob '!pnpm-lock.yaml' 'express|ioredis|createClient|prom-client|REDIS_|/metrics|incr\(' app` không có match (exit 1 nghĩa là không match). Đây là kết luận về snapshot được pin, không phải mọi branch, máy cá nhân, image hoặc production. App hiện không có test suites theo inventory; không suy ra kết quả runtime.

## Next.js, Express và Redis

| Thành phần | Kiến trúc dự kiến từ nguồn | Implementation thực tế quan sát | Tested/live |
|---|---|---|---|
| Next.js | WBS 3.3 và README §5 nêu UI/frontend Next 16 | Package/scripts/config/source là Next App Router; hai route probes cũng ở Next, nên snapshot Next có cả UI và HTTP handlers | Chưa chạy |
| Express | README §1.2 nêu Node 24 Express cho web/backend; README chưa diễn giải rõ ranh giới frontend/backend đồng tồn tại | Không thấy entry point/package/router Express trong tracked tree. Không dùng Next để kết luận Express đã bị thay thế hoặc là dependency của Next | Chưa chạy; backend evidence missing Q-04 |
| Redis | README/WBS nêu lưu/đếm lượt truy cập | Có config service/deployment/env. Chưa thấy Redis client, lệnh increment, key, TTL hoặc UI counter | Không xác minh kết nối, persistence hoặc concurrency |

Một số notes đã sửa sẵn tại repo bundle thuật lại rằng người dùng ở phiên trước đã làm rõ Next frontend + Express backend + Redis. Đây là **nguồn thứ cấp ngoài baseline**, không phải lời xác nhận của người dùng trong phiên này. Chỉ dùng làm cảnh báo tránh suy luận “Next thay Express”; không nhập AI workspace, Laravel, Three.js, dates hoặc accepted scope từ notes đó. Q-04 yêu cầu source backend và ranh giới được nhóm xác nhận trước baseline.

## Contradictions / gaps

| ID / severity | Locations / affected IDs | Expected vs observed | Tác động | Smallest correction / owner | Result |
|---|---|---|---|---|---|
| C-01 major | README L53 vs §5; WBS 1.2/3.3; E-03/04/07; BR-01/02, ADR-02 | README mô tả Express/Node24; cấu trúc/WBS mô tả Next; code chỉ chứng minh Next. Có thể đồng tồn tại, không đủ cơ sở tuyên bố mutually exclusive | Sai topology/runtime ownership nếu gộp Next với backend | Bổ sung component roles và links backend thực tế sau Q-04; Documentation/Web/Platform | FAIL về độ đầy đủ/nhất quán nguồn; không phải FAIL của Next |
| C-02 major | E-06; FR-03, NFR-02, Q-03 | Readiness code chỉ 200, không chứng minh phục vụ chức năng phụ thuộc Redis | False readiness nếu người đọc hiểu là dependency-aware | Tài liệu nói rõ current semantics; nhóm quyết định target trước implementation | FAIL nếu claim Redis-ready; current code description trong API là đúng |
| C-03 major | E-01 L53/76; E-03/04; FR-01/04 | Counter/metrics là mục tiêu; snapshot chưa có code | Demo/full API chưa sẵn sàng | Ghi planned/gap; Web/QA cung cấp implementation + test sau review | BLOCKED về triển khai; PASS khi phân loại đúng |
| C-04 major | README L74/§3.2 vs E-10; NFR-04 | Nguồn nói namespace database; root Kustomize đặt production-app cho cả Redis/policy; folder không là namespace | Sai mô tả boundary network/security | Xác minh render offline; sửa mô tả/ADR sau nhóm quyết định; không đổi manifests trong test | FAIL về consistency tài liệu/config |
| C-05 major | E-09; ENT-03, NFR-02 | Chưa có volume/lifecycle/TTL và client counter; không thể cam kết durable/global/unique visits | Sai recovery/parity nếu giả định persistence | Chốt Q-02/Q-05 trước Data baseline; Web/Platform | BLOCKED |
| C-06 minor | README L72/§3.1 vs E-10/E-11 | README nói directory recurse; config root là Kustomize và app không khai directory | Hướng dẫn GitOps không khớp config quan sát | Cập nhật đúng source mode sau xác nhận; Documentation/Platform | FAIL về mô tả nguồn, live mode chưa kiểm tra |
| C-07 minor | README Node24 nhiều đoạn vs WBS 3.4/E-07 | Dockerfile Next khai node:26.13.0-alpine3.23; version string không chứng minh image tồn tại, không chỉ ra backend Node version | Sai thông tin build/runtime | Tách version theo component và source; không tự đổi Dockerfile | FAIL về wording; runtime availability BLOCKED |
| C-08 minor | WBS 3.1..3.7 dates/status vs inspection 2026-11-05 | Có task ngày tương lai đánh dấu hoàn thành | Không thể coi lịch/status là bằng chứng chạy | Ghi completion evidence hoặc actual dates; Project coordination | BLOCKED về xác minh, không kết luận gian sai |

Các nguồn baseline giữ nguyên. Chỉ sandbox sửa cách diễn giải; các đề xuất cho canonical README/WBS chưa được áp dụng.

## Assumptions và questions

| ID / kind | Nội dung / provenance | Scope / commitment | Impact / status | Resolution role |
|---|---|---|---|---|
| A-01 Assumption | Có người đánh giá nghiệm thu; suy từ WBS 5.3, không biết danh tính/quyền | Context proposed | Không gán accepted sign-off | Nhóm / học phần |
| A-02 Assumption | Lát cắt counter + probes/metrics đủ để test sáu workflows; quyết định thử nghiệm của agent theo yêu cầu docs-only | Sandbox only / proposed | Không tương đương toàn scope sản phẩm | Người dùng review |
| Q-01 Open Question | Ai phê duyệt scope và tiêu chí nghiệm thu? Rubric bắt buộc ở đâu? | Trước official baseline | Thiếu authority/external obligation evidence | Nhóm / scope owner TBD |
| Q-02 Open Question | “Lượt truy cập” tính theo request/page/session/unique user? Refresh/retry/concurrent requests xử lý thế nào? UI đọc dữ liệu qua API nào? | BR-01/FR-01 proposed | Chặn AC đầy đủ, API nghiệp vụ và migration parity | Web Dev + nhóm scope |
| Q-03 Open Question | Ready cần kiểm tra Redis hay chỉ tiến trình? Timeout/failure status/body mong muốn? Probe nằm ở Next hay backend tương lai? | BR-02/FR-03 proposed | Chặn target ready contract và kiến trúc dependency handling | Web Dev + Platform + QA |
| Q-04 Open Question | Express backend ở path/branch/repo nào, consumer boundary với Next và port/route ownership ra sao? /metrics ở component nào? | ADR-02 proposed, FR-01/04 gaps | Chặn topology target, full API và Express migration | Web Dev + Platform |
| Q-05 Open Question | Counter key/schema, initial value, TTL/reset, persistence/recovery, consistency và mapping wire là gì? | ENT-03 proposed | Không thể cam kết durable/unique/exactly-once; không bịa TTL | Web Dev + Platform |
| Q-06 Open Question | Có migration intent/target được chốt không? Baseline Express tests/contracts và cutover/rollback authority là ai? | MIG-01..MIG-04 conditional | Migration không executable, không giả Laravel là mandatory | Web/Platform + scope owner TBD |
| Q-07 Open Question | Ngưỡng tải/latency/error rate, cửa sổ đo, retention và freshness/metrics acceptance? | NFR-03 proposed | Không đặt 99.9%, 100ms hoặc RPO/RTO tự ý | QA + Platform + nhóm |

Không câu hỏi nào ở trên chặn việc hoàn tất kiểm thử Skill với draft có gaps; chúng chặn **phê duyệt/triển khai tài liệu chính thức**. Không cần trả lời để agent tiếp tục các checks độc lập trong lượt này.
