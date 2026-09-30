"""Exception hierarchy of the project."""


class InputFileError(Exception):
    """An input file is missing, unreadable or not valid JSON."""


class SchemaError(Exception):
    """A definition or result object does not match its schema."""


class GenerationError(Exception):
    """The decoder reached a dead end or exceeded its step cap."""


class PromptProcessingError(Exception):
    """Processing of a single prompt failed.

    Attributes:
        prompt: The prompt text that could not be processed.
    """

    def __init__(self, prompt: str, message: str) -> None:
        """Store the offending prompt alongside the message.

        Args:
            prompt: The prompt text that could not be processed.
            message: Human-readable description of the failure.
        """
        super().__init__(message)
        self.prompt = prompt
