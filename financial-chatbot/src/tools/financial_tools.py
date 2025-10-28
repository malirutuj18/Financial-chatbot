"""
Financial Analysis Tools using Alpha Vantage API

Free Tier Limits:
- 25 API calls per day
- 5 calls per minute
"""

import requests
import time
from langchain.tools import tool
from typing import Dict, Any
from src.config.settings import settings

# Alpha Vantage API Configuration
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = settings.alpha_vantage_api_key

# Rate limiting tracker
class RateLimiter:
    """Simple rate limiter for API calls"""
    def __init__(self):
        self.last_call_time = 0
        self.min_interval = 12  # seconds between calls (5 per minute)
    
    def wait_if_needed(self):
        """Wait if we're calling too frequently"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_interval:
            wait_time = self.min_interval - time_since_last_call
            print(f"⏳ Rate limiting: waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
        
        self.last_call_time = time.time()

rate_limiter = RateLimiter()


def make_api_call(function: str, symbol: str, **kwargs) -> Dict[str, Any]:
    """
    Make API call to Alpha Vantage with rate limiting and error handling
    
    Args:
        function: Alpha Vantage function name
        symbol: Stock ticker symbol
        **kwargs: Additional parameters
        
    Returns:
        Dict with API response or error
    """
    rate_limiter.wait_if_needed()
    
    params = {
        'function': function,
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }
    params.update(kwargs)
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Check for API-specific errors
        if 'Error Message' in data:
            return {'error': f"Invalid ticker or API error: {data['Error Message']}"}
        
        if 'Note' in data:
            return {'error': "⚠️ API rate limit reached! Free tier: 25 calls/day. Please wait or upgrade."}
        
        if 'Information' in data:
            return {'error': f"API Info: {data['Information']}"}
        
        return data
        
    except requests.exceptions.Timeout:
        return {'error': "Request timeout. Please try again."}
    except requests.exceptions.RequestException as e:
        return {'error': f"Network error: {str(e)}"}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}


@tool
def get_income_statement(ticker: str, period: str = "annual") -> str:
    """
    Get income statement (revenue, expenses, profits) for a stock ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'IBM')
        period: 'annual' or 'quarterly'
        
    Returns:
        Formatted income statement with revenue, profit, and expense data
    """
    try:
        data = make_api_call('INCOME_STATEMENT', ticker)
        
        if 'error' in data:
            return f"❌ Error for {ticker.upper()}: {data['error']}"
        
        reports_key = 'annualReports' if period.lower() == 'annual' else 'quarterlyReports'
        
        if reports_key not in data or not data[reports_key]:
            return f"❌ No {period} income statement data for {ticker.upper()}"
        
        latest = data[reports_key][0]
        
        result = f"\n{'='*70}\n"
        result += f"📊 {ticker.upper()} Income Statement ({period.capitalize()})\n"
        result += f"Period Ending: {latest.get('fiscalDateEnding', 'N/A')}\n"
        result += f"{'='*70}\n\n"
        
        metrics = [
            ('Total Revenue', latest.get('totalRevenue', '0')),
            ('Cost of Revenue', latest.get('costOfRevenue', '0')),
            ('Gross Profit', latest.get('grossProfit', '0')),
            ('Operating Expenses', latest.get('operatingExpenses', '0')),
            ('Operating Income', latest.get('operatingIncome', '0')),
            ('Net Income', latest.get('netIncome', '0')),
            ('EBITDA', latest.get('ebitda', '0')),
            ('EPS', latest.get('reportedEPS', 'N/A')),
        ]
        
        for label, value in metrics:
            if label == 'EPS':
                result += f"{label:.<45} {value}\n"
            else:
                try:
                    val = int(float(value)) if value and value != 'None' else 0
                    result += f"{label:.<45} ${val:,}\n"
                except (ValueError, TypeError):
                    result += f"{label:.<45} N/A\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error processing {ticker.upper()}: {str(e)}"


@tool
def get_balance_sheet(ticker: str, period: str = "annual") -> str:
    """
    Get balance sheet (assets, liabilities, equity) for a stock ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'IBM')
        period: 'annual' or 'quarterly'
        
    Returns:
        Formatted balance sheet with assets, liabilities, and equity
    """
    try:
        data = make_api_call('BALANCE_SHEET', ticker)
        
        if 'error' in data:
            return f"❌ Error for {ticker.upper()}: {data['error']}"
        
        reports_key = 'annualReports' if period.lower() == 'annual' else 'quarterlyReports'
        
        if reports_key not in data or not data[reports_key]:
            return f"❌ No {period} balance sheet data for {ticker.upper()}"
        
        latest = data[reports_key][0]
        
        result = f"\n{'='*70}\n"
        result += f"💰 {ticker.upper()} Balance Sheet ({period.capitalize()})\n"
        result += f"Period Ending: {latest.get('fiscalDateEnding', 'N/A')}\n"
        result += f"{'='*70}\n\n"
        
        metrics = [
            ('Total Assets', latest.get('totalAssets', '0')),
            ('Current Assets', latest.get('totalCurrentAssets', '0')),
            ('Cash & Equivalents', latest.get('cashAndCashEquivalentsAtCarryingValue', '0')),
            ('Total Liabilities', latest.get('totalLiabilities', '0')),
            ('Current Liabilities', latest.get('totalCurrentLiabilities', '0')),
            ('Long Term Debt', latest.get('longTermDebt', '0')),
            ('Total Shareholder Equity', latest.get('totalShareholderEquity', '0')),
            ('Retained Earnings', latest.get('retainedEarnings', '0')),
        ]
        
        for label, value in metrics:
            try:
                val = int(float(value)) if value and value != 'None' else 0
                result += f"{label:.<45} ${val:,}\n"
            except (ValueError, TypeError):
                result += f"{label:.<45} N/A\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error processing {ticker.upper()}: {str(e)}"


@tool
def get_cash_flow(ticker: str, period: str = "annual") -> str:
    """
    Get cash flow statement (operating, investing, financing cash flows).
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'IBM')
        period: 'annual' or 'quarterly'
        
    Returns:
        Formatted cash flow statement
    """
    try:
        data = make_api_call('CASH_FLOW', ticker)
        
        if 'error' in data:
            return f"❌ Error for {ticker.upper()}: {data['error']}"
        
        reports_key = 'annualReports' if period.lower() == 'annual' else 'quarterlyReports'
        
        if reports_key not in data or not data[reports_key]:
            return f"❌ No {period} cash flow data for {ticker.upper()}"
        
        latest = data[reports_key][0]
        
        result = f"\n{'='*70}\n"
        result += f"💸 {ticker.upper()} Cash Flow Statement ({period.capitalize()})\n"
        result += f"Period Ending: {latest.get('fiscalDateEnding', 'N/A')}\n"
        result += f"{'='*70}\n\n"
        
        # Calculate Free Cash Flow
        try:
            ocf = float(latest.get('operatingCashflow', '0'))
            capex = float(latest.get('capitalExpenditures', '0'))
            fcf = ocf - abs(capex)
            result += f"{'Free Cash Flow (Calculated)':.<45} ${int(fcf):,}\n"
        except:
            pass
        
        metrics = [
            ('Operating Cash Flow', latest.get('operatingCashflow', '0')),
            ('Capital Expenditures', latest.get('capitalExpenditures', '0')),
            ('Cash from Investing', latest.get('cashflowFromInvestment', '0')),
            ('Cash from Financing', latest.get('cashflowFromFinancing', '0')),
            ('Dividend Payout', latest.get('dividendPayout', '0')),
            ('Net Income', latest.get('netIncome', '0')),
        ]
        
        for label, value in metrics:
            try:
                val = int(float(value)) if value and value != 'None' else 0
                result += f"{label:.<45} ${val:,}\n"
            except (ValueError, TypeError):
                result += f"{label:.<45} N/A\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error processing {ticker.upper()}: {str(e)}"


@tool
def get_stock_info(ticker: str) -> str:
    """
    Get comprehensive company information: price, market cap, ratios, and more.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'IBM')
        
    Returns:
        Detailed company overview with current price and key metrics
    """
    try:
        overview = make_api_call('OVERVIEW', ticker)
        
        if 'error' in overview:
            return f"❌ Error for {ticker.upper()}: {overview['error']}"
        
        if not overview or 'Symbol' not in overview:
            return f"❌ No data found for {ticker.upper()}. Check ticker symbol."
        
        # Get current quote
        quote = make_api_call('GLOBAL_QUOTE', ticker)
        current_price = 'N/A'
        change = 'N/A'
        
        if 'Global Quote' in quote and quote['Global Quote']:
            gq = quote['Global Quote']
            current_price = gq.get('05. price', 'N/A')
            change = gq.get('09. change', 'N/A')
            change_pct = gq.get('10. change percent', 'N/A')
        
        result = f"\n{'='*70}\n"
        result += f"🏢 {ticker.upper()} - {overview.get('Name', 'N/A')}\n"
        result += f"{'='*70}\n\n"
        
        result += f"📍 Company Info:\n"
        result += f"  Sector: {overview.get('Sector', 'N/A')}\n"
        result += f"  Industry: {overview.get('Industry', 'N/A')}\n"
        result += f"  Country: {overview.get('Country', 'N/A')}\n"
        result += f"  Exchange: {overview.get('Exchange', 'N/A')}\n\n"
        
        result += f"💵 Market Data:\n"
        result += f"  Current Price: ${current_price}\n"
        result += f"  Change: {change} ({change_pct})\n" if change != 'N/A' else ""
        
        try:
            mc = int(overview.get('MarketCapitalization', 0))
            result += f"  Market Cap: ${mc:,}\n"
        except:
            result += f"  Market Cap: {overview.get('MarketCapitalization', 'N/A')}\n"
        
        result += f"  52W High: ${overview.get('52WeekHigh', 'N/A')}\n"
        result += f"  52W Low: ${overview.get('52WeekLow', 'N/A')}\n\n"
        
        result += f"📈 Valuation:\n"
        result += f"  P/E Ratio: {overview.get('PERatio', 'N/A')}\n"
        result += f"  PEG Ratio: {overview.get('PEGRatio', 'N/A')}\n"
        result += f"  Price/Book: {overview.get('PriceToBookRatio', 'N/A')}\n"
        result += f"  Price/Sales: {overview.get('PriceToSalesRatioTTM', 'N/A')}\n\n"
        
        result += f"💡 Profitability:\n"
        result += f"  Profit Margin: {overview.get('ProfitMargin', 'N/A')}\n"
        result += f"  ROE: {overview.get('ReturnOnEquityTTM', 'N/A')}\n"
        result += f"  ROA: {overview.get('ReturnOnAssetsTTM', 'N/A')}\n\n"
        
        result += f"💰 Dividend:\n"
        result += f"  Dividend/Share: ${overview.get('DividendPerShare', 'N/A')}\n"
        result += f"  Dividend Yield: {overview.get('DividendYield', 'N/A')}\n"
        result += f"  Ex-Dividend Date: {overview.get('ExDividendDate', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error processing {ticker.upper()}: {str(e)}"


@tool
def get_financial_ratios(ticker: str) -> str:
    """
    Calculate key financial ratios: valuation, profitability, liquidity, leverage.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'IBM')
        
    Returns:
        Comprehensive financial ratios analysis
    """
    try:
        overview = make_api_call('OVERVIEW', ticker)
        
        if 'error' in overview:
            return f"❌ Error for {ticker.upper()}: {overview['error']}"
        
        if not overview or 'Symbol' not in overview:
            return f"❌ No ratio data for {ticker.upper()}"
        
        result = f"\n{'='*70}\n"
        result += f"📊 {ticker.upper()} Financial Ratios Analysis\n"
        result += f"{'='*70}\n\n"
        
        result += f"💎 Valuation Ratios:\n"
        result += f"  P/E Ratio (TTM): {overview.get('PERatio', 'N/A')}\n"
        result += f"  Forward P/E: {overview.get('ForwardPE', 'N/A')}\n"
        result += f"  PEG Ratio: {overview.get('PEGRatio', 'N/A')}\n"
        result += f"  Price/Book: {overview.get('PriceToBookRatio', 'N/A')}\n"
        result += f"  Price/Sales: {overview.get('PriceToSalesRatioTTM', 'N/A')}\n"
        result += f"  EV/Revenue: {overview.get('EVToRevenue', 'N/A')}\n"
        result += f"  EV/EBITDA: {overview.get('EVToEBITDA', 'N/A')}\n\n"
        
        result += f"💰 Profitability Ratios:\n"
        result += f"  Profit Margin: {overview.get('ProfitMargin', 'N/A')}\n"
        result += f"  Operating Margin: {overview.get('OperatingMarginTTM', 'N/A')}\n"
        result += f"  Return on Equity (ROE): {overview.get('ReturnOnEquityTTM', 'N/A')}\n"
        result += f"  Return on Assets (ROA): {overview.get('ReturnOnAssetsTTM', 'N/A')}\n\n"
        
        result += f"💧 Liquidity Ratios:\n"
        result += f"  Current Ratio: {overview.get('CurrentRatio', 'N/A')}\n"
        result += f"  Quick Ratio: {overview.get('QuickRatio', 'N/A')}\n\n"
        
        result += f"⚖️ Leverage Ratios:\n"
        result += f"  Debt/Equity: {overview.get('DebtToEquity', 'N/A')}\n\n"
        
        result += f"📈 Growth & Efficiency:\n"
        result += f"  Revenue Growth (YoY): {overview.get('QuarterlyRevenueGrowthYOY', 'N/A')}\n"
        result += f"  Earnings Growth (YoY): {overview.get('QuarterlyEarningsGrowthYOY', 'N/A')}\n"
        result += f"  Asset Turnover: {overview.get('AssetTurnover', 'N/A')}\n\n"
        
        result += f"⚠️ Risk:\n"
        result += f"  Beta: {overview.get('Beta', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error calculating ratios for {ticker.upper()}: {str(e)}"


@tool
def compare_companies(tickers: str) -> str:
    """
    Compare key metrics across multiple companies side-by-side.
    
    Args:
        tickers: Comma-separated ticker symbols (e.g., 'AAPL,MSFT,GOOGL')
        
    Returns:
        Comparison table with key metrics
        
    Note: Limited to 3 companies max due to free tier limits (25 calls/day)
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]
        
        if len(ticker_list) > 3:
            return "⚠️ Free tier limit: Max 3 companies for comparison (25 API calls/day limit)"
        
        comparison_data = []
        
        print(f"\n🔄 Comparing {len(ticker_list)} companies (this may take ~40 seconds)...\n")
        
        for ticker in ticker_list:
            try:
                overview = make_api_call('OVERVIEW', ticker)
                
                if 'error' in overview or 'Symbol' not in overview:
                    comparison_data.append({
                        'Ticker': ticker,
                        'Company': 'Error',
                        'Sector': 'N/A',
                        'Market Cap': 'N/A',
                        'P/E': 'N/A',
                        'ROE': 'N/A',
                    })
                    continue
                
                try:
                    mc = int(overview.get('MarketCapitalization', 0))
                    market_cap = f"${mc/1e9:.2f}B" if mc > 0 else 'N/A'
                except:
                    market_cap = 'N/A'
                
                comparison_data.append({
                    'Ticker': ticker,
                    'Company': overview.get('Name', 'N/A')[:30],
                    'Sector': overview.get('Sector', 'N/A')[:20],
                    'Market Cap': market_cap,
                    'P/E': overview.get('PERatio', 'N/A'),
                    'ROE': overview.get('ReturnOnEquityTTM', 'N/A'),
                })
                
            except Exception as e:
                comparison_data.append({
                    'Ticker': ticker,
                    'Company': f'Error: {str(e)[:15]}',
                    'Sector': 'N/A',
                    'Market Cap': 'N/A',
                    'P/E': 'N/A',
                    'ROE': 'N/A',
                })
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        
        result = f"\n{'='*85}\n"
        result += "🔍 Company Comparison\n"
        result += f"{'='*85}\n\n"
        result += df.to_string(index=False)
        result += "\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error comparing companies: {str(e)}"
