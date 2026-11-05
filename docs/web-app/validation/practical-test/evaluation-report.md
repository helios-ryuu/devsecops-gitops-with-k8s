# Explicit Practical Evaluation — BA Documentation Skills

| Document ID | Version | Status | Date | Owner role | Sources / upstream |
|---|---|---|---|---|---|
| PT-EVAL | 0.1.0 | DRAFT | 2026-11-05 | Senior BA / Solution Architect / Documentation QA; acceptance authority TBD | E-100..E-108; bảy artifacts PT-* 0.1.0; shared standard 1.0.0 |

Change log 0.1.0: practical evaluation mới, độc lập với smoke và các validation results trước đó. Tất cả outputs là DRAFT; đây không phải acceptance certificate hoặc migration/deployment approval.

## Kết quả và cách đọc PASS / FAIL / BLOCKED

Đã tạo sáu tài liệu BA, một reference analysis và report này cho **riêng Web App**. Ba Skills có kết quả PASS về chất lượng draft trong phạm vi evidence hiện có; API/Data/Migration có đầu ra hữu ích nhưng overall BLOCKED bởi các quyết định/baseline cần thiết còn thiếu. Không phát hiện lỗi nội dung còn tồn tại đủ căn cứ gắn FAIL tại thời điểm review cuối; BLOCKED không đồng nghĩa skill tự động pass hoặc hệ thống đã sẵn sàng.

PASS ở đây là chất lượng nội dung draft trong phạm vi đã kiểm tra. Các kết quả runtime AC/NFR, release selection, counter completeness và production readiness chưa PASS. Reviewer chính là agent tác giả; không có independent human sign-off hoặc blind evaluation.

## Skill discovery và explicit activation

Sáu Skills xuất hiện trong catalog đã đăng ký và người dùng gọi `$skill-name` trực tiếp, đồng thời cung cấp SKILL.md trong hội thoại. Đây là **explicit invocation evaluation**, không phải natural-language routing benchmark. Đã đọc bản SKILL.md trên filesystem, shared reference và template tương ứng trước khi tạo documents; không chỉ dựa vào headings hoặc mô tả catalog.

Local bundle root: `C:/Users/84352/.agents/skills/business-analyst-skill/skills/`. Shared reference: `_ba-shared/references/documentation-standard.md`, version 1.0.0. Không sửa bundle, không đồng bộ/pull remote BA Skills repository. GitHub metadata của Nobita534/BA-skill-documentation được đọc để xác định repository reference; không có bằng chứng local bundle bằng đúng commit remote, nên không claim remote revision pin.

| Order / Skill | SKILL.md đã đọc | Template đã đọc | Artifact |
|---|---|---|---|
| 1 brd-authoring | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/brd-authoring/SKILL.md) | assets/brd.template.md | [01-BRD.md](01-BRD.md) |
| 2 frd-authoring | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/frd-authoring/SKILL.md) | assets/frd.template.md | [02-FRD.md](02-FRD.md) |
| 3 api-contract-design | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/api-contract-design/SKILL.md) | assets/api-contract.template.yaml | [03-api-contract.yaml](03-api-contract.yaml) |
| 4 architecture-design | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/architecture-design/SKILL.md) | assets/architecture.template.md | [04-architecture.md](04-architecture.md) |
| 5 data-contract-design | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/data-contract-design/SKILL.md) | assets/data-contract.template.md | [05-data-contract.md](05-data-contract.md) |
| 6 backend-migration-planning | [SKILL.md](C:/Users/84352/.agents/skills/business-analyst-skill/skills/backend-migration-planning/SKILL.md) | assets/migration-plan.template.md | [06-migration-plan.md](06-migration-plan.md) |

Skill file SHA-256 cho reproducibility của installed inputs:

