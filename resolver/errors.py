"""Errors"""

import typing


class ResolverError(Exception):
    """Resolver generic error."""


class NotEnoughLettersError(ResolverError):
    """Not enough letters error compossing message."""

    def __init__(
        self,
        msg: str,
        missings: typing.Dict[str, typing.Tuple[int, typing.List[int]]],
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)
        self.missings = missings
