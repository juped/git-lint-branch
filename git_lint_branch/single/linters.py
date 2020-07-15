from pygit2 import Commit
from git_lint_branch.linter_output import *


def example_linter(commit: Commit):
    result = LinterOutput()
    result.level = LinterLevel.Notice
    result.title = 'Example linter output'
    result.message = '''
    This is an example of linter output.

    The first line of the commit message is:
    {message}
    '''.format(
        message=commit.message.splitlines()[0]
    )
    result.help_string = '''
    There is nothing to do, because this is just an example.
    '''
    return result