```text
brd-authoring               9bf3944f0f311d30d49d36081a6a88ee0267e66a6de4b0c53892e7e94d8aba0d
frd-authoring               5ff9b7670532727fe38ba68dc86adf80ad75619e232090bc0cd9f80dc52641e8
api-contract-design        8ef5b8d53d3d73ebe4b22fa0080c4b2b6807ed7348bd00c390d2dd83e567e4d8
architecture-design        af2d9e63893d82334500bf6a9401626522546a7be2e72e4ba282a5fd00425be8
data-contract-design       7b84370f4d5fb7bf637e08b639e0b7c6cf4a6d8fc7d19a5f3f95934aa7d0b8f1
backend-migration-planning  b6b15af35e18d8ad31bd1a28afaef6e0c6c2f25461b8a2fb4da60789194586a6
```

Đã áp dụng canonical ownership, business-first, distinct provenance/scope/commitment/implementation, contract-first và second-pass consistency sau khi có Data/Migration. Không gọi thêm agents; không dùng kết quả test trước đó như kết quả thực thi mới.

## Source evidence assessment

Target local branch: `ba/documentation`. HEAD inspected: `2110eddec91bc3e34137c86fef693095c4afb677`, remote origin trỏ target repository. Working tree ban đầu có `?? docs/`, nên HEAD không đại diện tất cả docs có sẵn. Đã hash snapshot 71 existing workspace files (loại .git/node_modules) trước khi viết; preservation check cuối được ghi bên dưới. Ngày inspection: 2026-11-05, không lấy lịch WBS làm thời điểm deployment thực tế.

