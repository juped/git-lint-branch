from pygit2 import Commit
from git_lint_branch.linter_output import *
from git_lint_branch.single.example_linter import *
from git_lint_branch.single.regex_linter import *
from git_lint_branch.single.diff_size_linter import diff_size_linter
from git_lint_branch.single.tense_linter import *
from git_lint_branch.single.backwards_merge_linter import *

single_linters = [
    regex_linter,
    diff_size_linter,
    tense_linter,
    backwards_merge_linter,
]
