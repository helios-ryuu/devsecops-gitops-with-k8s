// Native Bun YAML parsing only. No package install, network, app or cluster call.
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const api = Bun.YAML.parse(readFileSync(resolve(here, 'smoke/api-contract.yaml'), 'utf8'));
const raw = readFileSync(resolve(here, 'kustomize-render.yaml'), 'utf8');
const resources = raw.split(/^---\s*$/m).filter(s => s.trim()).map(s => Bun.YAML.parse(s));
console.log(JSON.stringify({ runtime: `Bun ${Bun.version}`, api, resources }));
