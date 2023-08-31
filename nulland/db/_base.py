"""Load all models to make them available for migration tool.

This file must never be imported in model modules to avoid circular imports.
Import base_class.Base instead.
"""

# flake8: noqa F401

from .base_class import Base

import nulland.models.notes
