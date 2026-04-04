from enum import IntEnum


class SpeedLevel(IntEnum):
    VERY_SLOW = 1
    SLOW = 2
    NORMAL = 3
    FAST = 4
    TURBO = 5

    @property
    def factor(self):
        mapping = {
            SpeedLevel.VERY_SLOW: 0.005,
            SpeedLevel.SLOW:      0.01,
            SpeedLevel.NORMAL:    0.02,
            SpeedLevel.FAST:      0.04,
            SpeedLevel.TURBO:     0.06
        }
        return mapping[self]
