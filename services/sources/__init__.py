"""
National Career Opportunity & Examination Sources Registry & Ingestion Engine.
Covers Tier 1 Statutory Authorities, Tier 2 Government Directories, and Verified Boards across India.
"""
from .source_registry import STATUTORY_SOURCES_REGISTRY
from .statutory_ingest import StatutoryOpportunityIngestor

__all__ = ["STATUTORY_SOURCES_REGISTRY", "StatutoryOpportunityIngestor"]
