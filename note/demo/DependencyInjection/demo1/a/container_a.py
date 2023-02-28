import enum
from typing import Dict, Any

from dependency_injector import containers, providers


class ConfigA:
    pass


class ViewModel:
    pass


class CoreContainerA(containers.DeclarativeContainer):
    """核心容器。"""

    configuration = providers.Singleton(ConfigA)
    """配置。"""

    view_model = providers.Singleton(ViewModel)
    """视图模型。"""

