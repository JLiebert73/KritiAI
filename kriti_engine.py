"""
KritiAI Backend Core Engine (`kriti_engine.py`)
Stripped of legacy PMFBY document upload, OCR, Aadhaar/PII masking, and LLM directive generators.
Strictly exports the database-driven KISAN-Audit verification pipeline and PM-KISAN registry connectors.
"""

import logging
from pm_kisan_registry import (
    init_and_seed_registry,
    get_all_farms,
    get_farm_by_id,
    update_farm_status
)
from kisan_audit_engine import (
    fetch_cadastral_boundary,
    fetch_planetary_pixels,
    compute_fractional_rasterization,
    generate_prithvi_eo2_embedding,
    validate_cultivability,
    upsample_to_submeter,
    execute_kisan_audit_pipeline
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = [
    "init_and_seed_registry",
    "get_all_farms",
    "get_farm_by_id",
    "update_farm_status",
    "fetch_cadastral_boundary",
    "fetch_planetary_pixels",
    "compute_fractional_rasterization",
    "generate_prithvi_eo2_embedding",
    "validate_cultivability",
    "upsample_to_submeter",
    "execute_kisan_audit_pipeline"
]
