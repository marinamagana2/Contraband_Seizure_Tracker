# 🚨 Contraband Seizure Tracker

This is a data dashboard I built to explore drug and weapon seizures along U.S. borders. It pulls from real CBP data (2019–2025) and lets you track where and when these seizures happened.

It’s interactive, visual, and helps highlight patterns over time—whether you’re curious about border trends or just want to see how data can tell a story.

---

## 🌎 What it does

The dashboard lets you:
- View **drug and weapon seizures** on an interactive U.S. map
- Filter by **year** using a slider (2019–2025)
- Compare different **regions** based on seizure quantity
- Display **both drugs and weapons** in the same visualization

Built with [Dash](https://dash.plotly.com/) + [Plotly Express](https://plotly.com/python/plotly-express/) — no login or uploading required. Just run it locally and explore.

## 🛠️ How to run it
Clone this repo
You can either:

Click the green “Code” button and “Download ZIP”, then unzip it
or

Use Git:
git clone https://github.com/marinamagana2/Contraband_Seizure_Tracker.git
cd Contraband_Seizure_Tracker

Install dependencies
Make sure you have Python 3.10+ installed. Then run:
pip install -r requirements.txt
Or install manually:
pip install dash pandas plotly

Launch it
Run this in your terminal:
python app.py
Then open your browser and go to:
http://127.0.0.1:8050
