__author__ = 'duydo'


class MapzenError(Exception):
    """MapzenError exception"""

    def __init__(self, reason=None, status_code=None, response=None):
        self.reason = reason
        self.status_code = status_code
        self.response = response
        super(MapzenError, self).__init__(reason)

    def __str__(self):
        return self.reason


class MapzenRateLimitError(MapzenError):
    """Exception for Mapzen hitting the rate limit."""
    pass
