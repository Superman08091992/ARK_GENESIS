from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from .exceptions import ContractViolation

class CubeFace(str, Enum):
    CONCIPERE = 'concipere'
    REALISER = 'realiser'
    ACTUARE = 'actuare'
    RECONNOISTRE = 'reconnoistre'
    RECOLLIGERE = 'recolligere'
    SUUS_AFFERMEN = 'suus-affermen'
    CONSERVARE = 'conservare'

@dataclass(frozen=True)
class CubeState:
    cube_id: str
    active_face: CubeFace
    state_ref: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self):
        if not self.cube_id:
            raise ContractViolation('cube_id is required')
        if not isinstance(self.active_face, CubeFace):
            raise ContractViolation('active_face must be CubeFace')
        if not self.state_ref:
            raise ContractViolation('state_ref is required')
        return self

    def as_dict(self):
        return {'cube_id': self.cube_id, 'active_face': self.active_face.value, 'state_ref': self.state_ref, 'metadata': dict(self.metadata)}
