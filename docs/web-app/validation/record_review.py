"""Append draft review corrections while preserving original creation/upstream hashes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

here = Path(__file__).resolve().parent
log_path = here / 'execution-log.json'
log = json.loads(log_path.read_text(encoding='utf-8'))
assert not log.get('review_revisions'), 'Review corrections already recorded; do not overwrite history'
reasons = {
    'smoke/architecture.md': 'QA first run found no explicit Validation heading; add heading without changing technical meaning.',
    'smoke/migration-plan.md': 'QA first run found abbreviated parity IDs; expand AC/ENT references to complete stable IDs.'}
revisions = []
for output, reason in reasons.items():
    original = next(s['output']['sha256'] for s in log['steps'] if s['output']['path'] == output)
    final = hashlib.sha256((here / output).read_bytes()).hexdigest()
    assert original != final, 'Expected review correction for ' + output
    revisions.append({'path': output, 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                      'version': '0.1.0', 'status': 'draft', 'sha256_before': original, 'sha256_after': final,
                      'reason': reason, 'initial_check_report': 'document-checks.initial.json',
                      'impact': 'Draft clarity/traceability; no source, contracts, commitments or technical behavior changed.'})
log['review_revisions'] = revisions
log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Recorded two draft QA corrections; preserved original step hashes.')
