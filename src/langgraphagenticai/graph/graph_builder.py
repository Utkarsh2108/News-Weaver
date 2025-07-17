# src/langgraphagenticai/graph/graph_builder.py
from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.nodes.ai_news_node import NewsNode
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        tools = get_tools()
        tool_node = create_tool_node(tools)
        llm = self.llm
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")


    def news_builder_graph(self):
        """Builds a news processing pipeline with PDF conversion and email support."""
        news_node = NewsNode(self.llm)

        # Add the nodes
        self.graph_builder.add_node("fetch_news", news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", news_node.summarize_news)
        self.graph_builder.add_node("translate_news", news_node.translate_news)
        self.graph_builder.add_node("save_result", news_node.save_result)
        self.graph_builder.add_node("convert_to_pdf", news_node.convert_to_pdf)
        self.graph_builder.add_node("send_email", news_node.send_email)

        # Add the edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "translate_news")
        self.graph_builder.add_edge("translate_news", "save_result")
        self.graph_builder.add_edge("save_result", "convert_to_pdf")
        self.graph_builder.add_edge("convert_to_pdf", "send_email")
        self.graph_builder.add_edge("send_email", END)

    def setup_graph(self, usecase: str):
        """Sets up the graph for the selected use case."""
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()
        elif usecase == "News":
            self.news_builder_graph()
        return self.graph_builder.compile()