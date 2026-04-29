#!/usr/bin/env python3
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FILES=(
 'manifest.json','version.json','doctrine/oda.yaml','doctrine/cube.yaml','doctrine/authority.yaml','doctrine/checkpoints.yaml','doctrine/operation_envelope.yaml',
 'faces/concipere.yaml','faces/realiser.yaml','faces/actuare.yaml','faces/reconnoistre.yaml','faces/recolligere.yaml','faces/suus-affermen.yaml','faces/conservare.yaml',
 'memory/procedural_core.yaml','memory/identity_core.yaml','phoenix/phoenix.yaml','phoenix/revival_rules.yaml','phoenix/reseed_protocol.yaml',
 'schemas/cube.schema.json','schemas/oda.schema.json','schemas/checkpoint.schema.json','schemas/identity_core.schema.json','schemas/procedural_core.schema.json')

@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: tuple
    def raise_for_errors(self):
        if not self.ok:
            raise SystemExit('\n'.join(self.errors))

def _load_json(path: Path):
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict):
        raise ValueError(str(path)+': expected JSON object')
    return data

def validate_graveyard(root: Path) -> ValidationResult:
    errors=[]
    graveyard=root/'opt'/'ark'/'graveyard'
    if not graveyard.exists():
        return ValidationResult(False,(f'missing graveyard root: {graveyard}',))
    for rel in REQUIRED_FILES:
        path=graveyard/rel
        if not path.exists():
            errors.append('missing required file: '+rel)
        elif path.is_file() and path.stat().st_size==0:
            errors.append('empty required file: '+rel)
    for rel in ('manifest.json','version.json'):
        path=graveyard/rel
        if path.exists():
            try:
                if 'schema_version' not in _load_json(path): errors.append(rel+': missing schema_version')
            except Exception as exc: errors.append(str(exc))
    for rel in ('schemas/cube.schema.json','schemas/oda.schema.json','schemas/checkpoint.schema.json','schemas/identity_core.schema.json','schemas/procedural_core.schema.json'):
        path=graveyard/rel
        if path.exists():
            try:
                if _load_json(path).get('type')!='object': errors.append(rel+': expected type=object')
            except Exception as exc: errors.append(str(exc))
    return ValidationResult(not errors, tuple(errors))

def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv)
    root=Path(args[0]).resolve() if args else Path.cwd()
    result=validate_graveyard(root)
    if result.ok:
        print('graveyard validation ok')
        return 0
    for error in result.errors: print(error,file=sys.stderr)
    return 1

if __name__=='__main__':
    raise SystemExit(main())
