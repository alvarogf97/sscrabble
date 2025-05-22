from resolver import resolve, errors
import typer
from connections import spotify
from rich.table import Table
from rich.console import Console

app = typer.Typer()


@app.command()
def process(
    playlist_url: str,
    message: str,
    strategy: str = 'inline',
    commit: bool = False,
):
    """
    Try to compose the given message with the tracks on the playlist
    """
    console = Console()
    try:
        resolution = resolve(playlist_url, message, strategy, commit)
        table = Table(title='✅ Resolution', title_justify='left')
        table.add_column('Position', style='cyan', no_wrap=True)
        table.add_column('Track name', style='magenta')
        table.add_column('Track artist', style='green')
        for i, track in enumerate(resolution):
            table.add_row(str(i), track.name, track.artist)
        console.print(table)
        if commit:
            typer.echo('Commited successfully!')
    except spotify.SpotifyConnectionError as e:
        typer.echo(f'❌ {str(e)}')
    except errors.NotEnoughLettersError as e:
        table = Table(title='❌ Missing letters', title_justify='left')
        table.add_column('Letter', style='cyan', no_wrap=True)
        table.add_column('Missings', style='magenta')
        table.add_column('Positions', style='green')

        for letter, (missings, positions) in sorted(e.missings.items()):
            pos_str = ', '.join(map(str, positions))
            table.add_row(letter, str(missings), pos_str)
        console.print(table)

    except errors.ResolverError as e:
        typer.echo(f'❌ {str(e)}')
