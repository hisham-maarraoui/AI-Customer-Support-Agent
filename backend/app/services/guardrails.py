import re
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class GuardrailsService:
    def __init__(self):
        # Personal data patterns
        self.personal_data_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'address': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
            'apple_id': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'device_id': r'\b[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}\b'
        }
        
        # Legal/financial advice keywords
        self.legal_financial_keywords = [
            'legal', 'lawyer', 'attorney', 'sue', 'lawsuit', 'court', 'judge',
            'financial', 'investment', 'stock', 'money', 'bank', 'account',
            'tax', 'irs', 'insurance', 'claim', 'compensation', 'damages',
            'contract', 'agreement', 'terms', 'liability', 'warranty'
        ]
        
        # Toxicity keywords
        self.toxicity_keywords = [
            'hate', 'kill', 'death', 'suicide', 'harm', 'hurt', 'attack',
            'bomb', 'weapon', 'drug', 'illegal', 'criminal', 'fraud',
            'scam', 'phishing', 'hack', 'steal', 'rob', 'threat'
        ]
        
        # Apple-specific sensitive topics
        self.apple_sensitive_topics = [
            'employee', 'internal', 'confidential', 'secret', 'beta',
            'unreleased', 'future product', 'roadmap', 'strategy'
        ]
        
        # Rate limiting
        self.rate_limit_window = 60  # seconds
        self.rate_limit_max_requests = 10
        self.user_requests = {}  # In production, use Redis or similar
    
    def check_message(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """Check message for various guardrails"""
        message_lower = message.lower()
        
        # Check for personal data
        personal_data_check = self._check_personal_data(message)
        if personal_data_check['found']:
            return {
                'flagged': True,
                'type': 'personal_data',
                'response': "I notice you've shared some personal information. For your security, I cannot process messages containing personal data like email addresses, phone numbers, or account details. Please remove this information and try again, or contact Apple Support directly for assistance with account-specific issues.",
                'details': personal_data_check
            }
        
        # Check for legal/financial advice requests
        legal_financial_check = self._check_legal_financial(message_lower)
        if legal_financial_check['found']:
            return {
                'flagged': True,
                'type': 'legal_financial',
                'response': "I cannot provide legal or financial advice. For legal matters related to Apple products or services, please consult with a qualified attorney. For financial issues, please contact Apple Support directly or consult with a financial advisor.",
                'details': legal_financial_check
            }
        
        # Check for toxicity
        toxicity_check = self._check_toxicity(message_lower)
        if toxicity_check['found']:
            return {
                'flagged': True,
                'type': 'toxicity',
                'response': "I'm here to help with Apple product and service questions. I cannot assist with harmful or inappropriate requests. If you have a legitimate Apple-related issue, I'd be happy to help. Otherwise, please contact Apple Support directly.",
                'details': toxicity_check
            }
        
        # Check for Apple-sensitive topics
        apple_sensitive_check = self._check_apple_sensitive(message_lower)
        if apple_sensitive_check['found']:
            return {
                'flagged': True,
                'type': 'apple_sensitive',
                'response': "I can only provide information about publicly available Apple products and services. For internal or confidential matters, please contact Apple Support directly.",
                'details': apple_sensitive_check
            }
        
        # Check rate limiting
        if user_id:
            rate_limit_check = self._check_rate_limit(user_id)
            if rate_limit_check['exceeded']:
                return {
                    'flagged': True,
                    'type': 'rate_limit',
                    'response': "You're sending messages too quickly. Please wait a moment before sending another message.",
                    'details': rate_limit_check
                }
        
        return {
            'flagged': False,
            'type': None,
            'response': None
        }
    
    def _check_personal_data(self, message: str) -> Dict[str, Any]:
        """Check for personal data patterns"""
        found_patterns = {}
        
        for data_type, pattern in self.personal_data_patterns.items():
            matches = re.findall(pattern, message, re.IGNORECASE)
            if matches:
                found_patterns[data_type] = {
                    'count': len(matches),
                    'examples': matches[:3]  # Limit to first 3 examples
                }
        
        return {
            'found': bool(found_patterns),
            'patterns': found_patterns
        }
    
    def _check_legal_financial(self, message_lower: str) -> Dict[str, Any]:
        """Check for legal/financial advice requests"""
        found_keywords = []
        
        for keyword in self.legal_financial_keywords:
            if keyword in message_lower:
                found_keywords.append(keyword)
        
        return {
            'found': bool(found_keywords),
            'keywords': found_keywords
        }
    
    def _check_toxicity(self, message_lower: str) -> Dict[str, Any]:
        """Check for toxic content"""
        found_keywords = []
        
        for keyword in self.toxicity_keywords:
            if keyword in message_lower:
                found_keywords.append(keyword)
        
        return {
            'found': bool(found_keywords),
            'keywords': found_keywords
        }
    
    def _check_apple_sensitive(self, message_lower: str) -> Dict[str, Any]:
        """Check for Apple-sensitive topics"""
        found_topics = []
        
        for topic in self.apple_sensitive_topics:
            if topic in message_lower:
                found_topics.append(topic)
        
        return {
            'found': bool(found_topics),
            'topics': found_topics
        }
    
    def _check_rate_limit(self, user_id: str) -> Dict[str, Any]:
        """Check rate limiting for user"""
        import time
        current_time = time.time()
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
        
        # Clean old requests
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Add current request
        self.user_requests[user_id].append(current_time)
        
        # Check if limit exceeded
        exceeded = len(self.user_requests[user_id]) > self.rate_limit_max_requests
        
        return {
            'exceeded': exceeded,
            'current_requests': len(self.user_requests[user_id]),
            'max_requests': self.rate_limit_max_requests,
            'window_seconds': self.rate_limit_window
        }
    
    def sanitize_message(self, message: str) -> str:
        """Sanitize message by removing personal data"""
        sanitized = message
        
        for data_type, pattern in self.personal_data_patterns.items():
            if data_type == 'email':
                sanitized = re.sub(pattern, '[EMAIL_ADDRESS]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'phone':
                sanitized = re.sub(pattern, '[PHONE_NUMBER]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'ssn':
                sanitized = re.sub(pattern, '[SSN]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'credit_card':
                sanitized = re.sub(pattern, '[CREDIT_CARD]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'address':
                sanitized = re.sub(pattern, '[ADDRESS]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'apple_id':
                sanitized = re.sub(pattern, '[APPLE_ID]', sanitized, flags=re.IGNORECASE)
            elif data_type == 'device_id':
                sanitized = re.sub(pattern, '[DEVICE_ID]', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def log_violation(self, user_id: str, violation_type: str, details: Dict[str, Any]):
        """Log guardrail violations for monitoring"""
        logger.warning(f"Guardrail violation - User: {user_id}, Type: {violation_type}, Details: {details}")
        
        # In production, you would send this to a monitoring service
        # like DataDog, New Relic, or a custom logging system
    
    def get_guardrail_stats(self) -> Dict[str, Any]:
        """Get statistics about guardrail usage"""
        return {
            'rate_limit_window': self.rate_limit_window,
            'rate_limit_max_requests': self.rate_limit_max_requests,
            'active_users': len(self.user_requests),
            'personal_data_patterns': len(self.personal_data_patterns),
            'legal_financial_keywords': len(self.legal_financial_keywords),
            'toxicity_keywords': len(self.toxicity_keywords),
            'apple_sensitive_topics': len(self.apple_sensitive_topics)
        }

# Global instance
guardrails = GuardrailsService() 