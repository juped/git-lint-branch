import configparser
import typer
import os
from pygit2 import discover_repository
import collections
from pygit2 import Repository
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
    config_file_path = os.path.join(repo_path, "..", ".git-lint-branch")
    if os.path.isfile(config_file_path):
        cfg.config = configparser.ConfigParser()
        cfg.config.read(config_file_path, encoding="utf-8")
    else:
        cfg.config = None
    upstream = cfg.repo.revparse_single(upstream)
    walker = cfg.repo.walk(cfg.repo.head.target, GIT_SORT_TOPOLOGICAL)
    walker.hide(upstream.id)
    walker = tosequence(walker)

    for commit in walker:
        for linter in single_linters:
            lint_result = linter(commit)
            if lint_result.level is not LinterLevel.Empty:
                print('Commit: {id}'.format(id=commit.id))
                lint_result.pretty_print()

    for linter in multi_linters:
        lint_result = linter(walker)
        if lint_result.level is not LinterLevel.Empty:
            lint_result.pretty_print()
