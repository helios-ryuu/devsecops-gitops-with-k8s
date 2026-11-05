"""Read-only project/skill evidence capture; writes only this validation directory."""
from pathlib import Path
import hashlib
import json
import subprocess
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SKILLS_REPO = Path('C:/Users/84352/.agents/skills/business-analyst-skill')
NAMES = ['brd-authoring', 'frd-authoring', 'api-contract-design',
         'architecture-design', 'data-contract-design', 'backend-migration-planning']

def git(*args, cwd=ROOT):
    p = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_new(name, value):
    with (HERE / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

source_paths = {
    'E-01': ['README.md'],
    'E-02': ['WBS.md'],
    'E-03': ['app/package.json', 'app/pnpm-lock.yaml'],
    'E-04': ['app/src/app/page.tsx', 'app/src/app/layout.tsx'],
    'E-05': ['app/src/app/healthz/route.ts'],
    'E-06': ['app/src/app/ready/route.ts'],
    'E-07': ['app/next.config.ts', 'app/Dockerfile'],
    'E-08': ['k8s-manifests/base/configmap.yaml', 'k8s-manifests/base/deployment.yaml'],
    'E-09': ['k8s-manifests/database/redis.yaml'],
    'E-10': ['k8s-manifests/kustomization.yaml', 'k8s-manifests/base/kustomization.yaml',
             'k8s-manifests/database/kustomization.yaml', 'k8s-manifests/security/kustomization.yaml',
             'k8s-manifests/security/network-policy.yaml'],
    'E-11': ['argocd/app.yaml'],
}
files = {}
for evidence_id, paths in source_paths.items():
    files[evidence_id] = []
    for rel in paths:
        p = ROOT / rel
        item = {'path': rel, 'sha256': digest(p), 'git_blob': git('hash-object', '--', rel)}
        # The lockfile is represented by its hash; readable excerpts focus on direct dependencies.
        if not rel.endswith('pnpm-lock.yaml'):
            item['lines'] = [{'line': n, 'text': s} for n, s in enumerate(p.read_text(encoding='utf-8').splitlines(), 1)]
        files[evidence_id].append(item)

tracked = git('ls-files').splitlines()
skill_files = {}
for p in sorted((SKILLS_REPO / 'skills').rglob('*')):
    if p.is_file():
        rel = p.relative_to(SKILLS_REPO).as_posix()
        skill_files[rel] = {'sha256': digest(p), 'git_blob': git('hash-object', '--', rel, cwd=SKILLS_REPO),
                            'head_blob': git('rev-parse', 'HEAD:' + rel, cwd=SKILLS_REPO)}

write_new('evidence.json', {
    'captured_at_utc': datetime.now(timezone.utc).isoformat(),
    'inspection_date': '2026-11-05',
    'project': {'remote': git('remote', 'get-url', 'origin'), 'branch': git('branch', '--show-current'),
                'head': git('rev-parse', 'HEAD'), 'origin_main': git('rev-parse', 'origin/main'),
                'main': git('rev-parse', 'main'), 'worktrees': git('worktree', 'list', '--porcelain')},
    'initial_git_observation': {
        'provenance': 'agent observation of tool output before writes; not a saved terminal transcript',
        'status': '## main...origin/main; no changed/untracked paths',
        'branch_before': 'main', 'ba_documentation_existed': False,
        'fetch': 'git fetch origin main; successful after .git/FETCH_HEAD permission escalation',
        'switch': 'git switch -c ba/documentation origin/main; exit 0'},
    'skill_bundle': {'remote': git('remote', 'get-url', 'origin', cwd=SKILLS_REPO),
                     'head': git('rev-parse', 'HEAD', cwd=SKILLS_REPO),
                     'working_tree_status': git('status', '--short', cwd=SKILLS_REPO),
                     'skills_diff': git('diff', '--name-only', 'HEAD', '--', 'skills', cwd=SKILLS_REPO),
                     'files': skill_files,
                     'limit': 'External repository has pre-existing edits outside skills; not changed here. No latest-remote-bundle assertion.'},
    'sources': files,
    'tracked_baseline_sha256': {rel: digest(ROOT / rel) for rel in tracked if (ROOT / rel).is_file()},
    'limits': ['Code observed, no application execution or cluster access.',
               'No credentials, TLS secret files or production state captured.',
               'Baseline hashes prove content scope only, not runtime feature readiness.']})

# This is a transcribed runtime catalog observation, independent of reading SKILL.md.
# It is deliberately not labeled a raw API or /skills export.
descriptions = {
    'brd-authoring': 'Create, refine or review a software/product Business Requirements Document (BRD) from business problems, goals, stakeholders and scope. Use for business requirements and release boundaries, not detailed FRD behavior or analytical study documentation.',
    'frd-authoring': 'Create, refine or review a Functional Requirements Document (FRD), system behaviors, business rules and acceptance criteria traced to business requirements. Use for functional specifications and measurable NFRs, not BRD framing, API schemas or analytical study requirements.',
    'api-contract-design': 'Design, revise or review a framework-independent OpenAPI 3.x HTTP API contract from functional requirements, including wire schemas, validation, errors and streaming behavior when required. Use for api-contract.yaml, not controller implementation or data storage design.',
    'architecture-design': 'Create, update or review architecture.md describing components, integrations, deployment, Mermaid diagrams and how design satisfies NFRs. Use for technical architecture documentation and trade-offs, not application implementation or infrastructure changes.',
    'data-contract-design': 'Create, refine or review data-contract.md for application entities, API-to-storage mappings, lifecycle, TTL and consistency, including Redis keys when Redis is used. Use for application data contracts, not analytical metric specifications, data analysis or database implementation.',
    'backend-migration-planning': 'Create, update or review migration-plan.md for replacing a backend runtime/framework, especially Express to Laravel, while preserving business behavior, OpenAPI and Data contracts. Use for parity, staged cutover and rollback planning, not executing migrations or redesigning product scope.'}
write_new('runtime-discovery.json', {
    'evidence_id': 'E-12', 'result': 'PASS', 'scope': 'Runtime catalog discovery in the current session only',
    'provenance': 'The developer-provided Available skills catalog was observed before manifest reads. This agent-authored transcription was saved later; it is not a raw registry export.',
    'raw_export_available': False, 'count': 6,
    'skills': [{'name': n, 'description': descriptions[n],
                'path': (SKILLS_REPO / 'skills' / n / 'SKILL.md').as_posix()} for n in NAMES],
    'fresh_session_explicit_invocation': 'BLOCKED: no independent harness run in this task',
    'implicit_selection_eval': 'BLOCKED: current task explicitly requests all six; not a blind routing evaluation',
    'not_proof': ['Reading SKILL.md alone', 'Prior validation reports in the bundle', 'Fixture checks alone']})
print(json.dumps({'captured_sources': len(files), 'skills': len(NAMES), 'branch': git('branch', '--show-current')}, ensure_ascii=False))
