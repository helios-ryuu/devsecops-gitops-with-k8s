"""Record guided application, not an independent skill-invocation trace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ORDER = ['brd-authoring', 'frd-authoring', 'api-contract-design',
         'architecture-design', 'data-contract-design', 'backend-migration-planning']
OUTPUTS = ['BRD.md', 'FRD.md', 'api-contract.yaml', 'architecture.md', 'data-contract.md', 'migration-plan.md']
path = HERE / 'execution-log.json'
log = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
    'mode': 'guided sequential application by the same agent in this session',
    'provenance': 'agent-authored record; not independent model/harness trace',
    'time_semantics': 'recorded_at is recording time after output creation; not invocation latency',
    'steps': []}
i = len(log['steps'])
if i >= len(ORDER) or sys.argv[1:] != [ORDER[i]]:
    raise SystemExit('Expected next skill: ' + (ORDER[i] if i < len(ORDER) else 'none'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
output = HERE / 'smoke' / OUTPUTS[i]
assert output.is_file(), 'Output must exist before recording'
log['steps'].append({
    'sequence': i + 1, 'skill': ORDER[i], 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'prompt_case': 'T-' + str(i + 4).zfill(2),
    'runtime_catalog': 'runtime-discovery.json',
    'instructions': 'C:/Users/84352/.agents/skills/business-analyst-skill/skills/' + ORDER[i] + '/SKILL.md',
    'supporting_inputs': ['shared documentation-standard.md', 'per-skill asset template', 'evidence.json', 'evidence-register.md'],
    'upstream_outputs': [{'path': 'smoke/' + s, 'sha256': sha(HERE / 'smoke' / s)} for s in OUTPUTS[:i]],
    'output': {'path': 'smoke/' + OUTPUTS[i], 'sha256': sha(output)},
    'result_scope': 'Draft produced; conclusions and blocked checks are recorded in output/report, not inferred from file existence'
})
path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Recorded step ' + str(i + 1) + ': ' + ORDER[i])
