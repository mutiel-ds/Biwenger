from typing import Dict, Any

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

# Database connection settings
DB_CONFIG: Dict[str, Any] = {
    "host": os.environ["DB_HOST"],
    "port": os.environ.get("DB_PORT", default="5432"),
    "database": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"]
} 