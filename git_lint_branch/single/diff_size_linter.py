from pygit2 import Commit, Diff

from git_lint_branch.linter_output import *
import git_lint_branch.cfg as cfg

LARGE_DIFF_THRESHOLD = 50

def guess_diff_size(diff: Diff):
    '''
    Uses max(insertions, deletions) per patch, summed over all patches
    to determine the size of a diff. Based on the guess that unrelated
    insertions and deletions may not commonly appear together. This prevents
    modifications from being counted twice.
    '''
    diff_size = 0
    for patch in diff:
        diff_size += max(patch.line_stats[1], patch.line_stats[2])
    return diff_size


def diff_size_linter(commit: Commit):

    result = LinterOutput()
    result.title = 'Commit diff size'
    result.level = LinterLevel.Empty
    result.help_string = '''
    A commit with a very large diff might contain unrelated changes.
    Consider splitting these changes into multiple commits if they are
    unrelated.
    '''

    if len(commit.parents) != 1:
        return result
        # reached a merge commit or the initial commit, don't check it

    diff = cfg.repo.diff(commit, commit.parents[0])
    diff_size = guess_diff_size(diff)

    if diff_size > LARGE_DIFF_THRESHOLD:
        result.level = LinterLevel.Caution
        result.message = f'''
    This commit has a large diff (~{diff_size} modifications).
    '''

    return result
