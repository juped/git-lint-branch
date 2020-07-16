![git-lint-branch](https://user-images.githubusercontent.com/43912285/87730869-9f76f400-c7e6-11ea-90e3-99ee01911f36.png)

*As contributors*, use this tool to check your branch history against common mistakes that annoy maintainers - and make that perfect pull request.

*As maintainers*, expect quality pull requests that satisfy rules you set, decreasing the time it takes to merge in those changes and release that new feature. Setup your CI to fail in case something's seriously wrong with a branch's history.

![diff-size-linter](https://user-images.githubusercontent.com/43912285/87727113-fcba7780-c7dd-11ea-9ff2-ce8dee6a955f.png)

# Features
We provide *two* kinds of linters:
- Single-Commit Linters
- Multi-Commmit Linters

Yep, that's correct, those of the first kind only analyse one commit from the history at a time, while those of the second look at multiple commits at once. 

This provides flexibility in terms of what a linter can detect, while maintaining a uniform and streamlined way or reporting those findings to the user.

Currently included are the following linters:

## Single-Commit Linters

- **Commit Message Pattern:** Ensures that the commit message's title follows a maintainer-specified regular expresssion, and is under a certain character limit. Also enforces a character limit on each subsequent line of the commit message.
- **Imperative Form:** Ensures that the commit message uses the imperative form, which is considered good practice.

![imperative-form-linter](https://user-images.githubusercontent.com/43912285/87729070-1cec3580-c7e2-11ea-90b6-bf24d2d20b31.png)

- **Diff Size:** Warns if a commit has a diff that is too large, which may be indicative of several logically unrelated changes being squashed into a single commit

## Multi-Commit Linters

- **Merge Commits:** Warns if merge-commits exist in topic-branches. Usually such commits appear only in upstream *integration* branches, and thus may indicate a fishy history.

![merge-commit-linter](https://user-images.githubusercontent.com/43912285/87729822-db5c8a00-c7e3-11ea-8895-4599cabf4bc0.png)

## In The Works

We have several more linters in the oven, including ones that **detect backward merges**, **complain if source code is edited without the tests being accordingly modified** and **detect commits that should perhaps be squashed but aren't**.

## Your Project, To Your Liking

Many of these linters are configurable, such as the regular expression used by the Commit Message Pattern linter. These options are meant to be decided by the project maintainers using a simple configuration file.

![.git-lint-branch](https://user-images.githubusercontent.com/43912285/87730515-9e919280-c7e5-11ea-8f57-803b40156683.png)

We also plan to make the *set of linters that are run*, as well as the *severity of them failing* as configurable options.

## Lint Your Way

Our linters do not suit your needs? The modular structure of `git-lint-branch` makes it really easy to add your own linters. Think it'll help others as well? We'll be happy to see a pull-request. See development and contributing guidelines below.

# Usage

# Development and Contributing

Dependencies:
- Typer
- PyGit2
- Spacy
- Colorama

To install for development
```shell
[enter virtual environment]
% pip install -e .
```
