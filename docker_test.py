import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from application.services.analysis_service import AnalysisService
from infrastructure.external_services.yahoo_finance import YahooFinance
from infrastructure.external_services.google_gemini_service import GoogleGeminiService

async def run_test():
    logging.info("Initializing services...")
    market_data_service = YahooFinance()
    llm_service = GoogleGeminiService()
    analysis_service = AnalysisService(market_data_service, llm_service)
    
    # --- Test Case 1: Valid Symbol ---
    try:
        logging.info("--- Running Test Case 1: Valid Symbol (AAPL) ---")
        symbol_valid = "AAPL"
        result_valid = await analysis_service.analyze_stock(symbol_valid)
        
        assert result_valid is not None
        assert result_valid.symbol == symbol_valid
        assert result_valid.ai_analysis is not None
        assert "recommendation" in result_valid.ai_analysis
        
        logging.info(f"Valid Symbol Test PASSED. Recommendation for {symbol_valid}: {result_valid.ai_analysis.get('recommendation')}")
        logging.info(f"AI Summary: {result_valid.ai_analysis.get('summary')}")

    except Exception as e:
        logging.error(f"Valid Symbol Test FAILED. Error: {e}")
        sys.exit(1) # Exit with error code

    # --- Test Case 2: Invalid Symbol ---
    try:
        logging.info("\n--- Running Test Case 2: Invalid Symbol (INVALIDSTOCK) ---")
        symbol_invalid = "INVALIDSTOCK"
        await analysis_service.analyze_stock(symbol_invalid)
        
        # If this line is reached, the test fails because an exception was expected
        logging.error("Invalid Symbol Test FAILED. Expected an exception but none was raised.")
        sys.exit(1)

    except ValueError as e:
        logging.info(f"Invalid Symbol Test PASSED. Correctly caught expected error: {e}")
    except Exception as e:
        logging.error(f"Invalid Symbol Test FAILED. Caught an unexpected error type: {type(e).__name__} - {e}")
        sys.exit(1)

    logging.info("\nAll tests passed successfully!")

if __name__ == "__main__":
    import sys
    asyncio.run(run_test())
