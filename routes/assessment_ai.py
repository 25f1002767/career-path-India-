"""
routes/assessment_ai.py
==============================================================================
Alias/delegation module pointing to routes.assessment to maintain backward
compatibility with any legacy imports.
==============================================================================
"""

from routes.assessment import assessment

__all__ = ["assessment"]
