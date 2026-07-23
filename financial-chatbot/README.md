# Financial Data Analysis Chatbot

A command-line financial analysis assistant powered by LangChain, OpenAI, and the Alpha Vantage API. Ask questions about public companies and receive analysis of financial statements, stock information, financial ratios, and comparisons.

## Features

- Income statement analysis
- Balance sheet analysis
- Cash flow analysis
- Stock prices and company information
- Financial ratio analysis
- Side-by-side comparisons of up to three companies
- Annual and quarterly reporting periods
- Interactive `help`, `tools`, and `exit` commands

## Requirements

- Python 3.12 or later
- An OpenAI API key
- An Alpha Vantage API key

The Alpha Vantage free tier currently allows 25 requests per day and 5 requests per minute. Requests are rate-limited by the application.

## Installation

1. Clone the repository and move into the project directory:

   ```bash
   git clone <repository-url>
   cd financial-chatbot
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirment.txt
   ```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.1
MAX_TOKENS=2000
```

Get an Alpha Vantage API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key). Keep `.env` private and do not commit API keys to GitHub.

## Usage

Start the chatbot from the project root:

```bash
python main.py
```

Example questions:

- `What was Apple's revenue last quarter?`
- `Show me Microsoft's balance sheet`
- `Compare AAPL, MSFT, and GOOGL`
- `Calculate financial ratios for Tesla`
- `What is Amazon's current stock price?`

Available commands:

| Command | Description |
| --- | --- |
| `help` | Show usage guidance |
| `tools` | List available financial analysis tools |
| `exit` | Close the chatbot |

## Project Structure

```text
.
├── main.py
├── requirment.txt
├── src/
│   ├── agent/       # LangChain chatbot agent
│   ├── config/      # Environment-based settings
│   ├── tools/       # Alpha Vantage financial tools
│   └── utils/       # Shared utilities
└── tests/           # Test suite
```

## Testing

Run the test suite with:

```bash
python -m pytest
```

## Disclaimer

This project is for educational and informational purposes only. It does not provide financial advice, investment recommendations, or a guarantee that market data is complete or current. Always verify information with reliable sources and consult a qualified financial professional before making investment decisions.

## License

No license has been specified for this repository yet.