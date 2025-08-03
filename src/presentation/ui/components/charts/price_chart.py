import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class PriceChart:
    def __init__(self, stock_data, indicators_data):
        self.stock_data = stock_data
        self.indicators_data = indicators_data
        self.df = self._prepare_dataframe()

    def _prepare_dataframe(self):
        if not self.stock_data or not self.stock_data.prices:
            return pd.DataFrame()
        
        price_list = [
            {
                "time": p.timestamp,
                "open": p.open,
                "high": p.high,
                "low": p.low,
                "close": p.close,
                "volume": p.volume
            }
            for p in self.stock_data.prices
        ]
        df = pd.DataFrame(price_list)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        return df

    def plot(self, dragmode='pan', selected_indicators=None):
        if self.df.empty:
            return self._create_blank_chart()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3]
        )

        # Candlestick Chart
        fig.add_trace(go.Candlestick(
            x=self.df.index,
            open=self.df['open'],
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            name='Price'
        ), row=1, col=1)

        # Volume Chart
        fig.add_trace(go.Bar(
            x=self.df.index,
            y=self.df['volume'],
            name='Volume',
            marker_color='rgba(173, 216, 230, 0.5)'
        ), row=2, col=1)
        
        # Add selected indicators
        if selected_indicators:
            for indicator in selected_indicators:
                if indicator in self.indicators_data:
                    for trace in self.indicators_data[indicator]:
                        fig.add_trace(go.Scatter(
                            x=self.df.index,
                            y=trace['values'],
                            mode='lines',
                            name=trace['name'],
                            line=dict(color=trace.get('color', 'white'), width=1)
                        ), row=1, col=1)

        fig.update_layout(
            title_text=f"{self.stock_data.name} ({self.stock_data.symbol})",
            template="plotly_dark",
            dragmode=dragmode,
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=50, b=50, t=50, pad=4)
        )
        
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        return fig

    def _create_blank_chart(self):
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    text="Enter a stock symbol to begin analysis",
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20, color="gray")
                )
            ]
        )
        return fig
