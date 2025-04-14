"""
Catchpoint Configurator - A framework for deploying Catchpoint monitoring configurations as code.
"""

__version__ = "1.0.0"

from .config import ConfigValidator
from .core import CatchpointConfigurator

__all__ = ["CatchpointConfigurator", "ConfigValidator"]
