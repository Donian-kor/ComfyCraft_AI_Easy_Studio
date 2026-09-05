"""Connection pooling and session management for HTTP connections."""

from __future__ import annotations

import threading
from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ConnectionPoolManager:
    """Manages HTTP connection pools for different hosts."""
    
    _instance: Optional[ConnectionPoolManager] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> ConnectionPoolManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._sessions: Dict[str, requests.Session] = {}
        self._lock = threading.Lock()
        self._initialized = True
    
    def get_session(self, base_url: str, max_retries: int = 3, pool_connections: int = 10, pool_maxsize: int = 10) -> requests.Session:
        """Get or create a session for the given URL.
        
        Args:
            base_url: The base URL for the session
            max_retries: Maximum number of retries
            pool_connections: Number of connection pools to cache
            pool_maxsize: Maximum number of connections to save in the pool
        
        Returns:
            A requests.Session configured with connection pooling
        """
        with self._lock:
            if base_url not in self._sessions:
                self._sessions[base_url] = self._create_session(
                    max_retries=max_retries,
                    pool_connections=pool_connections,
                    pool_maxsize=pool_maxsize
                )
            return self._sessions[base_url]
    
    @staticmethod
    def _create_session(max_retries: int = 3, pool_connections: int = 10, pool_maxsize: int = 10) -> requests.Session:
        """Create a new session with optimal settings."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,  # 0.5s, 1s, 2s for retries
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "HEAD"]
        )
        
        # Create adapters with connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def clear_session(self, base_url: str) -> None:
        """Clear the session for a specific URL."""
        with self._lock:
            if base_url in self._sessions:
                self._sessions[base_url].close()
                del self._sessions[base_url]
    
    def clear_all(self) -> None:
        """Clear all sessions."""
        with self._lock:
            for session in self._sessions.values():
                session.close()
            self._sessions.clear()


def get_connection_pool_manager() -> ConnectionPoolManager:
    """Get the singleton ConnectionPoolManager instance."""
    return ConnectionPoolManager()
