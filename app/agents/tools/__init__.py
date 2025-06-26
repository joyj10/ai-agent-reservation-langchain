import os
import importlib
import pkgutil
from langchain.tools import BaseTool

__all__ = []

TOOL_REGISTRY = []

package_dir = os.path.dirname(__file__)

for _, module_name, _ in pkgutil.iter_modules([package_dir]):
    module = importlib.import_module(f"{__name__}.{module_name}")
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, BaseTool):
            TOOL_REGISTRY.append(attr)
            __all__.append(attr_name)
