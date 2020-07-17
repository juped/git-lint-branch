from pygit2 import Commit
from git_lint_branch.spacy import NLP
from git_lint_branch.linter_output import *


def tense_linter(commit: Commit):
    tab = ' ' * 4
    result = LinterOutput()
    result.title = 'Tense Linter Output'
    past_tenses = []
    doc = NLP(commit.message)
    for sent in doc.sents:
        if sent.root.tag_ in ['VBD', 'VBN']:
            past_tenses.append(sent.root)
    if len(past_tenses) == 0:
        result.level = LinterLevel.Empty
        result.message = (
            f'\n{tab}The commit message is in the present tense.\n'
        )
        result.help_string = '\n{tab}Nothing to do here.\n'
        return result
    result.level = LinterLevel.Warning
    result.message = f'\n{tab}The following words are in past tense:\n'
    for i, token in enumerate(past_tenses):
        result.message += f'{tab * 2}{i + 1}. {token} ====> {token.lemma_}\n'
    result.help_string = (
        f'\n{tab}If this was the most recent commit, you can edit the message\n'
          f'{tab}with `git commit --amend`. Otherwise, use the reword command in\n'
          f'an interactive rebase.'
    )
    return result
