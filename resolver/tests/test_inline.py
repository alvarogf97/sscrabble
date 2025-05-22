import pytest
from resolver.inline import InlineResolver
from resolver.errors import NotEnoughLettersError
from connections.spotify import Track


@pytest.fixture
def playlist_url():
    return "https://open.spotify.com/playlist/FAKE_ID"


@pytest.fixture
def message():
    return "abc"


@pytest.fixture
def tracks():
    return [
        Track(id="1", name="A Song", artist="Artist 1"),
        Track(id="2", name="A Track", artist="Artist 2"),
        Track(id="3", name="B Track", artist="Artist 3"),
        Track(id="4", name="C Track", artist="Artist 4"),
        Track(id="5", name="Z Track", artist="Artist 5"),
    ]


def test_check_passes_when_letters_are_available(monkeypatch, playlist_url, message, tracks):
    monkeypatch.setattr(
        "resolver.inline.spotify.get_playlist_tracks", lambda _: tracks
    )
    resolver = InlineResolver(playlist_url, message)
    resolver.check()


def test_check_raises_when_letters_are_missing(monkeypatch, playlist_url):
    partial_tracks = [
        Track(id="1", name="A Song", artist="Artist 1"),
        Track(id="2", name="Another", artist="Artist 2"),
    ]
    monkeypatch.setattr(
        "resolver.inline.spotify.get_playlist_tracks", lambda _: partial_tracks
    )
    resolver = InlineResolver(playlist_url, "abc")
    with pytest.raises(NotEnoughLettersError) as exc:
        resolver.check()
    assert 'Missing letters' in str(exc.value)
    assert isinstance(exc.value.missings, dict)
    assert 'b' in exc.value.missings
    assert 'c' in exc.value.missings


def test_resolve_returns_tracks_in_correct_order(monkeypatch, playlist_url, message, tracks):
    monkeypatch.setattr(
        "resolver.inline.spotify.get_playlist_tracks", lambda _: tracks
    )
    resolver = InlineResolver(playlist_url, message)
    result = resolver._resolve()

    expected_order = ['a', 'b', 'c']
    used_track_letters = [t.name[0].lower() for t in result[:3]]
    assert used_track_letters == expected_order

    assert all(track not in result[:3] for track in result[3:])