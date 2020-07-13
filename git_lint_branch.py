import typer
from pygit2 import Repository
from pygit2 import GIT_SORT_TOPOLOGICAL

app = typer.Typer()

@app.command()
def main(upstream: str):
    """
    Lints the commit history reachable from the current HEAD that is not
    on UPSTREAM (i.e., the current branch).
    """
    repo = Repository('.git')
    upstream = repo.revparse_single(upstream)
    walker = repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL)
    walker.hide(upstream.id)
    for commit in walker:
        pass
