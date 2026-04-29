import hashlib
import json
from typing import Any

def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def sha256_data(data: Any) -> str:
    return sha256_text(canonical_json(data))
