from pygit2 import Commit
from git_lint_branch.linter_output import *
from git_lint_branch.single.linters import *
from git_lint_branch.single.regex_linter import *
from git_lint_branch.single.tense_linter import *

single_linters = [
    example_linter,
    regex_linter,
    tense_linter,
]
