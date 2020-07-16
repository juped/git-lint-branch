import re

from pygit2 import Commit
from git_lint_branch.linter_output import *
import git_lint_branch.cfg as cfg

def regex_linter(commit: Commit):
    result = LinterOutput()

    regex = cfg.config.get('regex_linter', 'regex', fallback=r".*")
    title_length = int(cfg.config.get('regex_linter', 'title_length', fallback=50))
    body_line_length = int(cfg.config.get('regex_linter', 'body_line_length', fallback=72))

    result.level = LinterLevel.Empty
    result.title = 'Commit message format'
    result.message = '''
    '''
    result.help_string = f'''
    Make sure the commit message title follows this pattern: {regex}
    and is under {title_length} characters.

    Also keep each line of the commit message body under {body_line_length} characters.
    '''

    pattern = re.compile(regex, re.UNICODE)
    commit_title = commit.message.splitlines()[0]
    if pattern.fullmatch(commit_title) is None:
        result.level = LinterLevel.Warning
        result.message += \
        '''Commit title does not match pattern.
    '''

    if len(commit_title) > title_length:
        result.level = max(result.level, LinterLevel.Warning)
        result.message += \
        '''Commit title too long.
    '''

    for line in commit.message.splitlines()[1:]:
        if len(line) > body_line_length:
            result.level = max(result.level, LinterLevel.Notice)
            result.message += \
            '''Commit body lines too long.
    '''
            break

    return result
