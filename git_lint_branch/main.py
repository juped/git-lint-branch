import typer
import os
from pygit2 import discover_repository
import collections
from pygit2 import Repository, Commit
from pygit2 import GIT_SORT_TOPOLOGICAL
import git_lint_branch.cfg as cfg
from git_lint_branch.linter_output import *
from git_lint_branch.single import single_linters
from git_lint_branch.multi import multi_linters


app = typer.Typer()

"""
From: https://stackoverflow.com/questions/16108285/correct-way-to-iterate-twice-over-a-list?rq=1
"""


def tosequence(it):
    """Turn iterable into a sequence, avoiding a copy if possible."""
    if not isinstance(it, collections.Sequence):
        it = list(it)
    return it

class Printer:
    def __init__(self, verbose: bool = True):
        # self._single_data = typer.style('+++ ', fg=typer.colors.CYAN)
        # self._single_data += typer.style('Linting your commits:\n', fg=typer.colors.BRIGHT_CYAN, bold=True, underline=True)
        self._verbose = verbose
        
        self._single_data = ''
        self._commit_str = ''

        self._multiple_data = ''

    def add_commit(self, commit: Commit):
        self._commit_str = typer.style(f'\nCOMMIT: {commit.id}\n', fg=typer.colors.BRIGHT_CYAN, bold=True)
        self._commit_str += typer.style(f'TITLE: {commit.message.splitlines()[0]}\n', fg=typer.colors.BRIGHT_CYAN, bold=True)

    def add_single_linter(self, linter: LinterOutput):
        self._single_data += self._commit_str
        self._commit_str = ''

        self._single_data += linter.pretty_str(self._verbose)

    def add_multiple_linter(self, linter: LinterOutput):
        self._multiple_data += linter.pretty_str(self._verbose)
        
    def show(self):
        final_str = ''
        if len(self._single_data) > 0:
            final_str += typer.style('+++ ', fg=typer.colors.GREEN)
            final_str += typer.style('Linting your commits:\n', fg=typer.colors.BRIGHT_GREEN, bold=True, underline=True)

            final_str += self._single_data

        if len(self._multiple_data) > 0:
            final_str += typer.style('\n+++ ', fg=typer.colors.GREEN)
            final_str += typer.style('Linting your commit history:\n', fg=typer.colors.BRIGHT_GREEN, bold=True, underline=True)
            
            final_str += self._multiple_data

        typer.echo(final_str)


@app.command()
def main(upstream: str):
    """
    Lints the commit history reachable from the current HEAD that is not
    on UPSTREAM (i.e., the current branch).
    """
    repo_path = discover_repository(os.getcwd())
    if repo_path is None:
        typer.echo('fatal: not a git repository (or any of the parent directories)', err=True)
        raise typer.Exit(code=1)
    cfg.repo = Repository(repo_path)
    upstream = cfg.repo.revparse_single(upstream)
    walker = cfg.repo.walk(cfg.repo.head.target, GIT_SORT_TOPOLOGICAL)
    walker.hide(upstream.id)
    walker = tosequence(walker)

    printer = Printer()

    for commit in walker:
        printer.add_commit(commit)

        for linter in single_linters:
            lint_result = linter(commit)
            if lint_result.level is not LinterLevel.Empty:
                printer.add_single_linter(lint_result)


    for linter in multi_linters:
        lint_result = linter(walker)
        if lint_result.level is not LinterLevel.Empty:
            printer.add_multiple_linter(lint_result)
    
    printer.show()
