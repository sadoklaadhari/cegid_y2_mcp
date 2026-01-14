#!/usr/bin/env python3
"""
Authentication Manager - Handles OAuth2, API Keys, JWT
"""

import logging
import jwt
import json
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)


class AuthManager:
    """Manage authentication and authorization"""
    
    def __init__(self, config: Dict):
        """Initialize auth manager"""
        self.config = config
        self.auth_config = config.get("auth", {})
        self.secret_key = self.auth_config.get("secret_key", "change-me-in-production")
        self.algorithm = self.auth_config.get("algorithm", "HS256")
        self.token_expiry = self.auth_config.get("token_expiry", 3600)  # 1 hour
        
        logger.info("Auth manager initialized")
    
    def generate_token(self, user_id: str, permissions: list = None) -> str:
        """Generate JWT token"""
        try:
            payload = {
                "user_id": user_id,
                "permissions": permissions or [],
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(seconds=self.token_expiry)
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Token generated for user: {user_id}")
            return token
        
        except Exception as e:
            logger.error(f"Error generating token: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key"""
        valid_keys = self.auth_config.get("api_keys", [])
        return api_key in valid_keys
    
    def validate_oauth(self, oauth_token: str) -> Optional[Dict]:
        """Validate OAuth2 token with provider"""
        try:
            oauth_config = self.auth_config.get("oauth", {})
            provider = oauth_config.get("provider", "cegid")
            
            # In production, verify with OAuth provider
            # This is a placeholder
            if oauth_token:
                return {
                    "user_id": "oauth_user",
                    "provider": provider,
                    "valid": True
                }
            
            return None
        except Exception as e:
            logger.error(f"OAuth validation error: {e}")
            return None
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission"""
        # Implementation depends on your permission model
        logger.debug(f"Checking permission {permission} for user {user_id}")
        return True  # Placeholder
    
    def get_credentials_from_config(self) -> Tuple[Optional[str], Optional[str]]:
        """Get credentials from config file"""
        cegid_config = self.config.get("cegid", {})
        api_key = cegid_config.get("api_key")
        client_id = cegid_config.get("client_id")
        return client_id, api_key
