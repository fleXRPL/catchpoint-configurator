"""
Catchpoint Configurator - A framework for deploying Catchpoint monitoring configurations as code.
"""

__version__ = "1.0.0"

from .core import CatchpointConfigurator
from .config import ConfigValidator

__all__ = ["CatchpointConfigurator", "ConfigValidator"]
