#!/usr/bin/env python3
"""
Financial Data Analysis Chatbot
Built with LangChain and Alpha Vantage API
"""

from src.agent.financial_agent import FinancialChatbot
from src.config.settings import settings
import sys


def print_header():
    """Display welcome header"""
    header = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🤖 FINANCIAL DATA ANALYSIS CHATBOT 💹                    ║
║                                                                    ║
║           Powered by LangChain + Alpha Vantage API                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

Welcome! I can help you analyze financial data for publicly traded companies.

📊 Example Queries:
  • What was IBM's revenue in 2023?
  • Show me Microsoft's balance sheet
  • Compare AAPL, MSFT, and GOOGL
  • Calculate financial ratios for Tesla
  • What is Amazon's current stock price?

💡 Tips:
  • Use ticker symbols (AAPL, MSFT, IBM, etc.)
  • Specify 'annual' or 'quarterly' for time periods
  • Free tier: 25 API calls/day, 5/minute

⚙️  Commands:
  • 'help' - Show help
  • 'tools' - List all tools
  • 'exit' - Quit

"""
    print(header)


def print_help():
    """Display help information"""
    help_text = """
╔════════════════════════════════════════════════════════════════════╗
║ HELP & USAGE GUIDE                                                 ║
╚════════════════════════════════════════════════════════════════════╝

📌 Available Commands:
  help     - Show this help message
  tools    - List all available analysis tools
  exit     - Exit the chatbot

📊 Analysis Capabilities:
  • Income Statements - Revenue, expenses, profitability
  • Balance Sheets - Assets, liabilities, equity
  • Cash Flow - Operating, investing, financing flows
  • Stock Info - Current prices, market data, company overview
  • Financial Ratios - ROE, ROA, P/E, debt ratios, etc.
  • Comparisons - Compare up to 3 companies side-by-side

📝 Example Questions:
  • "What was AAPL's revenue last quarter?"
  • "Show me the balance sheet for Microsoft"
  • "Compare Apple, Microsoft, and Google"
  • "Calculate profitability ratios for Tesla"
  • "What is Amazon's current stock price?"
  • "Show me IBM's cash flow statement"

⚠️  API Limits (Free Tier):
  • 25 API calls per day
  • 5 calls per minute (automatic rate limiting)
  • Comparisons limited to 3 companies

💡 Pro Tips:
  • Be specific with ticker symbols
  • Specify time period when relevant
  • Use quarterly for recent data
  • One company at a time for detailed analysis

"""
    print(help_text)


def main():
    """Main application loop"""
    
    # Validate configuration
    try:
        settings.validate_keys()
    except ValueError as e:
        print(e)
        print("\n📝 Setup Instructions:")
        print("1. Create a .env file in the project root")
        print("2. Add: OPENAI_API_KEY=your_key_here")
        print("3. Add: ALPHA_VANTAGE_API_KEY=your_key_here")
        print("4. Get free Alpha Vantage key: https://www.alphavantage.co/support/#api-key\n")
        sys.exit(1)
    
    # Display welcome
    print_header()
    
    # Initialize chatbot
    print("🔄 Initializing chatbot...\n")
    try:
        chatbot = FinancialChatbot()
        print()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}\n")
        sys.exit(1)
    
    # Main conversation loop
    query_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n👋 Thanks for using Financial Analysis Chatbot. Goodbye!\n")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'tools':
                print(chatbot.get_tools_info())
                continue
            
            # Process financial query
            query_count += 1
            print(f"\n🤖 Assistant: ", end="", flush=True)
            
            response = chatbot.query(user_input)
            print(response)
            
            # API usage reminder
            if query_count % 5 == 0:
                print(f"\n💡 Tip: You've made ~{query_count} queries. Free tier: 25 calls/day.\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    main()
