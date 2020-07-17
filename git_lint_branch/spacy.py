import spacy
import typer
from spacy.cli import download


# NOTE: Preload the Spacy English File as it is used across
#       several linters
try:
    NLP = spacy.load('en_core_web_sm')
except OSError:
    typer.echo(
        f'"en_core_web_sm" not found!! Spacy will try to automatically\n'
        f' download it. If it fails please download it manually using the\n'
        f' command `python -m spacy download en_core_web_sm`\n',
    err=True)
    download('en_core_web_sm')
    NLP = spacy.load('en_core_web_sm')
    typer.echo('"en_core_web_sm" model installed.', err=True)
