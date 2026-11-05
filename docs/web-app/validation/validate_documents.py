"""Targeted BA document checks; not a general OpenAPI/TS parser or semantic evaluator.

Reads project and bundle without modifying them. Reports are written only beside
this script. Negative cases mutate in-memory copies, never project documents.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import copy
import hashlib
import json
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NAMES = ['brd-authoring', 'frd-authoring', 'api-contract-design',
         'architecture-design', 'data-contract-design', 'backend-migration-planning']
FILES = ['BRD.md', 'FRD.md', 'api-contract.yaml', 'architecture.md', 'data-contract.md', 'migration-plan.md']
checks = []

def check(name, fn, scope='artifact/static'):
    try:
        detail = fn()
        checks.append({'name': name, 'result': 'PASS', 'scope': scope, 'detail': detail or 'condition checked'})
    except Exception as exc:
        checks.append({'name': name, 'result': 'FAIL', 'scope': scope, 'detail': str(exc)})

def expect(value, detail):
    if not value:
        raise AssertionError(detail)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return (HERE / name).read_text(encoding='utf-8-sig')

def git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    expect(p.returncode == 0, p.stderr)
    return p.stdout.strip()

def table(text, first_column):
    lines = text.splitlines()
    def cells(line):
        return [x.strip() for x in line.strip().strip('|').split('|')]
    for i, line in enumerate(lines):
        if line.startswith('| ') and cells(line)[0] == first_column:
            header = cells(line)
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith('|'):
                    break
                values = cells(row)
                expect(len(values) == len(header), 'Malformed table row: ' + row)
                rows.append(dict(zip(header, values)))
            return rows
    raise AssertionError('Missing table ' + first_column)

def operations(api):
    return [dict(path=path, method=method, **op) for path, item in api['paths'].items()
            for method, op in item.items() if method in ['get', 'put', 'post', 'delete', 'patch', 'head', 'options']]

def deref(api, ref):
    expect(ref.startswith('#/'), 'Only local JSON pointers supported')
    value = api
    for token in ref[2:].split('/'):
        value = value[token.replace('~1', '/').replace('~0', '~')]
    return value

def check_refs(api, item):
    if isinstance(item, dict):
        if '$ref' in item:
            deref(api, item['$ref'])
        for value in item.values():
            check_refs(api, value)
    elif isinstance(item, list):
        for value in item:
            check_refs(api, value)

def sample_errors(api, schema, value):
    if '$ref' in schema:
        return sample_errors(api, deref(api, schema['$ref']), value)
    supported = {'type', 'properties', 'required', 'additionalProperties', 'enum', 'minimum', 'format', 'pattern', 'description'}
    expect(not set(schema) - supported, 'Unsupported schema keywords: ' + str(set(schema) - supported))
    errors = []
    kind = schema.get('type')
    matches = (kind == 'object' and isinstance(value, dict)
               or kind == 'string' and isinstance(value, str)
               or kind == 'number' and isinstance(value, (int, float)) and not isinstance(value, bool))
    if not matches:
        return ['type mismatch']
    if 'enum' in schema and value not in schema['enum']:
        errors.append('enum mismatch')
    if kind == 'number' and value < schema.get('minimum', float('-inf')):
        errors.append('minimum violation')
    if kind == 'string':
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append('pattern violation')
        if schema.get('format') == 'date-time':
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    errors.append('timezone missing')
            except ValueError:
                errors.append('invalid date-time')
    if kind == 'object':
        for name in schema.get('required', []):
            if name not in value:
                errors.append('required field missing: ' + name)
        for name, child in value.items():
            if name in schema.get('properties', {}):
                errors.extend(sample_errors(api, schema['properties'][name], child))
            elif schema.get('additionalProperties') is False:
                errors.append('unknown field: ' + name)
    return errors

baseline = json.loads(read('evidence.json'))
catalog = json.loads(read('runtime-discovery.json'))
log = json.loads(read('execution-log.json'))
texts = {name: read('smoke/' + name) for name in FILES if name.endswith('.md')}

def git_scope():
    expect(git('branch', '--show-current') == 'ba/documentation', 'Wrong branch')
    for ref in ['HEAD', 'main', 'origin/main']:
        expect(git('rev-parse', ref) == baseline['project']['head'], 'Unexpected ref change: ' + ref)
    for rel, digest in baseline['tracked_baseline_sha256'].items():
        expect((ROOT / rel).is_file() and sha(ROOT / rel) == digest, 'Tracked content changed: ' + rel)
    expect(not git('diff', '--name-only', 'HEAD'), 'Tracked diff exists')
    # Keep leading status spaces; strip() would destroy porcelain's two-column status.
    p = subprocess.run(['git', 'status', '--porcelain=v1', '--untracked-files=all'], cwd=ROOT,
                       capture_output=True, text=True, encoding='utf-8', check=True)
    for line in p.stdout.splitlines():
        expect(line[3:].replace('\\', '/').startswith('docs/web-app/validation/'), 'Out-of-scope path: ' + line)
    return 'Baseline tracked hashes unchanged; all changed/untracked paths inside docs/web-app/validation; refs remain pinned.'

check('Git branch, base and documentation-only content scope', git_scope, 'repository safety')

def runtime_metadata():
    expect(catalog['count'] == 6 and {x['name'] for x in catalog['skills']} == set(NAMES), 'Catalog mismatch')
    expect(all(x['description'] and x['path'] for x in catalog['skills']), 'Missing runtime metadata')
    expect(catalog['raw_export_available'] is False, 'Provenance claim changed')
    return 'Recorded catalog advertises six skills; this check validates the transcribed record, not a new discovery query.'

check('Current-session runtime catalog record is complete and qualified', runtime_metadata, 'record integrity; not independent discovery')

def bundle_identity():
    root = Path(catalog['skills'][0]['path']).parents[2]
    for rel, item in baseline['skill_bundle']['files'].items():
        expect(sha(root / rel) == item['sha256'], 'Bundle changed: ' + rel)
        expect(item['git_blob'] == item['head_blob'], 'Captured skill differed from HEAD: ' + rel)
    return 'Captured bundle skill/template/shared files match pinned HEAD and remain unchanged.'

check('Bundle pin and skill file integrity', bundle_identity)

def sequence():
    expect([s['skill'] for s in log['steps']] == NAMES, 'Wrong application sequence')
    revisions = {r['path']: r for r in log.get('review_revisions', [])}
    def current_hash(path, captured_hash):
        revision = revisions.get(path)
        if revision:
            expect(revision['sha256_before'] == captured_hash and revision['reason'], 'Invalid documented revision: ' + path)
            return revision['sha256_after']
        return captured_hash
    for i, step in enumerate(log['steps']):
        expect(step['sequence'] == i + 1, 'Bad sequence number')
        out = step['output']
        expect(sha(HERE / out['path']) == current_hash(out['path'], out['sha256']), 'Output hash drift: ' + out['path'])
        expect(len(step['upstream_outputs']) == i, 'Missing recorded upstream')
        for item in step['upstream_outputs']:
            expect(sha(HERE / item['path']) == current_hash(item['path'], item['sha256']), 'Upstream hash drift: ' + item['path'])
    return 'Six guided steps, BRD first; creation/upstream hashes preserved and final artifacts match documented draft review revisions. Not an independent harness trace.'

check('Guided sequential application log and upstream artifacts', sequence)

def metadata():
    for name, body in texts.items():
        rows = table(body, 'Document ID')
        expect(rows[0]['Version'] == '0.1.0' and rows[0]['Status'] == 'draft', 'Control mismatch: ' + name)
        expect('2026-11-05' in rows[0]['Date'] and 'SANDBOX' in body, 'Date/sandbox missing: ' + name)
        for phrase in ['Change log', 'Validation']:
            expect(phrase.lower() in body.lower(), 'Missing ' + phrase + ': ' + name)
        expect('[registry]' in body or '[Nguồn và questions]' in body, 'No evidence registry link: ' + name)
        expect('{{' not in body and '}}' not in body, 'Template placeholder: ' + name)
    return 'Five Markdown smoke outputs have draft/version/date/owner/source/upstream/change/validation controls; API checked separately.'

check('Smoke Markdown document controls and unresolved questions visible', metadata)

def links_and_tables():
    for p in HERE.rglob('*.md'):
        body = p.read_text(encoding='utf-8')
        for line in body.splitlines():
            if line.startswith('| '):
                expect(line.endswith('|'), 'Malformed table boundary: ' + p.name)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', body):
            target = target.split('#')[0]
            if not target or re.match(r'^[a-z]+:', target, re.I):
                continue
            expect((p.parent / target).resolve().exists(), 'Broken local link: ' + str(p) + ' -> ' + target)
    return 'All local Markdown link targets exist; table rows used by this checker parse. No rendered-layout claim.'

check('Local links and table boundaries', links_and_tables)

parsed = None
def parse_yaml():
    global parsed
    bun = shutil.which('bun.cmd') or shutil.which('bun')
    expect(bun, 'Bun not available')
    run = subprocess.run([bun, 'run', str(HERE / 'parse_documents.mjs')], cwd=ROOT,
                         capture_output=True, text=True, encoding='utf-8')
    expect(run.returncode == 0, run.stderr)
    parsed = json.loads(run.stdout)
    return parsed['runtime'] + ': parsed OpenAPI draft and captured offline Kustomize YAML; not a full OpenAPI validator.'

check('YAML parser executes on actual NT548 artifacts', parse_yaml, 'YAML syntax')
expect(parsed is not None, 'Cannot continue dependent artifact checks without YAML parsing')
api = parsed['api']

def api_structure():
    expect(api['openapi'] == '3.1.1', 'Unexpected dialect')
    expect(api['info']['version'] == '0.1.0' and api['x-document-control']['status'] == 'draft', 'Wrong API control')
    ops = operations(api)
    expect(len(ops) == 2 and len({o['operationId'] for o in ops}) == 2, 'Wrong operation inventory')
    expect({o['path'] for o in ops} == {'/healthz', '/ready'}, 'Unsupported added path')
    expect(all(o['method'] == 'get' and set(o['responses']) == {'200'} for o in ops), 'Observed route/status drift')
    expect(all(o['x-fr-ids'] and o['x-commitment'] == 'proposed' for o in ops), 'Missing FR/commitment')
    check_refs(api, api)
    for op in ops:
        response = op['responses']['200']
        expect(response['description'], 'Missing response description')
        media = response['content']['application/json']
        expect(not sample_errors(api, media['schema'], media['example']), 'Invalid response example')
    return 'Targeted structure/ref checks and two synthetic examples pass supported schema subset only.'

check('Partial OpenAPI structure, local refs and example validation', api_structure, 'targeted subset; not full OAS certification')

brs = {r['BR ID']: r for r in table(texts['BRD.md'], 'BR ID')}
frs = {}
for match in re.finditer(r'^### (FR-\d+) .+?\n(.*?)(?=^### FR-|^## |\Z)', texts['FRD.md'], re.M | re.S):
    section = match[2]
    parent = re.search(r'Parent: (BR-\d+)', section)
    expect(parent is not None, 'FR missing explicit parent')
    frs[match[1]] = {'parent': parent[1], 'section': section, 'commitment': 'proposed' if 'proposed' in section else 'unknown'}
maps = table(texts['data-contract.md'], 'Entity')
# The first Entity table has the field dictionary header. Entity inventory uses a
# different first header below to avoid mistaking identity rows for field mappings.
if 'Schema' not in maps[0]:
    lines = texts['data-contract.md'].splitlines()
    start = next(i for i, s in enumerate(lines) if s.startswith('| Entity | Schema |'))
    maps = table('\n'.join(lines[start:]), 'Entity')
controls = table(texts['architecture.md'], 'NFR / source version')
nfrs = table(texts['FRD.md'], 'NFR ID')
trace = table(read('traceability.md'), 'BR')

# Read only this small handler vocabulary. This is a targeted control-flow/source
# check for these two files, not a TypeScript AST parser or proof of HTTP behavior.
source_contracts = {}
for path, opid in [('healthz', 'getHealth'), ('ready', 'getReadiness')]:
    src = (ROOT / 'app/src/app' / path / 'route.ts').read_text(encoding='utf-8')
    fields = {}
    for name, expr in re.findall(r'^\s+(\w+): (.+),$', src, re.M):
        if expr.startswith('"'):
            fields[name] = {'type': 'string', 'enum': [json.loads(expr)]}
        elif expr == 'process.uptime()':
            fields[name] = {'type': 'number', 'minimum': 0}
        elif expr == 'new Date().toISOString()':
            fields[name] = {'type': 'string', 'format': 'date-time', 'pattern': 'Z$'}
        else:
            raise AssertionError('Unsupported handler expression: ' + expr)
    source_contracts[opid] = fields

model = {'api': api, 'brs': brs, 'frs': frs, 'maps': maps, 'controls': controls, 'nfrs': nfrs,
         'trace': trace, 'api_upstreams': api['x-document-control']['upstream-versions']}

def consistency_errors(m):
    errors = []
    for frid, fr in m['frs'].items():
        if fr['parent'] not in m['brs']:
            errors.append('orphan FR ' + frid)
        if fr['commitment'] != 'proposed':
            errors.append('unsupported commitment promotion ' + frid)
    ops = operations(m['api'])
    op_ids = {o['operationId'] for o in ops}
    for op in ops:
        for frid in op['x-fr-ids']:
            if frid not in m['frs']:
                errors.append('orphan operation ' + op['operationId'])
        if op['operationId'] not in source_contracts:
            errors.append('operation has no inspected source baseline')
            continue
        schema = deref(m['api'], op['responses']['200']['content']['application/json']['schema']['$ref'])
        expected = source_contracts[op['operationId']]
        if set(schema['properties']) != set(expected) or set(schema['required']) != set(expected):
            errors.append('source field/required mismatch ' + op['operationId'])
        for field, constraints in expected.items():
            for key, value in constraints.items():
                if schema.get('properties', {}).get(field, {}).get(key) != value:
                    errors.append('source constraint mismatch ' + field + '.' + key)
    for schema_name, schema in m['api']['components']['schemas'].items():
        rows = [r for r in m['maps'] if r.get('Schema') == schema_name]
        if {r['Field'] for r in rows} != set(schema['properties']):
            errors.append('unmapped wire field ' + schema_name)
        for row in rows:
            if 'transient' not in row['Lifecycle']:
                errors.append('transient report storage drift ' + row['Field'])
    for nfr in m['nfrs']:
        if not any(nfr['NFR ID'] in row['NFR / source version'] and row['Control'] and row['Gap'] for row in m['controls']):
            errors.append('missing NFR control/gap ' + nfr['NFR ID'])
    covered = set()
    for row in m['trace']:
        if row['BR'] not in m['brs']:
            errors.append('trace parent missing')
        covered.add(row['BR'])
        if row['FR'] != 'NONE' and (row['FR'] not in m['frs'] or m['frs'][row['FR']]['parent'] != row['BR']):
            errors.append('trace FR-parent disagreement')
        if row['Operations'] != 'NONE' and row['Operations'] not in op_ids:
            errors.append('trace operation missing')
        if row['Operations'] == 'NONE' and not row['Gap / non-software reason']:
            errors.append('missing coverage gap/disposition')
    if covered != set(m['brs']):
        errors.append('BR without coverage/disposition')
    if any(v != '0.1.0' for v in m['api_upstreams'].values()):
        errors.append('upstream version mismatch')
    return errors

check('BR/FR/operation/source/schema/Data/NFR/version trace slice',
      lambda: expect(not consistency_errors(model), '; '.join(consistency_errors(model))), 'cross-document structural and source subset')

def ids_and_parity():
    rules = {r['RULE ID'] for r in table(texts['FRD.md'], 'RULE ID')}
    acs = {r['AC ID'] for r in table(texts['FRD.md'], 'AC ID')}
    for op in operations(api):
        expect(set(op['x-rule-ids']) <= rules and set(op['x-ac-ids']) <= acs, 'Operation has missing RULE/AC')
    migration = texts['migration-plan.md']
    for key in [*brs, *frs, *rules, *acs, *(r['NFR ID'] for r in nfrs), 'ENT-01', 'ENT-02', 'ENT-03', 'getHealth', 'getReadiness']:
        expect(key in migration, 'Parity inventory missing ' + key)
    expect('Plan completeness: BLOCKED' in migration and 'Cutover readiness: BLOCKED' in migration,
           'Migration has unsupported readiness claim')
    return 'RULE/AC references resolve and migration names all invariants with not-run/gap status. Not proof of semantic/runtime parity.'

check('RULE/AC links and migration inventory/readiness limits', ids_and_parity)

def namespace_render():
    objs = parsed['resources']
    expect(len(objs) == 7, 'Unexpected rendered object inventory')
    expect(all(o['metadata']['namespace'] == 'production-app' for o in objs), 'Namespace drift')
    policy = next(o for o in objs if o['kind'] == 'NetworkPolicy')
    peer = policy['spec']['ingress'][0]['from'][0]
    expect(peer['podSelector']['matchLabels'] == {'app': 'web'} and 'namespaceSelector' not in peer, 'Policy selector drift')
    return 'Offline render: 7 resources in production-app, including Redis and NetworkPolicy; contradicts README database namespace claim. No live enforcement test.'

check('Offline Kustomize render confirms namespace/selector evidence', namespace_render, 'configuration evidence')

def no_dependency_fabrication():
    for name in ['healthz', 'ready']:
        src = (ROOT / 'app/src/app' / name / 'route.ts').read_text(encoding='utf-8')
        expect(not re.search(r'redis|fetch\(|503|prom-client', src, re.I), 'Probe implementation changed')
    expect('/metrics' not in api['paths'] and len(api['paths']) == 2, 'Invented operation')
    expect('TBD Q-05' in texts['data-contract.md'] and 'không phải null/no expiry' in texts['data-contract.md'], 'TTL unknown distinction lost')
    return 'Current handler evidence contains no dependency/error branch; missing business/metrics operations and unknown TTL remain explicit.'

check('Current probe semantics and unknown Redis contract remain bounded', no_dependency_fabrication)

def mutation(name, mutate):
    candidate = copy.deepcopy(model)
    mutate(candidate)
    expect(consistency_errors(candidate), 'Mutation escaped checker: ' + name)
    return 'Injected inconsistency detected in memory; files unchanged.'

mutations = [
    ('orphan FR parent', lambda m: m['frs']['FR-01'].update(parent='BR-99')),
    ('orphan API FR reference', lambda m: m['api']['paths']['/healthz']['get'].update({'x-fr-ids': ['FR-99']})),
    ('enum mismatch with handler', lambda m: m['api']['components']['schemas']['HealthReport']['properties']['status'].update(enum=['ready'])),
    ('number to string drift', lambda m: m['api']['components']['schemas']['HealthReport']['properties']['uptime'].update(type='string')),
    ('missing required field', lambda m: m['api']['components']['schemas']['HealthReport'].update(required=['status', 'timestamp'])),
    ('unmapped wire field', lambda m: m['api']['components']['schemas']['HealthReport']['properties'].update(extra={'type': 'string'})),
    ('timestamp UTC encoding drift', lambda m: m['api']['components']['schemas']['ReadinessReport']['properties']['timestamp'].update(pattern='[+-][0-9]{2}:[0-9]{2}$')),
    ('missing NFR control and gap', lambda m: m.update(controls=[])),
    ('transient field made persistent', lambda m: m['maps'][0].update(Lifecycle='Redis persisted')),
    ('upstream version drift', lambda m: m['api_upstreams'].update({'TEST-FRD': '0.2.0'})),
    ('unapproved FR commitment promotion', lambda m: m['frs']['FR-01'].update(commitment='accepted')),
]
for label, mutate in mutations:
    check('Negative: ' + label, lambda label=label, mutate=mutate: mutation(label, mutate), 'in-memory mutation detection')

health = api['components']['schemas']['HealthReport']
for label, sample in [
    ('invalid enum', {'status': 'ready', 'uptime': 1, 'timestamp': '2026-11-05T00:00:00Z'}),
    ('missing timestamp', {'status': 'ok', 'uptime': 1}),
    ('negative uptime', {'status': 'ok', 'uptime': -1, 'timestamp': '2026-11-05T00:00:00Z'}),
    ('invalid date', {'status': 'ok', 'uptime': 1, 'timestamp': 'not-a-dateZ'}),
    ('unexpected field', {'status': 'ok', 'uptime': 1, 'timestamp': '2026-11-05T00:00:00Z', 'redis': 'up'}),
]:
    check('Negative sample: ' + label,
          lambda sample=sample: expect(bool(sample_errors(api, health, sample)), 'Bad sample accepted'), 'schema subset sample rejection')

blocked = [
    ('Fresh-session explicit invocation', 'No independent harness run; current-session guided application only.'),
    ('Blind implicit skill routing', 'Prompt explicitly requested all six; no isolated routing evaluation.'),
    ('Full OpenAPI-aware validation', 'Default Python lacks yaml/jsonschema/openapi_spec_validator; Bun subset checks do not certify OAS.'),
    ('Mermaid rendering', 'Diagram source reviewed; no renderer executed.'),
    ('Application HTTP/Redis/load and live cluster', 'Code/config inspection and offline render only; no app/cluster mutation or runtime tests.'),
    ('Migration plan and cutover readiness', 'Express source, target decision, accepted baselines, recovery/parity evidence absent Q-04/Q-06.'),
]
for name, detail in blocked:
    checks.append({'name': name, 'result': 'BLOCKED', 'scope': 'not executed / evidence absent', 'detail': detail})

counts = Counter(x['result'] for x in checks)
for result in ['PASS', 'FAIL', 'BLOCKED']:
    counts.setdefault(result, 0)
report = {
    'run_at_utc': datetime.now(timezone.utc).isoformat(),
    'tool': 'Python stdlib + native Bun YAML parser; targeted checker written for this validation task',
    'counts': dict(counts), 'checks': checks,
    'limits': ['Same agent authored and reviewed artifacts; no independent semantic evaluator.',
               'Metadata/keyword/hash/targeted source checks cannot prove full cross-document semantics.',
               'Schema checker supports only keywords actually used; unsupported keywords fail, not silently pass.',
               'Expected source contradictions are reported separately in evidence-register/report, not counted as checker failures.',
               'No application execution, deployment, migration, external messaging or production access.'],
    'smoke_artifact_sha256': {name: sha(HERE / 'smoke' / name) for name in FILES},
}
(HERE / 'document-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'counts': dict(counts), 'failures': [x for x in checks if x['result'] == 'FAIL']}, ensure_ascii=False, indent=2))
raise SystemExit(1 if counts['FAIL'] else 0)
