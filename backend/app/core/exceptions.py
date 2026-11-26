class ConfigError(Exception):
    """Raised when the files in /config are missing or invalid."""
class LLMResponseError(Exception):
    """Raised when the LLM returns no usable structured output."""