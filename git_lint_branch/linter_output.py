from enum import IntEnum
import typer

class LinterLevel(IntEnum):
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

color_map = {
    LinterLevel.Empty: typer.colors.WHITE,
    LinterLevel.Notice: typer.colors.BLUE,
    LinterLevel.Caution: typer.colors.GREEN,
    LinterLevel.Warning: typer.colors.YELLOW,
    LinterLevel.Failure: typer.colors.RED,
}

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

    def pretty_str(self, verbose: bool = True):
        if self.level is LinterLevel.Empty:
            raise ValueError('Cannot pretty print an empty LinterOutput')

        out = typer.style('\n+ ', fg=typer.colors.MAGENTA)
        out += typer.style('FAULT: ', fg=typer.colors.BRIGHT_MAGENTA)
        out += typer.style(self.title, fg=typer.colors.BRIGHT_MAGENTA, bold=True)

        out += typer.style('\n  SEVERITY: ', fg=typer.colors.BRIGHT_MAGENTA)
        out += typer.style(self.level.name, fg=color_map[self.level], bold=True)

        out += typer.style('\n  DETAILS:\n', fg=typer.colors.BRIGHT_MAGENTA)
        out += typer.style(self.message, fg=typer.colors.WHITE)

        if verbose:

            out += typer.style('\n  SUGGESTIONS:\n', fg=typer.colors.BRIGHT_MAGENTA)
            out += typer.style(self.help_string, fg=typer.colors.WHITE)

        return out
