import pytest
from datetime import datetime, timedelta
from ....src.domain.entities.stock import Stock
from ....src.domain.value_objects.price import Price
from ....src.domain.aggregates.stock_analysis import StockAnalysis

@pytest.fixture
def sample_stock_data():
    prices = []
    start_date = datetime(2023, 1, 1)
    price = 100
    for i in range(100):
        price += (i % 5 - 2) # some fluctuation
        prices.append(
            Price(
                timestamp=start_date + timedelta(days=i),
                open=price,
                high=price + 2,
                low=price - 2,
                close=price + 1,
                volume=1000 + i * 10
            )
        )
    return Stock(symbol="TEST", name="Test Stock", prices=prices)

def test_stock_analysis_creation(sample_stock_data):
    analysis = StockAnalysis(sample_stock_data)
    assert analysis.stock.symbol == "TEST"

def test_stock_analysis_analyze_run(sample_stock_data):
    analysis = StockAnalysis(sample_stock_data)
    result = analysis.analyze(timeframe='medium')
    assert result is not None
    assert result.trend in ['bullish', 'bearish', 'neutral']
    assert isinstance(result.strength, float)
    assert isinstance(result.recommendation, str)

def test_identify_support_resistance(sample_stock_data):
    analysis = StockAnalysis(sample_stock_data)
    prices = [p.close for p in sample_stock_data.prices]
    support = analysis._identify_support_levels(prices)
    resistance = analysis._identify_resistance_levels(prices)
    
    # With this simple data, we might not get many levels, but we can check the type
    assert isinstance(support, list)
    assert isinstance(resistance, list)
