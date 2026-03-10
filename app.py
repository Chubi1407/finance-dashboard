import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from data import (
    get_stock_data,
    calculate_daily_returns,
    calculate_cumulative_returns,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
)

# ── Page config ──
st.set_page_config(
    page_title="Portfolio Analytics Dashboard",
    page_icon="📈",
    layout="wide",
)

# ── Header ──
st.title("📈 Portfolio Analytics Dashboard")
st.markdown("Real-time portfolio performance and risk analysis.")
st.divider()

# ── Sidebar inputs ──
st.sidebar.header("Portfolio Settings")

tickers_input = st.sidebar.text_input(
    "Stock Tickers (comma separated)",
    value="AAPL, MSFT, GOOGL",
    help="Enter valid stock tickers e.g. AAPL, TSLA, AMZN"
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=date.today() - timedelta(days=365),
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today(),
)

run = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

# ── Main content ──
if run:
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if len(tickers) == 0:
        st.error("Please enter at least one ticker.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Fetching market data..."):
            prices = get_stock_data(tickers, str(start_date), str(end_date))
            daily_returns = calculate_daily_returns(prices)
            cumulative_returns = calculate_cumulative_returns(daily_returns)
            sharpe = calculate_sharpe_ratio(daily_returns)
            max_dd = calculate_max_drawdown(cumulative_returns)

        # ── Metrics row ──
        st.subheader("Key Metrics")
        cols = st.columns(len(tickers))
        for i, ticker in enumerate(tickers):
            if ticker in sharpe.index:
                with cols[i]:
                    st.metric(
                        label=f"{ticker} Sharpe Ratio",
                        value=sharpe[ticker],
                        help="Above 1.0 is good. Measures return per unit of risk."
                    )
                    st.metric(
                        label=f"{ticker} Max Drawdown",
                        value=f"{round(max_dd[ticker] * 100, 2)}%",
                        help="Worst peak-to-trough loss over the period."
                    )

        st.divider()

        # ── Cumulative returns chart ──
        st.subheader("Cumulative Returns")
        st.caption("Shows how $1 invested on the start date would have grown.")
        fig1 = px.line(
            cumulative_returns,
            labels={"value": "Growth of $1", "Date": "Date", "variable": "Ticker"},
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig1.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="#FAFAFA",
            legend_title="Ticker",
            hovermode="x unified",
        )
        st.plotly_chart(fig1, use_container_width=True)

        # ── Stock price chart ──
        st.subheader("Stock Price History")
        fig2 = px.line(
            prices,
            labels={"value": "Price (USD)", "Date": "Date", "variable": "Ticker"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig2.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="#FAFAFA",
            hovermode="x unified",
        )
        st.plotly_chart(fig2, use_container_width=True)

        # ── Portfolio allocation pie chart ──
        st.subheader("Equal-Weight Portfolio Allocation")
        allocation = {ticker: 100 / len(tickers) for ticker in tickers}
        fig3 = px.pie(
            names=list(allocation.keys()),
            values=list(allocation.values()),
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig3.update_layout(
            paper_bgcolor="#0E1117",
            font_color="#FAFAFA",
        )
        st.plotly_chart(fig3, use_container_width=True)

        # ── Raw data toggle ──
        with st.expander("View Raw Price Data"):
            st.dataframe(prices.style.format("${:.2f}"), use_container_width=True)

else:
    st.info("👈 Enter your tickers in the sidebar and click **Run Analysis** to get started.")