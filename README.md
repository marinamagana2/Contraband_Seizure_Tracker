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

## 🚀 How to Run This Dashboard

> You don’t need anything fancy to try this — just Python and a few packages.

### 1. Clone or download this repo
Click the green **Code** button and choose **Download ZIP**, or run:

```bash
git clone https://github.com/yourusername/Contraband_Seizure_Tracker.git
cd Contraband_Seizure_Tracker
```

### 2. Set up your environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

### 4. Run the app!

```bash
python app.py
```

Once it’s running, open your browser and go to:
```
http://127.0.0.1:8050
```

You'll see an interactive dashboard where you can:
- Explore drug and weapon seizures
- Switch between years using a slider
- Compare regions
- See both drug and weapon data on the map at the same time

---

💡 *No accounts, no uploading, no fuss. Just run it locally and explore!*



## 📁 What’s inside

| File | What it does |
| --- | --- |
| `app.py` | Runs the whole dashboard |
| `cbp_drug_seizures_*.csv` | Drug seizure data by fiscal year |
| `cbp_weapons_seizures_*.csv` | Weapons seizure data by fiscal year |
| `requirements.txt` | Python packages used in this project |

---

## 🌱 What I learned

- How to merge and clean messy real-world datasets  
- How to use Plotly’s `scatter_mapbox()` for spatial data  
- How to build Dash apps with tabs, sliders, and filters  
- How to design a visual that’s both clean and interactive  

---

## 🔮 Future ideas

What I might add later:

- 📊 A side-by-side chart view for trends over time  
- ⏳ Timeline animation of seizures by year  
- 🧠 Hover popups with detailed stats on each location  
- ☁️ Deploy the whole thing online (Render, Heroku, etc.)  

---

## 🧰 Tech used

- Dash  
- Plotly Express  
- Pandas  
- Python 3.10+

