"""
Financial Chatbot Agent
LangChain-based conversational AI for financial analysis
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from src.config.settings import settings
from src.tools.financial_tools import (
    get_income_statement,
    get_balance_sheet,
    get_cash_flow,
    get_stock_info,
    get_financial_ratios,
    compare_companies
)


class FinancialChatbot:
    """
    Financial Analysis Chatbot powered by LangChain and Alpha Vantage API.
    """
    
    def __init__(self):
        """Initialize the financial chatbot"""
        settings.validate_keys()
        
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
        print("✅ Financial Chatbot initialized successfully!")
    
    def _initialize_llm(self):
        """Initialize OpenAI Language Model"""
        return ChatOpenAI(
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key
        )
    
    def _initialize_tools(self):
        """Load financial analysis tools"""
        return [
            get_income_statement,
            get_balance_sheet,
            get_cash_flow,
            get_stock_info,
            get_financial_ratios,
            compare_companies
        ]
    
    def _create_agent(self):
        """Create LangChain agent with financial tools"""
        
        system_prompt = """You are a professional financial analyst AI assistant with access to comprehensive financial data through Alpha Vantage API.

**Your Capabilities:**
• Income Statements - Revenue, expenses, profitability (annual/quarterly)
• Balance Sheets - Assets, liabilities, equity (annual/quarterly)
• Cash Flow Statements - Operating, investing, financing cash flows
• Stock Information - Real-time prices, market cap, company overview
• Financial Ratios - Valuation, profitability, liquidity, leverage metrics
• Company Comparisons - Side-by-side analysis (max 3 companies)

**Available Tools:**
1. get_income_statement(ticker, period) - Revenue and profit data
2. get_balance_sheet(ticker, period) - Assets and liabilities
3. get_cash_flow(ticker, period) - Cash flow analysis
4. get_stock_info(ticker) - Current price and company overview
5. get_financial_ratios(ticker) - Key financial ratios
6. compare_companies(tickers) - Multi-company comparison

**Guidelines:**
• Use ticker symbols (AAPL, MSFT, IBM, etc.)
• Specify period as 'annual' or 'quarterly'
• Provide clear interpretations, not just numbers
• Explain financial terms simply
• Suggest relevant follow-up analyses
• Max 3 companies for comparisons (API limits)

**API Limits (Free Tier):**
• 25 API calls per day
• Rate limiting enforced (5 calls/minute)
• Comparisons include automatic delays

**Response Style:**
• Start with direct answer
• Present data clearly formatted
• Provide insights and context
• Suggest additional analyses

Be professional, accurate, and insightful. Always cite data periods."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            return_intermediate_steps=False
        )
    
    def query(self, user_input: str) -> str:
        """
        Process user query and return response
        
        Args:
            user_input: User's question
            
        Returns:
            Agent's response
        """
        try:
            response = self.agent.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            return f"❌ Error: {str(e)}\n\nPlease rephrase your question or check your API limits."
    
    def get_tools_info(self) -> str:
        """Get information about available tools"""
        info = "\n" + "="*70 + "\n"
        info += "🛠️  Available Financial Analysis Tools\n"
        info += "="*70 + "\n\n"
        
        for i, tool in enumerate(self.tools, 1):
            info += f"{i}. {tool.name}\n"
            info += f"   {tool.description}\n\n"
        
        return info
