from setuptools import setup

setup(
    name='git-lint-branch',
    version='0.0',
    py_modules=['git_lint_branch'],
    install_requires=[
        'typer',
        'pygit2',
        'spacy',
    ],
    entry_points='''
        [console_scripts]
        git-lint-branch=git_lint_branch.main:app
    ''',
)
