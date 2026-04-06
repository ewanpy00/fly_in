from enum import Enum
from typing import Dict


class ZoneType(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

    @property
    def cost(self) -> float:
        mapping: Dict[ZoneType, float] = {
            ZoneType.NORMAL: 1.0,
            ZoneType.RESTRICTED: 2.0,
            ZoneType.PRIORITY: 0.5,
            ZoneType.BLOCKED: float('inf')
        }
        return mapping[self]
