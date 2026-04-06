class ConfigError(Exception):
    pass


class ZoneFormatError(ConfigError):
    pass


class ZoneValueError(ConfigError):
    pass


class DroneValueError(ConfigError):
    pass


class ConnectionError(ConfigError):
    pass
