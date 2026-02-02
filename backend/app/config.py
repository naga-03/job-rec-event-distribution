import os

# -------------------------
# Base paths
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
AUTH_USERS_FILE = os.path.join(DATA_DIR, "auth_users.json")
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.json")

# -------------------------
# JWT / Auth configuration
# -------------------------

JWT_SECRET = "super-secret-key"  # for demo; use env var in prod
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
