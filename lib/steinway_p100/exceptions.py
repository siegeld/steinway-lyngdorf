"""Custom exceptions for Steinway P100 library."""


class SteinwayError(Exception):
    """Base exception for all Steinway P100 errors."""
    pass


class ConnectionError(SteinwayError):
    """Connection-related errors."""
    pass


class CommandError(SteinwayError):
    """Command execution errors."""
    pass


class TimeoutError(SteinwayError):
    """Operation timeout errors."""
    pass


class ResponseError(SteinwayError):
    """Invalid response errors."""
    pass