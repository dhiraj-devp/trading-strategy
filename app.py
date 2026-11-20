import streamlit as st
import pandas as pd
from datetime import datetime
from scanner_rules import Candle, scan_setups, eligible

st.set_page_config(page_title="NSE F&O Scanner", page_icon="📈", layout="wide")
st.title("📈 NSE F&O Intraday Scanner")
st.caption("Android-friendly dashboard • 5-minute candle rule tester • Alerts only")

st.warning(
    "ବର୍ତ୍ତମାନ ଏହା deploy-ready dashboard/rule tester। ସମ୍ପୂର୍ଣ୍ଣ automatic live scanner ନୁହେଁ: "
    "NSE breadth, OI Spurts, sector movers ଓ gainers/losers ପାଇଁ verified data feed ଏପର୍ଯ୍ୟନ୍ତ ଯୋଡ଼ାଯାଇନାହିଁ।"
)

with st.sidebar:
    st.header("Market Breadth")
    advances = st.number_input("Nifty 50 + F&O Advances", min_value=0, value=0, step=1)
    declines = st.number_input("Nifty 50 + F&O Declines", min_value=0, value=0, step=1)
    if advances > declines:
        direction = "LONG"
        st.success("Bias: UPSIDE / LONG")
    elif declines > advances:
        direction = "SHORT"
        st.error("Bias: DOWNSIDE / SHORT")
    else:
        direction = "NO TRADE"
        st.warning("Equal breadth: no trade")
    st.caption("Starter version ରେ breadth manual input ଅଟେ।")

tab1, tab2, tab3 = st.tabs(["Dashboard", "Setup Rule Tester", "Stock Filter"])

with tab1:
    a,b,c = st.columns(3)
    a.metric("Market Bias", direction)
    b.metric("Advances", f"{advances:,}")
    c.metric("Declines", f"{declines:,}")
    st.subheader("Live Alerts")
    st.info("Live alert ଏଠାରେ ଦେଖାଯିବ ଯେତେବେଳେ candle feed integration ହେବ। ଏହି version ରେ sample data ରୁ alert test କରିପାରିବେ।")
    st.markdown("""
**ନିୟମ**
- Stock selection window: 9:30 AM ପର୍ଯ୍ୟନ୍ତ
- F&O stocks ମାତ୍ର
- Daily move 5% ଠାରୁ ଅଧିକ ହେଲେ ignore
- 5-minute completed candles
- Setup 3 cutoff: 11:00 AM
- ଏହି app order place କରେନାହିଁ
""")

with tab2:
    st.subheader("5-minute candles ଦେଇ Setup test କରନ୍ତୁ")
    st.caption("ଆଜିର candle ଗୁଡ଼ିକୁ oldest-first କ୍ରମରେ ଦିଅନ୍ତୁ। କେବଳ ସମ୍ପୂର୍ଣ୍ଣ candle ବ୍ୟବହାର କରନ୍ତୁ।")
    dir_test = st.selectbox("Direction", ["LONG", "SHORT"])
    pdh = st.number_input("Previous Day High (PDH)", min_value=0.0, value=100.0, format="%.2f")
    pdl = st.number_input("Previous Day Low (PDL)", min_value=0.0, value=90.0, format="%.2f")
    example = "09:15,100,102,99,101,1000\n09:20,101,103,100,102,800\n09:25,102,104,101,103,700\n09:30,103,104,101,102,500"
    raw = st.text_area("Format: time,open,high,low,close,volume", value=example, height=170)
    if st.button("Scan Setup Rules", type="primary", use_container_width=True):
        try:
            rows=[]
            today=datetime.now().date()
            for line in raw.strip().splitlines():
                p=[x.strip() for x in line.split(",")]
                if len(p) != 6:
                    raise ValueError("ପ୍ରତ୍ୟେକ row ରେ 6ଟି field ଦିଅନ୍ତୁ।")
                ts=datetime.combine(today, datetime.strptime(p[0], "%H:%M").time())
                rows.append(Candle(ts, *[float(v) for v in p[1:]]))
            rows.sort(key=lambda x:x.ts)
            alerts=scan_setups(rows, dir_test, pdh, pdl)
            if alerts:
                st.success(f"{len(alerts)}ଟି Setup match ହେଲା")
                st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
            else:
                st.warning("ଏହି candles ରେ କୌଣସି Setup match ହେଲା ନାହିଁ।")
        except Exception as e:
            st.error(f"Input error: {e}")

with tab3:
    st.subheader("Candidate stock filter")
    uploaded=st.file_uploader("F&O candidate CSV upload କରନ୍ତୁ", type=["csv"])
    if uploaded:
        df=pd.read_csv(uploaded)
    else:
        df=pd.DataFrame(columns=["symbol","sector","change_pct","previous_day_high","previous_day_low"])
        st.caption("CSV columns: symbol, sector, change_pct, previous_day_high, previous_day_low")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        if "change_pct" in df.columns:
            df["eligible"] = df["change_pct"].apply(lambda x: eligible(float(x), direction, advances, declines))
            st.subheader("Current eligible list")
            st.dataframe(df[df["eligible"]], use_container_width=True, hide_index=True)

st.divider()
st.caption("Educational scanner only. Confirm data freshness, broker margin and exchange rules. No profit guarantee.")
