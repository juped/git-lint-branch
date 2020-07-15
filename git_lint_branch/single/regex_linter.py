import re

from pygit2 import Commit
from git_lint_branch.linter_output import *

# TODO: Load from config
REGEX = r'^(.+:\ )?[A-Z].+\.$'
TITLE_LENGTH = 76
BODY_LINE_LENGTH = 76

def regex_linter(commit: Commit):
    result = LinterOutput()

    result.level = LinterLevel.Empty
    result.title = 'Commit message format'
    result.message = '''
    '''
    result.help_string = f'''
    Make sure the commit message title follows this pattern: {REGEX}
    and is under {TITLE_LENGTH} characters.

    Also keep each line of the commit message body under {BODY_LINE_LENGTH} characters.
    '''

    pattern = re.compile(REGEX, re.UNICODE)
    commit_title = commit.message.splitlines()[0]
    if pattern.fullmatch(commit_title) is None:
        result.level = LinterLevel.Warning
        result.message += \
        '''Commit title does not match pattern.
    '''

    if len(commit_title) > TITLE_LENGTH:
        result.level = max(result.level, LinterLevel.Warning)
        result.message += \
        '''Commit title too long.
    '''

    for line in commit.message.splitlines()[1:]:
        if len(line) > BODY_LINE_LENGTH:
            result.level = max(result.level, LinterLevel.Notice)
            result.message += \
            '''Commit body lines too long.
    '''
            break

    return result
