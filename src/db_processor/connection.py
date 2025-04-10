from typing import Optional, Any

import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client, Client, ClientOptions

from src.config import SUPABASE_URL, SUPABASE_SECRET_KEY, SUPABASE_PUBLIC_KEY, DB_CONFIG

class DatabaseConnection:
    public: bool = False
    _instance: Optional['DatabaseConnection'] = None
    _supabase: Optional[Client] = None
    _pg_conn = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, public: bool = False) -> None:
        self.public: bool = public
        self._init_supabase()

    def _init_supabase(self) -> None:
        """
        Initialize Supabase client
        """
        key: str = SUPABASE_PUBLIC_KEY if self.public else SUPABASE_SECRET_KEY
        if not self._supabase:
            if not SUPABASE_URL or not key:
                raise ValueError("Supabase URL and Key must be provided in environment variables")
            self._supabase = create_client(supabase_url=SUPABASE_URL, supabase_key=key)

    def _init_pg_conn(self) -> None:
        """
        Initialize PostgreSQL connection
        """
        if not self._pg_conn:
            if not all(DB_CONFIG.values()):
                raise ValueError("Database configuration must be provided in environment variables")
            self._pg_conn: Any = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

    def connect_schema(self, schema: str) -> None:
        """
        Connect to Database schema
        """
        if not self._supabase:
            raise RuntimeError("Supabase client not initialized")
        
        key: str = SUPABASE_PUBLIC_KEY if self.public else SUPABASE_SECRET_KEY
        self._supabase = create_client(
            supabase_url=SUPABASE_URL,
            supabase_key=key,
            options=ClientOptions(schema=schema)
        )

    @property
    def supabase(self) -> Client:
        """
        Get Supabase client instance
        """
        if not self._supabase:
            raise RuntimeError("Supabase client not initialized")
        return self._supabase

    @property
    def pg_conn(self) -> Any:
        """
        Get PostgreSQL connection
        """
        if not self._pg_conn:
            raise RuntimeError("PostgreSQL connection not initialized")
        return self._pg_conn

    def close(self) -> None:
        """
        Close database connections
        """
        if self._pg_conn:
            self._pg_conn.close()
            self._pg_conn = None

    def __del__(self) -> None:
        """
        Cleanup when object is destroyed
        """
        self.close() 