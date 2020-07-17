from pygit2 import Commit
from git_lint_branch.linter_output import *
import git_lint_branch.cfg as cfg

def backwards_merge_linter(commit: Commit):
    result = LinterOutput()
    result.level = LinterLevel.Empty

    if len(commit.parents) < 2:
        return result

    parents_iter = iter(commit.parents)
    next(parents_iter)
    for parent in parents_iter:
        # if the parent is on upstream, its merge-base with upstream
        # will be itself.
        base = cfg.repo.merge_base(cfg.upstream.oid, parent.oid)
        if base != parent.oid:
            continue
        result.level = LinterLevel.Warning
        result.title = 'Backwards Merge'
        result.message = f'''
        This commit is a backwards merge which merges changes from
        upstream into this branch. While this is often done for
        convenience by developers, the final branch history should
        not contain backwards merges.
        '''
        result.help_string = f'''
        Rebasing this branch onto its upstream with e.g. `git rebase [upstream]`
        will remove any merge commits on the branch by default.
        '''
        break
    return result
