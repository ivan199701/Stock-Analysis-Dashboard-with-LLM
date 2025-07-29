import plotly.graph_objects as go
from plotly.subplots import make_subplots
from domain.entities.stock import Stock
from domain.value_objects.analysis_result import AnalysisResult

from datetime import datetime, timedelta

class PriceChart:
    def render(self, stock_data: Stock, analysis: AnalysisResult, initial_days_visible: int, dragmode: str) -> go.Figure:
        df = stock_data._get_dataframe()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3]
        )

        # Candlestick Chart
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ), row=1, col=1)

        # --- Add Indicators if analysis is available ---
        if analysis:
            # SMA Indicator
            if 'sma' in analysis.indicators and analysis.indicators['sma']:
                fig.add_trace(go.Scatter(
                    x=df.index[-len(analysis.indicators['sma']):],
                    y=analysis.indicators['sma'],
                    mode='lines', name='SMA', line=dict(color='orange', width=1)
                ), row=1, col=1)

            # EMA Indicator
            if 'ema' in analysis.indicators and analysis.indicators['ema']:
                fig.add_trace(go.Scatter(
                    x=df.index[-len(analysis.indicators['ema']):],
                    y=analysis.indicators['ema'],
                    mode='lines', name='EMA', line=dict(color='yellow', width=1)
                ), row=1, col=1)

            # Bollinger Bands
            if 'bbands' in analysis.indicators and analysis.indicators['bbands']:
                bbands = analysis.indicators['bbands']
                fig.add_trace(go.Scatter(x=df.index[-len(bbands['upper']):], y=bbands['upper'], mode='lines', name='Upper Band', line=dict(color='gray', width=1, dash='dash')), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index[-len(bbands['lower']):], y=bbands['lower'], mode='lines', name='Lower Band', line=dict(color='gray', width=1, dash='dash'), fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)

            # Support and Resistance Levels
            for level in analysis.support_levels:
                fig.add_hline(y=level, line_dash="dot", line_color="green", annotation_text=f"Support {level:.2f}", annotation_position="bottom right", row=1, col=1)
            for level in analysis.resistance_levels:
                fig.add_hline(y=level, line_dash="dot", line_color="red", annotation_text=f"Resistance {level:.2f}", annotation_position="top right", row=1, col=1)

        # Volume Chart
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='Volume',
            marker_color='rgba(173, 216, 230, 0.5)'
        ), row=2, col=1)

        # Set initial visible range
        end_date = df.index[-1]
        start_date = end_date - timedelta(days=initial_days_visible)
        fig.update_xaxes(range=[start_date, end_date])

        fig.update_layout(
            title=f"{stock_data.name} ({stock_data.symbol})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            dragmode=dragmode
        )
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        return fig

    def render_blank(self) -> go.Figure:
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
                    font=dict(size=20)
                )
            ]
        )
        return fig
