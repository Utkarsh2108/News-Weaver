# src/langgraphagenticai/utils/message_parser.py
import re
from src.langgraphagenticai.tools.translation_tool import SUPPORTED_LANGUAGES

class NewsMessageParser:
    """
    Parses user messages to extract news-related parameters
    """
    
    def __init__(self):
        self.time_keywords = {
            'daily': ['daily', 'today', 'current', 'latest', 'recent'],
            'weekly': ['weekly', 'week', 'this week', 'past week'],
            'monthly': ['monthly', 'month', 'this month', 'past month'],
            'yearly': ['yearly', 'year', 'annual', 'this year']
        }
        
        self.news_keywords = [
            'news', 'latest', 'update', 'current', 'recent', 'breaking',
            'headlines', 'stories', 'reports', 'coverage', 'articles'
        ]
    
    def is_news_request(self, message: str) -> bool:
        """
        Determines if the message is a news request
        """
        message_lower = message.lower()
        
        # Check for news keywords
        has_news_keyword = any(keyword in message_lower for keyword in self.news_keywords)
        
        # Check for time-related keywords
        has_time_keyword = any(
            any(time_word in message_lower for time_word in time_words)
            for time_words in self.time_keywords.values()
        )
        
        # Check for topic-related patterns
        topic_patterns = [
            r'\b(sports?|technology|tech|politics?|health|business|entertainment|science|world|international)\b',
            r'\b(give me|show me|get me|fetch|provide|tell me about)\b.*\b(news|updates?|headlines?)\b',
            r'\bnews\s+(about|on|regarding|for)\b',
            r'\b(latest|recent|current)\s+(news|updates?|headlines?)\b'
        ]
        
        has_topic_pattern = any(re.search(pattern, message_lower) for pattern in topic_patterns)
        
        return has_news_keyword or (has_time_keyword and has_topic_pattern)
    
    def parse_news_message(self, message: str) -> dict:
        """
        Parses news message and extracts frequency, topic, and language
        Returns dict with parsed parameters
        """
        message_lower = message.lower()
        
        # Extract frequency
        frequency = self._extract_frequency(message_lower)
        
        # Extract topic
        topic = self._extract_topic(message_lower)
        
        # Extract language
        language = self._extract_language(message_lower)
        
        return {
            'frequency': frequency,
            'topic': topic,
            'language': language,
            'formatted_message': f"{frequency}:{topic}:{language}"
        }
    
    def _extract_frequency(self, message: str) -> str:
        """Extract time frequency from message"""
        for frequency, keywords in self.time_keywords.items():
            if any(keyword in message for keyword in keywords):
                return frequency
        return 'daily'  # default
    
    def _extract_topic(self, message: str) -> str:
        """Extract news topic from message"""
        # Common topic patterns
        topic_patterns = {
            r'\b(sports?|sport)\b': 'sports',
            r'\b(tech|technology|technological)\b': 'technology',
            r'\b(politics?|political|government)\b': 'politics',
            r'\b(health|medical|healthcare)\b': 'health',
            r'\b(business|economic|economy|finance|financial)\b': 'business',
            r'\b(entertainment|celebrity|movies?|films?)\b': 'entertainment',
            r'\b(science|scientific|research)\b': 'science',
            r'\b(world|international|global)\b': 'world',
            r'\b(ai|artificial intelligence|machine learning|ml)\b': 'artificial intelligence',
            r'\b(crypto|cryptocurrency|bitcoin|blockchain)\b': 'cryptocurrency',
            r'\b(climate|environment|environmental|global warming)\b': 'climate',
            r'\b(education|educational|school|university)\b': 'education'
        }
        
        for pattern, topic in topic_patterns.items():
            if re.search(pattern, message):
                return topic
        
        # Look for "news about/on X" pattern
        about_pattern = r'\b(news|updates?|headlines?)\s+(about|on|regarding|for)\s+([a-zA-Z\s]+?)(?:\s+in\s+|\s+news|\s*$)'
        match = re.search(about_pattern, message)
        if match:
            extracted_topic = match.group(3).strip()
            if extracted_topic and len(extracted_topic) > 1:
                return extracted_topic
        
        # Look for "give me X news" pattern
        give_pattern = r'\b(give me|show me|get me|fetch|provide)\s+([a-zA-Z\s]+?)\s+(news|updates?|headlines?)\b'
        match = re.search(give_pattern, message)
        if match:
            extracted_topic = match.group(2).strip()
            if extracted_topic and len(extracted_topic) > 1:
                return extracted_topic
        
        return 'general news'  # default
    
    def _extract_language(self, message: str) -> str:
        """Extract target language from message"""
        # Check for explicit language mentions
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            lang_variations = [
                lang_code.lower(),
                lang_name.lower(),
                lang_name.split('(')[0].strip().lower()  # Remove parentheses part
            ]
            
            for variation in lang_variations:
                if variation in message:
                    return lang_code
        
        # Look for "in X language" pattern
        lang_pattern = r'\b(in|translate to|convert to)\s+([a-zA-Z]+)\b'
        match = re.search(lang_pattern, message)
        if match:
            lang_mention = match.group(2).lower()
            for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
                if lang_mention in lang_name.lower() or lang_mention == lang_code.lower():
                    return lang_code
        
        return 'English'  # default

# Example usage and test cases
if __name__ == "__main__":
    parser = NewsMessageParser()
    
    test_messages = [
        "Give me latest sports news in Hindi",
        "Show me technology updates for this week",
        "Provide recent news about politics",
        "Get me daily business news in Spanish",
        "What's the latest news on artificial intelligence?",
        "Fetch weekly entertainment news",
        "Tell me about current health news in French",
        "Show me today's cryptocurrency news",
        "Get monthly climate news in German",
        "Latest news about education"
    ]
    
    print("Testing News Message Parser:")
    print("=" * 50)
    
    for message in test_messages:
        is_news = parser.is_news_request(message)
        if is_news:
            parsed = parser.parse_news_message(message)
            print(f"Message: {message}")
            print(f"Is News: {is_news}")
            print(f"Parsed: {parsed}")
            print(f"Formatted: {parsed['formatted_message']}")
            print("-" * 30)
        else:
            print(f"Message: {message}")
            print(f"Is News: {is_news}")
            print("-" * 30)
