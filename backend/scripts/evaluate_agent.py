#!/usr/bin/env python3
"""
Evaluation Framework for Apple Support AI Agent

This script evaluates the AI agent against 50+ realistic test scenarios
to measure accuracy, helpfulness, and citation quality.
"""

import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.ai_agent import ai_agent
from app.services.vector_store import vector_store

class AgentEvaluator:
    def __init__(self):
        self.test_scenarios = self._load_test_scenarios()
        self.results = []
        
    def _load_test_scenarios(self) -> List[Dict[str, Any]]:
        """Load test scenarios from the evaluation data"""
        scenarios = [
            # iPhone Related Questions
            {
                "id": "iphone_001",
                "category": "iPhone",
                "question": "How do I reset my iPhone to factory settings?",
                "expected_keywords": ["factory reset", "erase", "settings", "general"],
                "expected_sources": ["iPhone", "reset", "factory"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            {
                "id": "iphone_002",
                "category": "iPhone",
                "question": "My iPhone won't turn on, what should I do?",
                "expected_keywords": ["power", "battery", "force restart", "hardware"],
                "expected_sources": ["iPhone", "power", "battery"],
                "difficulty": "high",
                "type": "troubleshooting"
            },
            {
                "id": "iphone_003",
                "category": "iPhone",
                "question": "How do I transfer data from my old iPhone to a new one?",
                "expected_keywords": ["transfer", "iCloud", "backup", "restore"],
                "expected_sources": ["iPhone", "transfer", "backup"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "iphone_004",
                "category": "iPhone",
                "question": "What's the difference between iPhone 14 and iPhone 15?",
                "expected_keywords": ["specifications", "features", "comparison", "upgrade"],
                "expected_sources": ["iPhone", "comparison", "specifications"],
                "difficulty": "easy",
                "type": "information"
            },
            {
                "id": "iphone_005",
                "category": "iPhone",
                "question": "How do I enable Face ID on my iPhone?",
                "expected_keywords": ["Face ID", "settings", "security", "biometric"],
                "expected_sources": ["iPhone", "Face ID", "security"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # iPad Related Questions
            {
                "id": "ipad_001",
                "category": "iPad",
                "question": "How do I connect my iPad to a wireless printer?",
                "expected_keywords": ["printer", "wireless", "AirPrint", "network"],
                "expected_sources": ["iPad", "printer", "AirPrint"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "ipad_002",
                "category": "iPad",
                "question": "Can I use my iPad as a second monitor for my Mac?",
                "expected_keywords": ["Sidecar", "second monitor", "display", "Mac"],
                "expected_sources": ["iPad", "Sidecar", "Mac"],
                "difficulty": "medium",
                "type": "information"
            },
            {
                "id": "ipad_003",
                "category": "iPad",
                "question": "How do I update my iPad to the latest iOS version?",
                "expected_keywords": ["update", "iOS", "software", "settings"],
                "expected_sources": ["iPad", "update", "iOS"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Mac Related Questions
            {
                "id": "mac_001",
                "category": "Mac",
                "question": "How do I check if my Mac is compatible with macOS Sonoma?",
                "expected_keywords": ["compatibility", "macOS", "system requirements", "check"],
                "expected_sources": ["Mac", "macOS", "compatibility"],
                "difficulty": "easy",
                "type": "information"
            },
            {
                "id": "mac_002",
                "category": "Mac",
                "question": "My Mac is running very slowly, how can I speed it up?",
                "expected_keywords": ["performance", "slow", "optimization", "storage"],
                "expected_sources": ["Mac", "performance", "optimization"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            {
                "id": "mac_003",
                "category": "Mac",
                "question": "How do I connect my Mac to an external display?",
                "expected_keywords": ["external display", "monitor", "connect", "ports"],
                "expected_sources": ["Mac", "display", "connect"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Apple Watch Related Questions
            {
                "id": "watch_001",
                "category": "Apple Watch",
                "question": "How do I pair my Apple Watch with my iPhone?",
                "expected_keywords": ["pair", "setup", "iPhone", "Watch app"],
                "expected_sources": ["Apple Watch", "pair", "setup"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "watch_002",
                "category": "Apple Watch",
                "question": "My Apple Watch battery is draining quickly, what can I do?",
                "expected_keywords": ["battery", "drain", "optimization", "settings"],
                "expected_sources": ["Apple Watch", "battery", "optimization"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # AirPods Related Questions
            {
                "id": "airpods_001",
                "category": "AirPods",
                "question": "How do I reset my AirPods?",
                "expected_keywords": ["reset", "forget", "reconnect", "settings"],
                "expected_sources": ["AirPods", "reset", "setup"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "airpods_002",
                "category": "AirPods",
                "question": "One of my AirPods is not working, how do I fix it?",
                "expected_keywords": ["one AirPod", "not working", "audio", "troubleshoot"],
                "expected_sources": ["AirPods", "troubleshooting", "audio"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # iCloud Related Questions
            {
                "id": "icloud_001",
                "category": "iCloud",
                "question": "How do I check my iCloud storage usage?",
                "expected_keywords": ["iCloud", "storage", "usage", "check"],
                "expected_sources": ["iCloud", "storage", "usage"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "icloud_002",
                "category": "iCloud",
                "question": "How do I backup my iPhone to iCloud?",
                "expected_keywords": ["backup", "iCloud", "settings", "automatic"],
                "expected_sources": ["iCloud", "backup", "iPhone"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # App Store Related Questions
            {
                "id": "appstore_001",
                "category": "App Store",
                "question": "How do I update apps on my iPhone?",
                "expected_keywords": ["update", "apps", "App Store", "automatic"],
                "expected_sources": ["App Store", "update", "apps"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "appstore_002",
                "category": "App Store",
                "question": "I can't download apps from the App Store, what's wrong?",
                "expected_keywords": ["download", "error", "payment", "network"],
                "expected_sources": ["App Store", "download", "troubleshooting"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # Security Related Questions
            {
                "id": "security_001",
                "category": "Security",
                "question": "How do I enable two-factor authentication on my Apple ID?",
                "expected_keywords": ["two-factor", "authentication", "security", "Apple ID"],
                "expected_sources": ["security", "two-factor", "Apple ID"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "security_002",
                "category": "Security",
                "question": "I forgot my iPhone passcode, how do I unlock it?",
                "expected_keywords": ["passcode", "forgot", "unlock", "reset"],
                "expected_sources": ["security", "passcode", "unlock"],
                "difficulty": "high",
                "type": "troubleshooting"
            },
            
            # Software Update Questions
            {
                "id": "software_001",
                "category": "Software",
                "question": "How do I update my iPhone to iOS 17?",
                "expected_keywords": ["update", "iOS", "software", "settings"],
                "expected_sources": ["software", "update", "iOS"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "software_002",
                "category": "Software",
                "question": "My iPhone says it needs more storage to update, what can I do?",
                "expected_keywords": ["storage", "space", "delete", "clean up"],
                "expected_sources": ["software", "storage", "update"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # Hardware Questions
            {
                "id": "hardware_001",
                "category": "Hardware",
                "question": "How do I clean my iPhone screen safely?",
                "expected_keywords": ["clean", "screen", "safely", "microfiber"],
                "expected_sources": ["hardware", "clean", "screen"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "hardware_002",
                "category": "Hardware",
                "question": "My iPhone camera is blurry, how do I fix it?",
                "expected_keywords": ["camera", "blurry", "lens", "clean"],
                "expected_sources": ["hardware", "camera", "troubleshooting"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # Network Questions
            {
                "id": "network_001",
                "category": "Network",
                "question": "How do I connect my iPhone to WiFi?",
                "expected_keywords": ["WiFi", "connect", "settings", "network"],
                "expected_sources": ["network", "WiFi", "connect"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "network_002",
                "category": "Network",
                "question": "My iPhone won't connect to WiFi, what should I do?",
                "expected_keywords": ["WiFi", "troubleshoot", "forget", "reset"],
                "expected_sources": ["network", "WiFi", "troubleshooting"],
                "difficulty": "medium",
                "type": "troubleshooting"
            },
            
            # Privacy Questions
            {
                "id": "privacy_001",
                "category": "Privacy",
                "question": "How do I control which apps can access my location?",
                "expected_keywords": ["privacy", "location", "settings", "apps"],
                "expected_sources": ["privacy", "location", "settings"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "privacy_002",
                "category": "Privacy",
                "question": "How do I delete my browsing history on Safari?",
                "expected_keywords": ["Safari", "history", "delete", "clear"],
                "expected_sources": ["privacy", "Safari", "history"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Accessibility Questions
            {
                "id": "accessibility_001",
                "category": "Accessibility",
                "question": "How do I enable VoiceOver on my iPhone?",
                "expected_keywords": ["VoiceOver", "accessibility", "settings", "screen reader"],
                "expected_sources": ["accessibility", "VoiceOver", "settings"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "accessibility_002",
                "category": "Accessibility",
                "question": "How do I make text larger on my iPhone?",
                "expected_keywords": ["text size", "larger", "accessibility", "display"],
                "expected_sources": ["accessibility", "text size", "display"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Family Sharing Questions
            {
                "id": "family_001",
                "category": "Family Sharing",
                "question": "How do I set up Family Sharing on my iPhone?",
                "expected_keywords": ["Family Sharing", "setup", "family", "organizer"],
                "expected_sources": ["Family Sharing", "setup", "family"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "family_002",
                "category": "Family Sharing",
                "question": "How do I add a family member to Family Sharing?",
                "expected_keywords": ["add member", "invite", "Family Sharing", "email"],
                "expected_sources": ["Family Sharing", "add member", "invite"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Apple Music Questions
            {
                "id": "music_001",
                "category": "Apple Music",
                "question": "How do I download songs for offline listening on Apple Music?",
                "expected_keywords": ["download", "offline", "Apple Music", "library"],
                "expected_sources": ["Apple Music", "download", "offline"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "music_002",
                "category": "Apple Music",
                "question": "How do I cancel my Apple Music subscription?",
                "expected_keywords": ["cancel", "subscription", "Apple Music", "settings"],
                "expected_sources": ["Apple Music", "cancel", "subscription"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Apple TV Questions
            {
                "id": "tv_001",
                "category": "Apple TV",
                "question": "How do I connect my Apple TV to my TV?",
                "expected_keywords": ["connect", "HDMI", "setup", "TV"],
                "expected_sources": ["Apple TV", "connect", "setup"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "tv_002",
                "category": "Apple TV",
                "question": "How do I update my Apple TV software?",
                "expected_keywords": ["update", "software", "tvOS", "settings"],
                "expected_sources": ["Apple TV", "update", "tvOS"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Apple Pay Questions
            {
                "id": "pay_001",
                "category": "Apple Pay",
                "question": "How do I set up Apple Pay on my iPhone?",
                "expected_keywords": ["Apple Pay", "setup", "card", "Wallet"],
                "expected_sources": ["Apple Pay", "setup", "Wallet"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "pay_002",
                "category": "Apple Pay",
                "question": "How do I add a credit card to Apple Pay?",
                "expected_keywords": ["add card", "credit card", "Apple Pay", "Wallet"],
                "expected_sources": ["Apple Pay", "add card", "Wallet"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Find My Questions
            {
                "id": "findmy_001",
                "category": "Find My",
                "question": "How do I find my lost iPhone using Find My?",
                "expected_keywords": ["Find My", "lost", "locate", "iCloud"],
                "expected_sources": ["Find My", "lost", "locate"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "findmy_002",
                "category": "Find My",
                "question": "How do I enable Find My on my iPhone?",
                "expected_keywords": ["Find My", "enable", "settings", "location"],
                "expected_sources": ["Find My", "enable", "settings"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Siri Questions
            {
                "id": "siri_001",
                "category": "Siri",
                "question": "How do I enable Siri on my iPhone?",
                "expected_keywords": ["Siri", "enable", "settings", "voice"],
                "expected_sources": ["Siri", "enable", "settings"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "siri_002",
                "category": "Siri",
                "question": "How do I change Siri's voice?",
                "expected_keywords": ["Siri", "voice", "change", "settings"],
                "expected_sources": ["Siri", "voice", "settings"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Battery Questions
            {
                "id": "battery_001",
                "category": "Battery",
                "question": "How do I check my iPhone's battery health?",
                "expected_keywords": ["battery health", "check", "settings", "capacity"],
                "expected_sources": ["battery", "health", "settings"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "battery_002",
                "category": "Battery",
                "question": "How can I extend my iPhone's battery life?",
                "expected_keywords": ["battery life", "extend", "optimize", "settings"],
                "expected_sources": ["battery", "life", "optimization"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Storage Questions
            {
                "id": "storage_001",
                "category": "Storage",
                "question": "How do I check my iPhone's storage usage?",
                "expected_keywords": ["storage", "usage", "check", "settings"],
                "expected_sources": ["storage", "usage", "settings"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "storage_002",
                "category": "Storage",
                "question": "How do I free up storage space on my iPhone?",
                "expected_keywords": ["free up", "storage", "delete", "clean"],
                "expected_sources": ["storage", "free up", "clean"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Camera Questions
            {
                "id": "camera_001",
                "category": "Camera",
                "question": "How do I take a screenshot on my iPhone?",
                "expected_keywords": ["screenshot", "capture", "buttons", "volume"],
                "expected_sources": ["camera", "screenshot", "capture"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "camera_002",
                "category": "Camera",
                "question": "How do I use Portrait mode on my iPhone camera?",
                "expected_keywords": ["Portrait mode", "camera", "depth", "blur"],
                "expected_sources": ["camera", "Portrait mode", "depth"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Messages Questions
            {
                "id": "messages_001",
                "category": "Messages",
                "question": "How do I send a text message on my iPhone?",
                "expected_keywords": ["text message", "send", "Messages app", "compose"],
                "expected_sources": ["Messages", "text", "send"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "messages_002",
                "category": "Messages",
                "question": "How do I delete text messages on my iPhone?",
                "expected_keywords": ["delete", "messages", "conversation", "swipe"],
                "expected_sources": ["Messages", "delete", "conversation"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Mail Questions
            {
                "id": "mail_001",
                "category": "Mail",
                "question": "How do I add an email account to my iPhone?",
                "expected_keywords": ["email", "account", "add", "settings"],
                "expected_sources": ["Mail", "email", "account"],
                "difficulty": "medium",
                "type": "how_to"
            },
            {
                "id": "mail_002",
                "category": "Mail",
                "question": "How do I organize my emails into folders on iPhone?",
                "expected_keywords": ["folders", "organize", "mailboxes", "create"],
                "expected_sources": ["Mail", "folders", "organize"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Calendar Questions
            {
                "id": "calendar_001",
                "category": "Calendar",
                "question": "How do I create a new calendar event on my iPhone?",
                "expected_keywords": ["calendar", "event", "create", "add"],
                "expected_sources": ["Calendar", "event", "create"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "calendar_002",
                "category": "Calendar",
                "question": "How do I sync my iPhone calendar with my Mac?",
                "expected_keywords": ["sync", "calendar", "iCloud", "Mac"],
                "expected_sources": ["Calendar", "sync", "iCloud"],
                "difficulty": "medium",
                "type": "how_to"
            },
            
            # Photos Questions
            {
                "id": "photos_001",
                "category": "Photos",
                "question": "How do I share photos from my iPhone?",
                "expected_keywords": ["share", "photos", "select", "share button"],
                "expected_sources": ["Photos", "share", "select"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "photos_002",
                "category": "Photos",
                "question": "How do I create a photo album on my iPhone?",
                "expected_keywords": ["album", "create", "photos", "organize"],
                "expected_sources": ["Photos", "album", "create"],
                "difficulty": "easy",
                "type": "how_to"
            },
            
            # Settings Questions
            {
                "id": "settings_001",
                "category": "Settings",
                "question": "How do I change my iPhone's wallpaper?",
                "expected_keywords": ["wallpaper", "background", "settings", "choose"],
                "expected_sources": ["Settings", "wallpaper", "background"],
                "difficulty": "easy",
                "type": "how_to"
            },
            {
                "id": "settings_002",
                "category": "Settings",
                "question": "How do I change the language on my iPhone?",
                "expected_keywords": ["language", "change", "settings", "general"],
                "expected_sources": ["Settings", "language", "general"],
                "difficulty": "medium",
                "type": "how_to"
            }
        ]
        
        return scenarios
    
    async def evaluate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single test scenario"""
        print(f"Evaluating: {scenario['question']}")
        
        try:
            # Get AI response
            response = ai_agent.generate_response(scenario['question'])
            
            # Evaluate accuracy
            accuracy_score = self._evaluate_accuracy(response, scenario)
            
            # Evaluate helpfulness
            helpfulness_score = self._evaluate_helpfulness(response, scenario)
            
            # Evaluate citation quality
            citation_score = self._evaluate_citations(response, scenario)
            
            # Calculate overall score
            overall_score = (accuracy_score + helpfulness_score + citation_score) / 3
            
            result = {
                "scenario_id": scenario["id"],
                "category": scenario["category"],
                "question": scenario["question"],
                "ai_response": response["message"],
                "sources": response.get("sources", []),
                "confidence": response.get("confidence", 0.0),
                "scores": {
                    "accuracy": accuracy_score,
                    "helpfulness": helpfulness_score,
                    "citations": citation_score,
                    "overall": overall_score
                },
                "expected_keywords": scenario["expected_keywords"],
                "expected_sources": scenario["expected_sources"],
                "difficulty": scenario["difficulty"],
                "type": scenario["type"],
                "evaluated_at": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            print(f"Error evaluating scenario {scenario['id']}: {e}")
            return {
                "scenario_id": scenario["id"],
                "error": str(e),
                "scores": {
                    "accuracy": 0.0,
                    "helpfulness": 0.0,
                    "citations": 0.0,
                    "overall": 0.0
                }
            }
    
    def _evaluate_accuracy(self, response: Dict[str, Any], scenario: Dict[str, Any]) -> float:
        """Evaluate the accuracy of the response"""
        score = 0.0
        response_text = response["message"].lower()
        
        # Check for expected keywords
        keyword_matches = 0
        for keyword in scenario["expected_keywords"]:
            if keyword.lower() in response_text:
                keyword_matches += 1
        
        keyword_score = keyword_matches / len(scenario["expected_keywords"])
        score += keyword_score * 0.4  # 40% weight for keywords
        
        # Check if response is relevant to the question
        relevance_score = 0.0
        if any(word in response_text for word in scenario["question"].lower().split()):
            relevance_score = 1.0
        
        score += relevance_score * 0.3  # 30% weight for relevance
        
        # Check for technical accuracy (basic heuristics)
        technical_score = 0.0
        if "apple" in response_text or "iphone" in response_text or "settings" in response_text:
            technical_score = 1.0
        
        score += technical_score * 0.3  # 30% weight for technical accuracy
        
        return min(score, 1.0)
    
    def _evaluate_helpfulness(self, response: Dict[str, Any], scenario: Dict[str, Any]) -> float:
        """Evaluate the helpfulness of the response"""
        score = 0.0
        response_text = response["message"]
        
        # Check response length (not too short, not too long)
        length_score = 0.0
        if 50 <= len(response_text) <= 500:
            length_score = 1.0
        elif 25 <= len(response_text) <= 1000:
            length_score = 0.7
        
        score += length_score * 0.2  # 20% weight for length
        
        # Check for actionable steps
        action_score = 0.0
        action_words = ["step", "tap", "select", "choose", "enable", "disable", "go to", "open"]
        if any(word in response_text.lower() for word in action_words):
            action_score = 1.0
        
        score += action_score * 0.3  # 30% weight for actionable content
        
        # Check for empathy and tone
        tone_score = 0.0
        positive_words = ["help", "assist", "guide", "support", "recommend", "suggest"]
        if any(word in response_text.lower() for word in positive_words):
            tone_score = 1.0
        
        score += tone_score * 0.2  # 20% weight for tone
        
        # Check for completeness
        completeness_score = 0.0
        if len(response_text) > 100 and "." in response_text:
            completeness_score = 1.0
        
        score += completeness_score * 0.3  # 30% weight for completeness
        
        return min(score, 1.0)
    
    def _evaluate_citations(self, response: Dict[str, Any], scenario: Dict[str, Any]) -> float:
        """Evaluate the quality of citations"""
        score = 0.0
        sources = response.get("sources", [])
        
        # Check if sources are provided
        if sources:
            score += 0.4  # 40% for having sources
        
        # Check source relevance
        relevant_sources = 0
        for source in sources:
            source_text = f"{source.get('title', '')} {source.get('product', '')}".lower()
            if any(expected in source_text for expected in scenario["expected_sources"]):
                relevant_sources += 1
        
        if sources:
            relevance_score = relevant_sources / len(sources)
            score += relevance_score * 0.3  # 30% for relevance
        
        # Check source quality (URLs, titles)
        quality_score = 0.0
        for source in sources:
            if source.get("url") and source.get("title"):
                quality_score += 1
        
        if sources:
            quality_score = quality_score / len(sources)
            score += quality_score * 0.3  # 30% for quality
        
        return min(score, 1.0)
    
    async def run_evaluation(self) -> Dict[str, Any]:
        """Run the complete evaluation"""
        print("Starting AI Agent Evaluation...")
        print(f"Testing {len(self.test_scenarios)} scenarios...")
        
        results = []
        for scenario in self.test_scenarios:
            result = await self.evaluate_scenario(scenario)
            results.append(result)
            await asyncio.sleep(1)  # Rate limiting
        
        # Calculate overall statistics
        stats = self._calculate_statistics(results)
        
        # Save results
        self._save_results(results, stats)
        
        return {
            "results": results,
            "statistics": stats,
            "evaluated_at": datetime.now().isoformat()
        }
    
    def _calculate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate evaluation statistics"""
        valid_results = [r for r in results if "error" not in r]
        
        if not valid_results:
            return {"error": "No valid results to analyze"}
        
        # Overall scores
        accuracy_scores = [r["scores"]["accuracy"] for r in valid_results]
        helpfulness_scores = [r["scores"]["helpfulness"] for r in valid_results]
        citation_scores = [r["scores"]["citations"] for r in valid_results]
        overall_scores = [r["scores"]["overall"] for r in valid_results]
        
        # Category breakdown
        categories = {}
        for result in valid_results:
            category = result["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(result["scores"]["overall"])
        
        category_avg = {cat: sum(scores) / len(scores) for cat, scores in categories.items()}
        
        # Difficulty breakdown
        difficulties = {}
        for result in valid_results:
            difficulty = result["difficulty"]
            if difficulty not in difficulties:
                difficulties[difficulty] = []
            difficulties[difficulty].append(result["scores"]["overall"])
        
        difficulty_avg = {diff: sum(scores) / len(scores) for diff, scores in difficulties.items()}
        
        return {
            "total_scenarios": len(results),
            "valid_scenarios": len(valid_results),
            "overall_scores": {
                "accuracy": {
                    "average": sum(accuracy_scores) / len(accuracy_scores),
                    "min": min(accuracy_scores),
                    "max": max(accuracy_scores)
                },
                "helpfulness": {
                    "average": sum(helpfulness_scores) / len(helpfulness_scores),
                    "min": min(helpfulness_scores),
                    "max": max(helpfulness_scores)
                },
                "citations": {
                    "average": sum(citation_scores) / len(citation_scores),
                    "min": min(citation_scores),
                    "max": max(citation_scores)
                },
                "overall": {
                    "average": sum(overall_scores) / len(overall_scores),
                    "min": min(overall_scores),
                    "max": max(overall_scores)
                }
            },
            "category_performance": category_avg,
            "difficulty_performance": difficulty_avg,
            "top_performers": sorted(valid_results, key=lambda x: x["scores"]["overall"], reverse=True)[:5],
            "bottom_performers": sorted(valid_results, key=lambda x: x["scores"]["overall"])[:5]
        }
    
    def _save_results(self, results: List[Dict[str, Any]], stats: Dict[str, Any]):
        """Save evaluation results to file"""
        os.makedirs("data", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = f"data/evaluation_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save summary statistics
        stats_file = f"data/evaluation_stats_{timestamp}.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"Results saved to: {results_file}")
        print(f"Statistics saved to: {stats_file}")
    
    def print_summary(self, stats: Dict[str, Any]):
        """Print evaluation summary"""
        print("\n" + "="*50)
        print("EVALUATION SUMMARY")
        print("="*50)
        
        if "error" in stats:
            print(f"Error: {stats['error']}")
            return
        
        overall = stats["overall_scores"]["overall"]
        print(f"Overall Performance: {overall['average']:.2f}/1.0")
        print(f"Accuracy: {stats['overall_scores']['accuracy']['average']:.2f}/1.0")
        print(f"Helpfulness: {stats['overall_scores']['helpfulness']['average']:.2f}/1.0")
        print(f"Citations: {stats['overall_scores']['citations']['average']:.2f}/1.0")
        
        print(f"\nScenarios Tested: {stats['valid_scenarios']}/{stats['total_scenarios']}")
        
        print("\nCategory Performance:")
        for category, score in stats["category_performance"].items():
            print(f"  {category}: {score:.2f}/1.0")
        
        print("\nDifficulty Performance:")
        for difficulty, score in stats["difficulty_performance"].items():
            print(f"  {difficulty}: {score:.2f}/1.0")
        
        print("\nTop 3 Performers:")
        for i, result in enumerate(stats["top_performers"][:3], 1):
            print(f"  {i}. {result['question'][:50]}... (Score: {result['scores']['overall']:.2f})")
        
        print("\nAreas for Improvement:")
        for i, result in enumerate(stats["bottom_performers"][:3], 1):
            print(f"  {i}. {result['question'][:50]}... (Score: {result['scores']['overall']:.2f})")

async def main():
    """Main evaluation function"""
    evaluator = AgentEvaluator()
    
    # Run evaluation
    evaluation_result = await evaluator.run_evaluation()
    
    # Print summary
    evaluator.print_summary(evaluation_result["statistics"])
    
    return evaluation_result

if __name__ == "__main__":
    asyncio.run(main()) 