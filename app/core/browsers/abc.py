"""ABC Browser"""

from abc import ABC, abstractmethod


class Browser(ABC):
    """Abstract base class for browser implementations."""

    executable = None
    options = None
    instance = None

    def __init__(
        self,
        headless: bool = True,
        multi_instances: bool = False
    ) -> None:
        """
        Initialize browser.

        Args:
            headless: Run browser in headless mode
            multi_instances: Allow multiple browser instances
        """
        self.headless = headless
        self.multi_instances = multi_instances

        self._set_executable()
        self._set_options()

    @abstractmethod
    def _set_executable(self) -> None:
        """Set browser executable path."""
        pass

    @abstractmethod
    def _set_options(self) -> None:
        """Set browser options."""
        pass

    @abstractmethod
    def get_instance(self) -> None:
        """Get browser driver instance."""
        pass
