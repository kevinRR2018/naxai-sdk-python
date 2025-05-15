"""
Email suppression lists resources package for the Naxai SDK.

This package provides resource classes for managing email suppression lists,
including bounces and unsubscribes to maintain email deliverability.
"""

from .bounces import BouncesResource
from .unsubscribes import UnsubscribesResource

__all__ = ["BouncesResource", "UnsubscribesResource"]
