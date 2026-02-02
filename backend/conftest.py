import sys
from pathlib import Path

# Add backend/ to PYTHONPATH so "app" can be imported
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
