from git_lint_branch.colors import colorize
from enum import Enum

linterlevel2color = dict(
    Empty='white',
    Notice='blue',
    Caution='cyan',
    Warning='yellow',
    Failure='red',
)

class LinterLevel(Enum):
    """
    Linter output severity levels. Rough definitions:
    Notice: Likely not a problem, but worth noting.
    Caution: May be a problem.
    Warning: Likely a problem.
    Failure: Should be considered a test failure.
             (For repository maintainer use only.)
    """
    Empty   = 0
    Notice  = 1
    Caution = 2
    Warning = 3
    Failure = 4

class LinterOutput():
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: LinterLevel):
        if not isinstance(value, LinterLevel):
            raise TypeError('Severity level must be a valid LinterLevel')
        self._level = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    # TODO: message and help_string get their indentation from the
    # indentation of the linter itself. It should be made uniform in
    # the setters.
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def help_string(self):
        return self._help_string

    @help_string.setter
    def help_string(self, value: str):
        self._help_string = value

    def pretty_print(self):
        if self._level is LinterLevel.Empty:
            raise ValueError('Cannot pretty print an empty LinterOutput')
        print(
            colorize(
                'Severity: {level}'.format(level=self.level.name),
                color=linterlevel2color[self.level.name],
                bold=True
            )
        )
        print(self.title)
        print('Details:\n{message}'.format(message=self.message))
        print('Suggestions:\n{help_string}'.format(help_string=self.help_string))
