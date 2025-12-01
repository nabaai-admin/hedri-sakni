import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class UiPathClient:
    """Client for interacting with UiPath API"""
    
    def __init__(self, api_url: str, api_key: str, client_id: str, client_secret: str):
        self.api_url = api_url
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
    
    def _authenticate(self) -> bool:
        """Authenticate with UiPath API and get access token"""
        try:
            # This is a placeholder - adjust based on actual UiPath authentication
            auth_url = f"{self.api_url}/oauth/token"
            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(auth_url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get('access_token')
            self.token_expires_at = datetime.utcnow().timestamp() + data.get('expires_in', 3600)
            
            logger.info("Successfully authenticated with UiPath API")
            return True
            
        except Exception as e:
            logger.error(f"Failed to authenticate with UiPath API: {str(e)}")
            return False
    
    def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token"""
        if not self.access_token or (self.token_expires_at and datetime.utcnow().timestamp() >= self.token_expires_at):
            return self._authenticate()
        return True
    
    def send_reservation_request(
        self, 
        national_id: str, 
        phone_number: str, 
        area: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send reservation request to UiPath API
        
        Args:
            national_id: Customer's national ID
            phone_number: Customer's phone number
            area: Selected area name
            additional_data: Any additional data to include
            
        Returns:
            Dictionary with response data including success status and message
        """
        try:
            if not self._ensure_authenticated():
                return {
                    'success': False,
                    'status_code': 401,
                    'message': 'Failed to authenticate with UiPath API'
                }
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-API-Key': self.api_key
            }
            
            payload = {
                'national_id': national_id,
                'phone_number': phone_number,
                'area': area,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            if additional_data:
                payload.update(additional_data)
            
            logger.info(f"Sending reservation request for national_id: {national_id}, area: {area}")
            
            # Send request to UiPath
            response = requests.post(
                f"{self.api_url}/reservations",
                json=payload,
                headers=headers,
                timeout=60
            )
            
            response_data = response.json() if response.content else {}
            
            result = {
                'success': response.status_code in [200, 201],
                'status_code': response.status_code,
                'message': response_data.get('message', 'Request sent successfully'),
                'data': response_data
            }
            
            logger.info(f"UiPath API response: {result}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error("UiPath API request timed out")
            return {
                'success': False,
                'status_code': 408,
                'message': 'Request timed out'
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"UiPath API request failed: {str(e)}")
            return {
                'success': False,
                'status_code': 500,
                'message': f'Request failed: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error in UiPath client: {str(e)}")
            return {
                'success': False,
                'status_code': 500,
                'message': f'Unexpected error: {str(e)}'
            }
