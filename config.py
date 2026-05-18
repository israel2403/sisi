"""
Application configuration file.

This module centralizes constants used across the SISI project.
Later, repository.py will use DATA_FILE to save/load data with pickle.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "pacientes.pkl"

APP_NAME = "SISI - Sistema Infantil  de Seguimiento Integral"
APP_VERSION = "1.0.0"
