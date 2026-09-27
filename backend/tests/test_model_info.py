"""Tests for BOVIMED YOLO11n model transparency."""

import os
from pathlib import Path

import pytest

from app.config import get_settings
from app.services.model_info import (
    BOVIMED_CLASS_SET,
    BOVIMED_CLASSES_DISPLAY,
    BOVIMED_MODEL_FILE,
    BOVIMED_MODEL_NAME,
    VALIDATION_METRICS,
    get_model_info,
    get_model_metadata,
    is_valid_bovimed_class,
)
from app.services.yolo_service import get_yolo_service, reset_yolo_service


BACKEND_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = BACKEND_ROOT / "models" / "best.pt"


def test_model_info_payload_structure():
    info = get_model_info()
    assert info["model_name"] == "BOVIMED YOLO11n"
    assert info["model_type"] == "Custom Object Detection"
    assert info["model_file"] == "best.pt"
    assert info["class_count"] == 7
    assert info["classes"] == BOVIMED_CLASSES_DISPLAY
    assert info["validation_metrics"] == VALIDATION_METRICS
    assert set(info["classes"]) == BOVIMED_CLASS_SET


def test_validation_metrics_are_fixed():
    assert VALIDATION_METRICS["mAP50"] == pytest.approx(0.8454)
    assert VALIDATION_METRICS["mAP50_95"] == pytest.approx(0.6019)
    assert VALIDATION_METRICS["precision"] == pytest.approx(0.8146)
    assert VALIDATION_METRICS["recall"] == pytest.approx(0.7695)


def test_all_display_classes_are_valid():
    for name in BOVIMED_CLASSES_DISPLAY:
        assert is_valid_bovimed_class(name)


def test_invalid_detection_class_rejected():
    assert not is_valid_bovimed_class("person")
    assert not is_valid_bovimed_class("car")
    assert not is_valid_bovimed_class("dog")


def test_model_metadata_for_live_mode():
    meta = get_model_metadata(model_loaded=True, demo_mode=False)
    assert meta["model_name"] == BOVIMED_MODEL_NAME
    assert meta["model_loaded"] is True
    assert meta["demo_mode"] is False


def test_model_metadata_for_demo_mode():
    meta = get_model_metadata(model_loaded=True, demo_mode=True)
    assert meta["model_loaded"] is False
    assert meta["demo_mode"] is True


@pytest.mark.skipif(not MODEL_PATH.is_file(), reason="best.pt not present in test environment")
def test_best_pt_exists_and_loads_in_production_mode(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "false")
    get_settings.cache_clear()
    reset_yolo_service()
    settings = get_settings()
    assert settings.resolved_model_path.name == BOVIMED_MODEL_FILE
    yolo = get_yolo_service()
    yolo.ensure_model_loaded()
    assert yolo.model_loaded is True
    info = get_model_info()
    assert info["demo_mode"] is False
    assert info["model_loaded"] is True
    assert info["model_name"] == "BOVIMED YOLO11n"
    names = yolo.status()["class_names"]
    for class_name in names.values():
        assert is_valid_bovimed_class(class_name)


def test_production_mode_must_not_be_demo_when_best_pt_present(monkeypatch):
    if not MODEL_PATH.is_file():
        pytest.skip("best.pt not present")
    monkeypatch.setenv("DEMO_MODE", "false")
    get_settings.cache_clear()
    reset_yolo_service()
    info = get_model_info()
    assert info["demo_mode"] is False, "demo_mode unexpectedly true while best.pt is available"


def test_missing_best_pt_fails_to_load(monkeypatch, tmp_path):
    missing = tmp_path / "missing.pt"
    monkeypatch.setenv("DEMO_MODE", "false")
    monkeypatch.setenv("MODEL_PATH", str(missing))
    get_settings.cache_clear()
    reset_yolo_service()
    yolo = get_yolo_service()
    yolo.ensure_model_loaded()
    assert yolo.model_loaded is False
    info = get_model_info()
    assert info["model_loaded"] is False


def test_model_info_matches_api_contract():
    """Service payload must match GET /api/model-info contract."""
    info = get_model_info()
    required = {
        "model_name",
        "model_type",
        "model_file",
        "model_loaded",
        "demo_mode",
        "class_count",
        "classes",
        "validation_metrics",
    }
    assert required.issubset(info.keys())
    assert info["model_name"] == "BOVIMED YOLO11n"
    assert info["model_file"] == "best.pt"
    assert info["class_count"] == 7
