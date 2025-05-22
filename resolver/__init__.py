import typing
from resolver.inline import InlineResolver
from connections import spotify


__RESOLVERS_REGISTRY = {'inline': InlineResolver}


TResolver = typing.Literal['inline']


def resolve(
    playlist_url: str,
    message: str,
    strategy: str = 'inline',
    commit: bool = False,
    *args,
    **kwargs,
) -> typing.List[spotify.Track]:
    """Resolve spotify playlist with the given message

    Args:
        playlist_url (str): the playlist we want to compose the message with.
        message (str): the message we want to hide into the playlist.
        strategy (str, optional): hidden strategy. Defaults to 'inline'.
        commit (bool, optional): whether you want the playlist to be modified
            automatically. Defaults to False.

    Raises:
        ValueError: whether the given strategy does not exists.
        SpotifyConnectionError: whether there's a problem connecting to
            spotify.
        ResolverError: whether there's a problem resolving the message.

    Returns:
        typing.List[spotify.Track]: a list containing spotify tracks in order.
    """

    resolver_klass = __RESOLVERS_REGISTRY.get(strategy)
    if not resolver_klass:
        raise ValueError(f'Error {strategy} not found')
    return resolver_klass(playlist_url, message, *args, **kwargs).resolve(
        commit=commit
    )
