"""
Test Suite for Financial Chatbot
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.financial_agent import FinancialChatbot
from src.tools.financial_tools import get_stock_info


def test_agent_initialization():
    """Test agent initialization"""
    print("\n" + "="*70)
    print("TEST 1: Agent Initialization")
    print("="*70)
    
    try:
        chatbot = FinancialChatbot()
        assert chatbot.agent is not None
        assert len(chatbot.tools) == 6
        print("✅ Agent initialized")
        print(f"✅ {len(chatbot.tools)} tools loaded")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_single_tool():
    """Test individual tool"""
    print("\n" + "="*70)
    print("TEST 2: Single Tool (get_stock_info)")
    print("="*70)
    
    try:
        print("📊 Fetching IBM stock info...")
        result = get_stock_info.invoke({"ticker": "IBM"})
        
        assert result is not None
        assert len(result) > 100
        
        print("✅ Tool executed successfully")
        print(f"\nSample output:\n{result[:400]}...\n")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_agent_query():
    """Test full agent query"""
    print("\n" + "="*70)
    print("TEST 3: Agent Query")
    print("="*70)
    
    try:
        chatbot = FinancialChatbot()
        
        query = "What is IBM's current stock price?"
        print(f"🔍 Query: {query}")
        
        response = chatbot.query(query)
        
        assert response is not None
        assert len(response) > 50
        
        print("✅ Query successful")
        print(f"\nResponse preview:\n{response[:300]}...\n")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "#"*70)
    print("#" + " "*15 + "FINANCIAL CHATBOT TEST SUITE" + " "*26 + "#")
    print("#"*70)
    print("\n⚠️  Note: Tests respect API rate limits (25 calls/day)\n")
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Single Tool Test", test_single_tool),
        ("Agent Query Test", test_agent_query),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} passed")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
