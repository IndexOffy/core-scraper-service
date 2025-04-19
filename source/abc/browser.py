"ABC Brownser"

from abc import ABC, abstractmethod


class Browser(ABC):

    executable = None
    options = None
    instance = None

    def __init__(
        self,
        headless: bool = True,
        multi_instances: bool = False
    ) -> None:
        self.headless = headless
        self.multi_instances = multi_instances

        self._set_executable()
        self._set_options()

    @abstractmethod
    def _set_executable(self) -> None:
        pass

    @abstractmethod
    def _set_options(self) -> None:
        pass

    @abstractmethod
    def get_instance(self) -> None:
        pass
