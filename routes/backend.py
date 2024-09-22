import logging
from typing import Dict, Any
from flask import Blueprint, jsonify, request
import sys
import os
from pathlib import Path


# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

be = Blueprint("backend", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Setze die Log-Ebene auf DEBUG
