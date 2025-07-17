# src/langgraphagenticai/nodes/ai_news_node.py

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.tools.translation_tool import create_translation_tool
from src.langgraphagenticai.tools.pdf_tool import convert_md_to_pdf
from src.langgraphagenticai.tools.email_tool import send_email_with_attachment
import os

class NewsNode:
    def __init__(self, llm):
        """Initialize the NewsNode with API keys and tools."""
        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}
        self.translation_tool = create_translation_tool(llm)

    def fetch_news(self, state: dict) -> dict:
        """Fetch news and parse user input for frequency, topic, language, and email."""
        message_content = state['messages'][0].content
        
        # Expected format: "frequency:topic:language:email"
        parts = message_content.split(':')
        self.state['frequency'] = parts[0].strip().lower()
        self.state['topic'] = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "general news"
        self.state['target_language'] = parts[2].strip() if len(parts) > 2 and parts[2].strip() else "English"
        self.state['recipient_email'] = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None

        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'yearly': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 366}

        search_query = f"Top latest {self.state['topic']} news India and globally"
        response = self.tavily.search(query=search_query, topic="news", max_results=20, days=days_map.get(self.state['frequency'], 1))
        
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news(self, state: dict) -> dict:
        """Summarize the fetched news using an LLM."""
        # ... (This method remains unchanged)
        news_items = self.state['news_data']
        topic = self.state['topic']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a skilled news summarizer. Your task is to process news articles and create a well-structured markdown summary.

            **Instructions:**
            1. **Date Format**: Use **YYYY-MM-DD** format in IST timezone
            2. **Content**: Create concise, informative summaries (2-3 sentences max per article)
            3. **Organization**: Sort chronologically with latest news first
            4. **Sources**: Include source URL as clickable link
            5. **Quality**: Focus on key facts, avoid redundancy, maintain journalistic tone

            **Output Format:**
            ```
            ### YYYY-MM-DD
            - **[Headline/Key Point]**: [2-3 sentence summary with main facts and implications] ([Source Name](URL))
            ```
            """),
            ("user", "Please summarize the following articles:\n\n{articles}")
        ])
        
        articles_str = "\n\n".join([f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}" for item in news_items])
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state

    def translate_news(self, state: dict) -> dict:
        """Translate the news summary if a target language is specified."""
        # ... (This method remains unchanged)
        target_language = self.state.get('target_language', 'English')
        summary = self.state.get('summary', '')
        if target_language.lower() == 'english':
            self.state['translated_summary'] = summary
        else:
            self.state['translated_summary'] = self.translation_tool._run(summary, target_language)
        return self.state
    
    def save_result(self, state: dict) -> dict:
            """Save the summary to a markdown file with language in the filename."""
            summary = self.state.get('translated_summary', self.state.get('summary', ''))
            topic_clean = self.state['topic'].replace(' ', '_').replace('/', '_')
            frequency = self.state['frequency']
            target_language = self.state.get('target_language', 'English')
            
            # Create directory if it doesn't exist
            news_dir = "./News"
            os.makedirs(news_dir, exist_ok=True)
            
            # --- CORRECTED FILENAME LOGIC ---
            if target_language.lower() == 'english':
                filename = f"{news_dir}/{frequency}_{topic_clean}_summary.md"
                header = f"# {frequency.capitalize()} {topic_clean.title()} News Summary\n\n"
            else:
                language_clean = target_language.replace(' ', '_').replace('(', '').replace(')', '')
                filename = f"{news_dir}/{frequency}_{topic_clean}_{language_clean}_summary.md"
                header = f"# {frequency.capitalize()} {topic_clean.title()} News Summary ({target_language})\n\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(header + summary)
            
            self.state['md_filename'] = filename
            return self.state

    def convert_to_pdf(self, state: dict) -> dict:
        """Convert the saved markdown file to PDF."""
        md_path = self.state.get('md_filename')
        if md_path:
            pdf_path = convert_md_to_pdf(md_path)
            self.state['pdf_filename'] = pdf_path
            print(f"Converted {md_path} to {pdf_path}")
        return self.state

    def send_email(self, state: dict) -> dict:
        """Send the generated PDF as an email attachment if an email is provided."""
        recipient_email = self.state.get('recipient_email')
        pdf_path = self.state.get('pdf_filename')
        
        if recipient_email and pdf_path:
            subject = f"{self.state['frequency'].capitalize()} {self.state['topic'].title()} News Summary"
            body = f"Please find attached the {self.state['frequency']} news summary for '{self.state['topic']}'."
            send_email_with_attachment(recipient_email, subject, body, pdf_path)
            self.state['email_sent'] = True
        return self.state