from pygit2 import Walker
from git_lint_branch.linter_output import *


def repeat_linter(walker: Walker):
    result = LinterOutput()
    result.level = LinterLevel.Empty
    result.title = 'Repeating Commit Messages'
    result.message = ''''''
    result.help_string = '''
    \tTry renaming the repeated commit messages in a more meaningful manner
    '''

    repeat_dict = {}

    for commit in walker:
        commit_msg_clean = commit.message.strip("\n")
        if commit_msg_clean not in repeat_dict:
            repeat_dict[commit_msg_clean] = 1
        else:
            repeat_dict[commit_msg_clean] += 1

    for commit, commit_number in repeat_dict.items():
        if commit_number > 1:
            result.level = LinterLevel.Warning
            result.message += f'\n\tThe commit message: "{commit}" has been repeated {str(commit_number)} times'

    result.message += '\n'
    return result

def any_merges(walker: Walker):
    result = LinterOutput()
    result.level = LinterLevel.Empty

    merge_list = []

    for commit in walker:
        if len(commit.parents) > 1:
            merge_list.append(commit)

    if len(merge_list) > 0:
        result.level = LinterLevel.Caution
        result.message = '''
        This branch contains merge commits (commits with two or more parents).
        Ordinarily, merge commits should only appear in upstream 'integration'
        branches, not in topic branches. However, merge commits could be correct
        if the topic was split into multiple 'subtopics' which were then merged
        into the general topic.
        '''
        result.help_string = '''
        Any `git rebase` operation, such as `git rebase master`, removes merges
        from the commit history by default.
        '''

    return result
