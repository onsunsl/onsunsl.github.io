import enum
from typing import Dict, Any

from dependency_injector import containers, providers

from .a.container_a import CoreContainerA


class PosEnvType(enum.IntEnum):
    """POS环境。"""

    TEST = enum.auto()
    """测试。"""

    UAT = enum.auto()
    """UAT。"""

    PRODUCT = enum.auto()
    """生产。"""


class AiohttpClient:
    pass

class ThemeViewModel:
    pass

class SchedulerBase:
    pass


def _get_pos_env_type(env: str) -> PosEnvType:
    """获取POS环境。"""

    return PosEnvType.TEST if "TEST" in env else PosEnvType.PRODUCT


def _get_online_sale_url(env: str, api: Dict[str, Any]) -> str:
    """获取在线销售URL。"""

    return api[env]["sale"]


class MainContainer(containers.DeclarativeContainer):
    """主容器。"""

    config = providers.Configuration(yaml_files=["config.yaml"])
    """配置。"""

    env_type = providers.Callable(_get_pos_env_type, env=config.client.env)
    """环境。"""

    main_scheduler = providers.Dependency(instance_of=SchedulerBase)
    """主调度器。"""

    theme_view_model = providers.Singleton(
        ThemeViewModel, value=config.yaml.theme
    )
    """主题视图模型。"""

    token = providers.Object("")
    """令牌。"""

    base_offline_url = providers.Object("OFFLINE")
    """基础离线URL。"""

    client = providers.Factory(AiohttpClient)
    """客户端。"""

    core_container = providers.Container(CoreContainerA, env=config.env)
    """核心容器。"""

