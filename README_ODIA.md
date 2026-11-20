# Android Mobile ପାଇଁ NSE F&O Scanner — Free Deployment Starter

## ଏହା କ'ଣ?
ଏହା Streamlit dashboard ଅଟେ। Android Chrome ରେ ଖୋଲିପାରିବ। Free hosting ପାଇଁ Streamlit Community Cloud ବ୍ୟବହାର କରିବାର deployment files ରହିଛି। ଏହା ଏପର୍ଯ୍ୟନ୍ତ fully automatic live scanner ନୁହେଁ।

## Android ରୁ deploy କରିବା ପାଇଁ
ସବୁଠାରୁ ସହଜ ପଥ:
1. ZIP extract କରନ୍ତୁ।
2. GitHub account ଖୋଲନ୍ତୁ ଏବଂ ନୂଆ **private repository** ସୃଷ୍ଟି କରନ୍ତୁ।
3. ଏହି project ର files repository ରେ upload କରନ୍ତୁ। `.streamlit/secrets.toml` କିମ୍ବା API tokens upload କରନ୍ତୁ ନାହିଁ।
4. https://share.streamlit.io/ ଖୋଲି GitHub connect କରନ୍ତୁ।
5. Repository ଓ `app.py` ବାଛି Deploy କରନ୍ତୁ।
6. Deploy ହେଲେ Streamlit URL Android Chrome ରେ ଖୋଲନ୍ତୁ; Chrome menu → “Add to Home screen” କଲେ app ପରି ଖୋଲିବ।

## Free hosting ର ସୀମା
Free hosting sleep/idle ହୋଇପାରେ, uptime ଗ୍ୟାରେଣ୍ଟି ନୁହେଁ। ସେହିପାଇଁ ଏହା 24×7 high-reliability live trading scanner ପାଇଁ ନିଶ୍ଚିତ ନୁହେଁ।

## ଏବେ କାମ କରୁଥିବା ଅଂଶ
- Mobile-friendly dashboard
- Advances/Declines manual input ରୁ direction
- Setup 1/2/3 rule tester
- 5% ରୁ ଅଧିକ daily movement filter
- Candidate CSV upload/filter
- Dashboard-only alerts display

## ଏପର୍ଯ୍ୟନ୍ତ ଯୋଡ଼ାଯାଇନଥିବା ଅଂଶ
- Groww API authentication ଓ automatic live quote/candle polling
- Nifty 50 + F&O live advances/declines feed
- NSE OI Spurts top 5 feed
- 13ଟି sector ମଧ୍ୟରୁ top 2 ଓ ପ୍ରତି sector ର top 5 F&O stocks
- NSE top gainers/losers top 5 feed
- Live candle stream/cache ଓ automatic alert refresh
- Official/licensed data-source verification

Groww API access/token ଓ NSE screener feeds ର ଉପଲବ୍ଧତା ଅଲଗାଭାବେ ସେଟ୍ କରିବାକୁ ପଡ଼ିବ। Public NSE website ର page scrape କରିବାକୁ stable, approved live API ଭାବରେ ଧରନ୍ତୁ ନାହିଁ।

## Setup 1 logic
- ପ୍ରଥମ 3ଟି 5-minute candle ମଧ୍ୟରେ
- LONG/upside direction ରେ RED candle
- SHORT/downside direction ରେ GREEN candle
- ସେହି candle ର Open ଓ Close ଉଭୟ ପୂର୍ବ candle ର Low ଓ High ମଧ୍ୟରେ

## Local test
Python 3.11+ ରେ:
`pip install -r requirements.txt`
`streamlit run app.py`

ଏହା order place କରେନାହିଁ। ପ୍ରଥମେ paper trading ରେ test କରନ୍ତୁ।
