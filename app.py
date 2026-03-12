import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from trading_bot import run_backtest 

st.set_page_config(page_title="ML Trader Analytics", layout="wide")

@st.cache_data(ttl=3600)
def get_analysis_data():
    start_date = datetime(2025, 1, 1) 
    end_date = datetime.now()
    params = {"take_profit": 1.07, "stop_loss": 0.93, "momentum_days": 1, "cash_at_risk": 1.0, "symbol": "SPY"}
    result = run_backtest(start_date, end_date, params)
    
    spy_df = yf.download("SPY", start="2025-01-01", progress=False)
    if isinstance(spy_df.columns, pd.MultiIndex):
        spy_df.columns = spy_df.columns.get_level_values(0)
    
    col = 'Adj Close' if 'Adj Close' in spy_df.columns else 'Close'
    spy_ret = ((spy_df[col].iloc[-1] - spy_df[col].iloc[0]) / spy_df[col].iloc[0]) * 100
    return result, spy_ret

st.title("ML Sentiment Trader Analytics")

with st.spinner("Generating Risk-Reward Profile..."):
    result, spy_perf = get_analysis_data()

if result:
    def extract(k):
        v = result.get(k, 0)
        return v.get('drawdown', 0) if isinstance(v, dict) else v

    bot_ret = extract('total_return') * 100
    bot_vol = extract('volatility') * 100
    sharpe = extract('sharpe')

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bot Return", f"{bot_ret:.2f}%")
    c2.metric("SPY Return", f"{spy_perf:.2f}%", delta=f"{bot_ret - spy_perf:.2f}% Alpha")
    c3.metric("Sharpe Ratio", f"{sharpe:.2f}")
    c4.metric("Max Drawdown", f"{extract('max_drawdown')*100:.2f}%")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.write("### Efficiency Gauge (Sharpe)")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = sharpe,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Strategy Efficiency"},
            gauge = {
                'axis': {'range': [None, 3]},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 1], 'color': "#3e444d"},
                    {'range': [1, 2], 'color': "#1f6feb"},
                    {'range': [2, 3], 'color': "#238636"}],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.write("### Risk vs. Return Analysis")
        plot_df = pd.DataFrame({
            "Asset": ["ML Bot", "SPY Benchmark"],
            "Return (%)": [bot_ret, spy_perf],
            "Volatility (%)": [bot_vol, 15.2], 
            "Size": [20, 20]
        })
        
        fig_scatter = px.scatter(
            plot_df, x="Volatility (%)", y="Return (%)", color="Asset",
            size="Size", text="Asset",
            color_discrete_map={"ML Bot": "#00d4ff", "SPY Benchmark": "#ff4b4b"}
        )
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(
            template="plotly_dark", 
            xaxis_title="Risk (Volatility %)",
            yaxis_title="Reward (Return %)",
            showlegend=False
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.write("### Strategy Scorecard")
    st.table(pd.DataFrame({
        "Performance Metric": ["CAGR", "Volatility", "Sharpe", "Max Drawdown", "RoMaD"],
        "Value": [f"{extract('cagr')*100:.2f}%", f"{bot_vol:.2f}%", f"{sharpe:.2f}", 
                  f"{extract('max_drawdown')*100:.2f}%", f"{result.get('romad', 0):.2f}"]
    }))

if st.button("Refresh Backtest"):
    st.cache_data.clear()
    st.rerun()