"""
Database Connection Module
Handles PostgreSQL connection, session management, and database initialization.
"""

import os
from typing import Optional
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool
from pathlib import Path
import json

from .db_models import Base


class Database:
    """
    Database connection manager for PostgreSQL.
    Handles connection pooling, session management, and initialization.
    """
    
    _engine = None
    _session_factory = None
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Get database URL from environment variables or config file.
        Priority: Environment variables > config file > default
        
        Returns:
            Database connection URL
        """
        # Try environment variable first
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            return db_url
        
        # Try config file
        config_path = Path('data') / 'db_config.json'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('database_url')
            except Exception:
                pass
        
        # Default PostgreSQL connection
        return os.getenv(
            'DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/citizen_feedback'
        )
    
    @classmethod
    def initialize(cls, database_url: Optional[str] = None, echo: bool = False):
        """
        Initialize database connection and create tables.
        
        Args:
            database_url: Optional database URL (if not provided, uses get_database_url)
            echo: Whether to echo SQL statements (for debugging)
        """
        if cls._engine is None:
            url = database_url or cls.get_database_url()
            
            # Create engine with connection pooling
            cls._engine = create_engine(
                url,
                echo=echo,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,  # Verify connections before using
                pool_recycle=3600,  # Recycle connections after 1 hour
            )
            
            # Create session factory
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                autocommit=False,
                autoflush=False
            )
            
            # Create all tables
            Base.metadata.create_all(cls._engine)
    
    @classmethod
    def get_engine(cls):
        """Get the database engine."""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
    
    @classmethod
    def get_session(cls) -> Session:
        """
        Get a new database session.
        
        Returns:
            SQLAlchemy Session object
        """
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory()
    
    @classmethod
    @contextmanager
    def session_scope(cls):
        """
        Provide a transactional scope for database operations.
        Automatically commits on success and rolls back on error.
        
        Usage:
            with Database.session_scope() as session:
                session.add(feedback)
        """
        session = cls.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    @classmethod
    def create_tables(cls):
        """Create all database tables if they don't exist."""
        if cls._engine is None:
            cls.initialize()
        Base.metadata.create_all(cls._engine)
    
    @classmethod
    def drop_tables(cls):
        """Drop all database tables. Use with caution!"""
        if cls._engine is None:
            cls.initialize()
        Base.metadata.drop_all(cls._engine)
    
    @classmethod
    def close(cls):
        """Close database connections and cleanup."""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
    
    @classmethod
    def test_connection(cls) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            from sqlalchemy import text
            with cls.session_scope() as session:
                session.execute(text('SELECT 1'))
            return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
    
    @classmethod
    def get_connection_info(cls) -> dict:
        """
        Get information about the database connection.
        
        Returns:
            Dictionary with connection information
        """
        if cls._engine is None:
            cls.initialize()
        
        return {
            'url': str(cls._engine.url).replace(cls._engine.url.password or '', '***'),
            'pool_size': cls._engine.pool.size() if hasattr(cls._engine.pool, 'size') else 'N/A',
            'checked_in': cls._engine.pool.checkedin() if hasattr(cls._engine.pool, 'checkedin') else 'N/A',
            'checked_out': cls._engine.pool.checkedout() if hasattr(cls._engine.pool, 'checkedout') else 'N/A',
            'overflow': cls._engine.pool.overflow() if hasattr(cls._engine.pool, 'overflow') else 'N/A',
            'dialect': cls._engine.dialect.name,
            'driver': cls._engine.dialect.driver
        }
