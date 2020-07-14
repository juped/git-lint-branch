from pygit2 import Commit
from git_lint_branch.spacy import NLP
from git_lint_branch.linter_output import *


def example_linter(commit: Commit):
    result = LinterOutput()
    result.level = LinterLevel.Notice
    result.title = "Example linter output"
    result.message = """
    This is an example of linter output.

    The first line of the commit message is:
    {message}
    """.format(
        message=commit.message.splitlines()[0]
    )
    result.help_string = """
    There is nothing to do, because this is just an example.
    """
    return result


def tense_linter(commit: Commit):
    tab = "    "
    result = LinterOutput()
    result.title = "Tense Linter Output"
    past_tenses = []
    for line in commit.message.splitlines():
        doc = NLP(line)
        for token in doc:
            if token.tag_ in ["VBD", "VBN"]:
                past_tenses.append(token)
    if len(past_tenses) == 0:
        result.level = LinterLevel.Empty
        result.message = (
            f"\n{tab}The commit message is in the present tense.\n"
        )
        result.help_string = "\n{tab}Nothing to do here.\n"
        return result
    result.level = LinterLevel.Warning
    result.message = f"\n{tab}The following words are in past tense:\n"
    for i, token in enumerate(past_tenses):
        result.message += f"{tab * 2}{i + 1}. {token} ====> {token.lemma_}\n"
    result.help_string = (
        f"\n{tab}Try using the suggested words to" f" fix the commit message\n"
    )
    return result