| Evidence | Source / location | Knowledge / verification | Claim và giới hạn |
|---|---|---|---|
| E-100 | User practical-evaluation brief hiện tại | Fact về requested intent / user-provided | Scope classes, product problem, proposed stack; không implementation proof hoặc rubric độc lập |
| E-101 | [README.md](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/README.md), §1.2/§2/§6 | Source-stated | Web owner, Express/Node 24, Redis/probes/metrics và lịch nhóm; không runtime |
| E-102 | [WBS.md](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/WBS.md), phân công, 2.4, 3.3/3.4, 4.2 | Source-stated | Next.js/Redis, done labels, deadline 05/12; done không chứng minh implemented/run |
| E-103 | [app/package.json](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/app/package.json), [page](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/app/src/app/page.tsx), [healthz](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/app/src/app/healthz/route.ts), [ready](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/app/src/app/ready/route.ts) | Code-observed, not tested | Next dependencies + starter, GET probes; ready unconditional. File inventory app/src/app chỉ có hai route handlers. Không Express/Redis client/metrics/Three/simulator implementation tìm thấy trong app |
| E-104 | [Dockerfile](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/app/Dockerfile), next.config.ts; [root kustomization](https://github.com/helios-ryuu/devsecops-gitops-with-k8s/blob/2110eddec91bc3e34137c86fef693095c4afb677/k8s-manifests/kustomization.yaml), base configmap/deployment, database/redis, security/network-policy | Configured only | Next standalone, Node 26.13.0, port 3000, two replicas, UID 10001, Redis env/service/probes, namespace production-app. Redis YAML không volume/PVC. Không live infra verification |
| E-105 | [Prior validation](../README.md), [report](../report.md), [evidence](../evidence-register.md), [smoke BRD](../smoke/BRD.md) | Existing document evidence | Dùng để nhận diện kết quả/IDs cũ và bảo toàn; không overwrite/reuse requirement scope cũ. Bài smoke loại agent idea vì input lúc đó khác, không là mâu thuẫn cần sửa |
| E-106 | Local six SKILL.md + shared reference + six templates | Files read / hashes ở trên | Installed bundle được đánh giá; remote equivalence chưa verified |
| E-107 | git branch/status/rev-parse/remotes; pre/post filesystem hashes | Local command-observed | Branch/edit boundary; không commit/push/merge; không proof app behavior |
| E-108 | [My Office pinned commit](https://github.com/khanh020905/my-office/tree/77fdd1371ea1f3a78bd905880b5681deec3b7a45), R-100..114 tại [analysis](07-reference-analysis.md) | Read-only code/source analysis qua connector | Module/data-flow/security/license findings; không execution/performance/security certification |

Web fetch fallback đã được thử nhưng GitHub pages trả cache miss; nghiên cứu source sử dụng GitHub connector fetch đọc được content. Không coi cache miss là không có license/source. Không tìm hoặc hiển thị credentials từ môi trường cá nhân.

## Document quality evaluation và kết quả từng Skill

| Skill / artifact | Nội dung thực tế đã đánh giá | Quality finding / limitation | Overall skill result |
|---|---|---|---|
| BRD | Nhu cầu hiểu work state trước 3D; goals không bịa KPI; stakeholder source; BR-100..108 phân scope/commitment/implementation; alternatives minimal vs extension | PASS draft framing/traceability; authority/rubric/release selection chưa baseline | **PASS** scoped draft; acceptance BLOCKED Q-100 |
| FRD | 12 FR đều parent BR; HTTP/UI/internal tách rõ; agent/task transitions/guards, duplicate/gap rules; 15 AC có success/failure/boundary; 7 NFR có verification/owner | PASS conditional behavior design; counter semantics, performance/recovery thresholds không giả định | **PASS** scoped draft; affected ACs BLOCKED |
| API | Three operations có x-fr-ids; success probe types giữ source; proposed ready 503 và metrics; Error/UTC schemas/examples; explicit no public access decision; no GET counter mutation | YAML/OpenAPI/examples PASS; FR-101 chưa operation vì Q-101, security chưa chốt. Partial contract không đủ cover mandatory app | **BLOCKED** completeness/access; supported subset PASS |
| Architecture | Current/configured/proposed diagrams riêng; context/components/deployment/sequences; NFR coverage; Redis failure behavior; slim ADAPT/BUILD và trust boundaries | PASS design reasoning; Express topology/probe ownership/resource fit còn TBD; Mermaid chưa rendered | **PASS** scoped design draft; deployment readiness BLOCKED |
| Data | Entity grain/types/null/enum/relationships; logical browser event contract; API mappings; proposed Redis namespace/type/TTL handling; concurrency/ambiguous timeout/loss distinction | Logical mapping PASS; visitor trigger/init/TTL/max encoding/persistence/restore thiếu quyết định, không tạo false guarantee | **BLOCKED** lifecycle baseline; supported logical draft PASS |
| Migration | Missing Express explicit; parity rows bám five upstream docs; framework/default serialization risks; phase gates; single writer; cutover/rollback hậu writes và unsafe boundary | Plan ở mức feasibility có nội dung, nhưng không có Express source/accepted contracts/tests; không executable-ready | **BLOCKED** source-baseline discovery và readiness |

Không gắn PASS chỉ vì file tồn tại. Ví dụ API hợp lệ cú pháp vẫn BLOCKED vì counter bắt buộc chưa có wire contract; Data có key pattern vẫn BLOCKED vì TTL/init/recovery chưa quyết định. Đây là kết quả critical review có chủ đích.

## Cross-document traceability và consistency

| BR | FR | API operations / reason N/A | Data | Architecture / migration |
|---|---|---|---|---|
| BR-100 | FR-100 | HTML UI ngoài JSON API | UI presentation | Next UI; UI regression parity |
| BR-101 | FR-101 | BLOCKED Q-101, không tự bịa route | ENT-100; key proposed, lifecycle Q-103 | Counter use case/Redis Port; MIG counter parity gated |
| BR-102 | FR-102/103 | getLiveness/getReadiness | Transient process/check fields | ADR-102; readiness failure sequence; parity matrix |
| BR-103 | FR-104 | getApplicationMetrics | Per-process derived series, no business history | ADR-104; parser/traffic parity |
| BR-104 | FR-105 | N/A packaging/config | Configuration không business entity | Current Docker vs proposed split, NFR-100/105, MIG staging |
| BR-105 | FR-106/107/108 | N/A internal browser demo ADR-101 | ENT-101/102/103 | Simulator/reducer, no server writer or AI execution |
| BR-106 | FR-109/110/111 | N/A scene/recent UI | Snapshot-derived poses, transient recent buffer | Scene adapter ADAPT, mapper BUILD; frontend regression |
| BR-107 | No active FR | Optional deferred | No retained source/replay contract | SSE/2D/history/filter excluded from candidate topology |
| BR-108 | No active FR | Future deferred | No real provider/user/session data | MIG feasibility only, not course acceptance |

State enum chung idle/working/completed/failed; Task status riêng running/completed/failed. API operational schema không có agent enum vì không có agent HTTP resource. UTC strings ở API/domain; reference ts epoch milliseconds không được copy. Terminal agent/task/ref consistency do RULE-105 sở hữu. Buffer transient không claim retained history. Redis counter atomic increment không claim exactly-once/durability. NFR-100..106 đều có realization hoặc explicit gap tại Architecture; Migration bảo toàn chúng sau khi baseline accepted.

## Scope, architecture findings và contradictions

| ID | Claim sources | Expected vs observed / impact | Smallest correction / owner |
|---|---|---|---|
| C-100 | E-100/E-101 vs E-102/E-103 | Express intended nhưng source Next only. Không thể nói current Express hoặc migration-ready | Discovery + Q-108 topology; Web owner, không sửa code trong test |
| C-101 | E-101 Node 24 vs E-102/E-104 Node 26.13.0 | Runtime documentation/config khác nhau, không chứng minh runtime support/build | Platform+Web reconcile ở nhiệm vụ implementation khác |
| C-102 | README database namespace vs root kustomization production-app | Host/policy design không được suy từ README diagram | Platform xác nhận actual rendered/deployed topology; giữ docs test phân current/configured |
| C-103 | WBS 2.4 done và current /ready | Contract “done” source-stated nhưng ready chỉ always 200, chưa Redis app client | Chốt acceptance criteria/dependency policy; Web+QA+Platform |

A-100: browser-local simulator đủ cho conditional MVP là **Assumption/proposed**, không phải business decision đã duyệt. ADR-100..104 trong Architecture và ADR-105 trong Migration là **Decisions/proposed**, không accepted. Facts ở evidence table không được chuyển thành implementation-tested. Questions dưới đây vẫn **Open**.

Scope creep đã chặn: real agent execution/CLI/session integrations, provider account handling, auth/multi-user, server task mutation, event ingestion, Redis broker, SSE/replay, full city/seasonal life và migration work. Những mục này không trở thành mandatory do My Office có code.

## Reuse conclusions

[07-reference-analysis.md](07-reference-analysis.md) có source index, Mermaid data flow và matrix 13 nhóm. Đề xuất REUSE chỉ pure helpers sau extraction/notice; ADAPT chibi/basic poses, subset desk scene, camera/renderer và selective performance techniques; BUILD own state mapper, browser simulator/reducer/UI và Redis counter; SKIP real-session backend, CLI/hooks/account/vault/undo cùng extras.

MIT source notice đã đọc, nhưng third-party vehicle/brand/vendor/font permissions cần kiểm theo artifact. Source-stated asset provenance không là blanket license clearance. Không thực hiện reuse/copy source trong practical test.

## Missing requirements và open questions — canonical registry

| Q | Missing decision / alternatives | Affected artifacts / gate | Resolution role / status |
|---|---|---|---|
| Q-100 | Ai duyệt release/rubric? Chọn mandatory-only hay mandatory + proposed office extension? | BRD/FRD extension selection, all baseline approvals | Người dùng/Web owner + nhóm; OPEN |
| Q-101 | Visit là page view, navigation hay unique visitor? refresh/bots/preload/probe exclusions, trigger, retry/idempotency và accepted ambiguous-timeout behavior? | FR-101/AC-101/102, counter API/storage; blocker | Web owner + QA; OPEN |
| Q-102 | Ai được đọc UI/probes/metrics? Network exposure, origins/CORS, secrets nếu có? | API access/security, architecture integration; blocker trước deploy | Web + Platform; OPEN; auth feature vẫn Future |
| Q-103 | Counter key scope/init authority/reset, TTL vs no expiry, eviction/persistence, backup/restore, max value/wire encoding, RPO/RTO? | Data ENT-100, API counter, migration recovery; blocker | Web + Platform; OPEN |
| Q-104 | Supported hardware/browser/load, latency/FPS/memory targets, Redis check depth/deadline, shutdown/drain/time limits? | FRD NFRs, target topology/resource fit, recovery gates | Web + QA + Platform; OPEN |
| Q-105 | Accessibility/keyboard standard và thiết bị mục tiêu? Chọn optional 2D fallback hay chỉ text dashboard? | NFR-106/scene AC coverage | Web owner + QA; OPEN; không tự chọn optional |
| Q-106 | Metric vocabulary/units/labels/counter inclusion, scrape path access và consumer integration? | FR-104, API metrics/Architecture/Migration | Web + QA/Observability + Platform; OPEN |
| Q-107 | Simulator scenario/cadence, terminal display/reset control, string/run/task/buffer limits? | Conditional demo rules/Data/AC-112/FR-111 | Web owner; OPEN; không bịa retention/capacity |
| Q-108 | Next vs separate Express ownership/deployable/routing/ports/probes? Future migration business case, source ref, target version, window/rollback authority? | Architecture/packaging; MIG-100 and cutover gates | Web + Platform + người dùng; OPEN |

Chưa có câu trả lời không ngăn giao draft có gaps; các câu này ngăn promotion thành official/accepted contracts. Không dùng elapsed time hoặc việc tạo file như approval.

## Executed validation và finding register

Tooling validation cài riêng trong thư mục tạm, không đổi app/package.json, lockfile hoặc repository source. Lần tải đầu sandbox bị chặn mạng; đã xin escalation cho pip download. Sandbox không đọc được package folder do quyền truy cập, nên kiểm định read-only được chạy có escalation. Cả hai bước chỉ phục vụ kiểm định tài liệu, không chạy code từ reference. pip báo các dependency conflicts của môi trường global có sẵn; packages được cài `--target` tạm, không chủ đích sửa global/app dependencies.

| ID | Check / severity | Locations + version / expected vs observed | Impact | Correction / owner | Result / follow-up |
|---|---|---|---|---|---|
| VAL-110 | Syntax/spec/examples / major | PT-API 0.1.0: PyYAML 6.0.3 parse; openapi-spec-validator 0.9.0 validate; jsonschema 4.26.0 Draft202012+format checking; 6 local refs resolved; 6 response examples validated | Contract supported subset mechanically valid | No correction required / reviewer | PASS; không chứng minh runtime/security hoặc Prometheus text semantics |
| VAL-111 | Traceability/content / major | PT-BRD/FRD/API/ARCH/DATA/MIG 0.1.0: manual semantic review + structural checks | BR parents/scope, operation FR links, types/null/time/enum và NFR controls phù hợp | Keep blocked counter scope explicit / Web reviewer | PASS supported links; completeness BLOCKED Q-101 |
| VAL-112 | Branch/edit preservation / blocker | E-107 pre/post hashes và final changed-file inventory | Chỉ tám new files trong practical-test, giữ prior validation/app/infra | Recheck final filesystem boundary / reviewer | Kết quả cuối ghi tại verification record bên dưới |
| VAL-113 | Runtime/diagram rendering / major | Không build/run app/reference, không deploy, không render Mermaid | Không claim AC/NFR/performance/deployment passed | Run trong nhiệm vụ implementation/QA sau / owners | BLOCKED runtime evidence; diagram rendering chưa thực hiện |

Các findings VAL-100..109/114..116 ở canonical documents vẫn active; không tái dùng VAL-01..18 của bộ test cũ. API validation không kiểm Prometheus exposition bằng parser chuyên dụng: string example schema pass không tương đương scrape compatibility tested. RefResolver của jsonschema phát deprecation warning, không làm validation fail; tooling improvement đề xuất chuyển sang referencing API.

### Verification record

Kết quả đã chạy trên workspace ngày 2026-11-05:

- Branch vẫn `ba/documentation`, HEAD không đổi so với E-107.
- SHA-256 của **71 existing files** khớp pre-write snapshot; bao gồm prior validation results, app source và infrastructure/config đã có. Không có file cũ bị xóa hoặc đổi nội dung.
- **Đúng 8 file mới**, tất cả dưới `docs/web-app/validation/practical-test/`; cả 8 có trạng thái DRAFT, không còn template placeholders, code fences cân bằng.
- **12 FR** có parent thuộc **9 BR** hợp lệ; ba operationIds unique theo API validator output, mỗi operation gắn FR đúng HTTP behavior. Các BR optional/future có deferment rõ, không bị chấm là active coverage thiếu.
- Tất cả local Markdown file links resolve được. Có **7 Mermaid blocks** được kiểm tra text/boundary semantics; chưa render, không claim visual syntax/layout QA PASS.
- `git diff --check` exit 0; vì files mới còn untracked, lệnh này chỉ kiểm tracked diff. UTF-8 content, fences, placeholders, links, trace rows và edit boundary của files mới được kiểm bằng Python riêng, không dựa vào lệnh đó để chứng nhận untracked files.
- `git status --short` vẫn hiển thị `?? docs/` như baseline, nên đã dùng filesystem hash + new-file inventory để phân biệt đúng tám outputs mới, không chỉ nhìn git status tổng quát.
- My Office LICENSE/package ở pinned commit được fetch lại và content khớp các reads main ban đầu; các sâu source reads dùng pinned ref.

VAL-112 = **PASS preservation/edit boundary**. VAL-110 = **PASS supported OpenAPI subset**, VAL-111 = **PASS supported links/semantics với completeness BLOCKED**, VAL-113 vẫn **BLOCKED runtime evidence / chưa render diagrams**. Các khoảng trống nghiệp vụ/implementation không được đóng bằng mechanical checks.

## Recommendations cho Skills và vòng review tiếp theo

1. Giữ separation giữa knowledge/provenance/scope/commitment/implementation. Nó giúp phát hiện intended Express/current Next và configured Redis/client absent thay vì điền template thành facts.
2. Bổ sung fixture “optional features được liệt kê rõ nhưng chưa selected”, assert downstream không sinh SSE/auth/task APIs. Fixture reference lớn nên test adapter/build/skip reasoning thay vì copy inventory thành FRs.
3. API skill nên có nhánh partial-contract coverage ledger, thể hiện unresolved security trong OpenAPI tooling vốn có thể render unsecured, và validator harness với negative examples. Không biến omitted security thành public-access approval.
4. Data skill nên có fixture counter timeout-after-write/missing-key-after-eviction, JS/PHP numeric encoding và namespace prefix; require explicit unknown TTL khác no-expiry. Browser transient vs Redis shared state cần được kiểm chéo.
5. Architecture skill nên có integration gate khi planned separate backend mâu thuẫn standalone Next packaging; require frontend và backend health ownership, tránh health backend bị dùng làm proof frontend.
6. Migration skill giữ BLOCKED discovery/readiness khi source framework absent; bổ sung test post-cutover writes và unsafe data rollback. Chấm plan completeness tách execution readiness.
7. Reference-review workflow cần asset provenance matrix có verified/source-stated/unverified, pin commit, và phân biệt source MIT với third-party vendor/font/brand rights. Static controls không phải security certification.
8. Vòng đánh giá tiếp theo: natural-language trigger/boundary tests trong fresh sessions, human semantic review, render Mermaid, contract runtime fixtures và approved NFR measurements. Chưa thực hiện những đánh giá này; không suy explicit test pass thành routing benchmark pass.

Không sửa Skills trong bài test. Trước chuyển official: người dùng review Q-100..108, chọn release, chốt counter/access/data lifecycle/topology; sau đó revise canonical drafts đồng bộ và thực thi QA có evidence. Bộ hiện tại **chưa sẵn sàng nghiệm thu**.
