import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load datasets
drug_files = [
    "cbp_drug_seizures_fy19_22.csv",
    "cbp_drug_seizures_fy20_23.csv",
    "cbp_drug_seizures_fy21_24.csv",
    "cbp_drug_seizures_fy22_25.csv"
]
weapon_files = [
    "cbp_weapons_seizures_fy19_22.csv",
    "cbp_weapons_seizures_fy20_23.csv",
    "cbp_weapons_seizures_fy21_24.csv",
    "cbp_weapons_seizures_fy22_25.csv"
]

df_drugs = pd.concat([pd.read_csv(f) for f in drug_files], ignore_index=True)
df_weapons = pd.concat([pd.read_csv(f) for f in weapon_files], ignore_index=True)

# Standardize columns
df_drugs['Area of Responsibility'] = df_drugs['Area of Responsibility'].str.title()
df_weapons['Area of Responsibility'] = df_weapons['Area of Responsibility'].str.title()
df_drugs['FY'] = pd.to_numeric(df_drugs['FY'], errors='coerce')
df_weapons['Fiscal Year'] = pd.to_numeric(df_weapons['Fiscal Year'], errors='coerce')

# Coordinates
aor_coords = {
    'San Diego Field Office': (32.7157, -117.1611),
    'Laredo Field Office': (27.5306, -99.4803),
    'El Paso Field Office': (31.7619, -106.4850),
    'Tucson Field Office': (32.2226, -110.9747),
    'New Orleans Field Office': (29.9511, -90.0715),
    'Miami Field Office': (25.7617, -80.1918),
    'Detroit Field Office': (42.3314, -83.0458),
    'Chicago Field Office': (41.8781, -87.6298),
    'Buffalo Field Office': (42.8864, -78.8784),
    'Seattle Field Office': (47.6062, -122.3321),
    'Boston Field Office': (42.3601, -71.0589),
    'New York Field Office': (40.7128, -74.0060),
    'Houston Field Office': (29.7604, -95.3698),
    'Atlanta Field Office': (33.7490, -84.3880),
    'Los Angeles Field Office': (34.0522, -118.2437),
    'Baltimore Field Office': (39.2904, -76.6122),
    'San Francisco Field Office': (37.7749, -122.4194)
}

df_drugs['lat'] = df_drugs['Area of Responsibility'].map(lambda x: aor_coords.get(x, (None, None))[0])
df_drugs['lon'] = df_drugs['Area of Responsibility'].map(lambda x: aor_coords.get(x, (None, None))[1])
df_weapons['lat'] = df_weapons['Area of Responsibility'].map(lambda x: aor_coords.get(x, (None, None))[0])
df_weapons['lon'] = df_weapons['Area of Responsibility'].map(lambda x: aor_coords.get(x, (None, None))[1])

# App
app = dash.Dash(__name__)
app.title = "CBP Contraband Seizure Tracker"

app.layout = html.Div([
    html.H1("CBP Contraband Seizure Tracker"),
    html.P("Explore trends in drug and weapons seizures across U.S. borders"),

    dcc.Tabs([
        dcc.Tab(label="Drug Seizures 🍎", children=[
            dcc.Slider(
                id='drug-year-slider',
                min=int(df_drugs['FY'].min()),
                max=int(df_drugs['FY'].max()),
                step=1,
                value=int(df_drugs['FY'].max()),
                marks={int(y): str(int(y)) for y in sorted(df_drugs['FY'].dropna().unique())}
            ),
            dcc.Graph(id='drug-bar'),
            dcc.Graph(id='drug-trend')
        ]),
        dcc.Tab(label="Weapons Seizures 🔫", children=[
            dcc.Slider(
                id='weapon-year-slider',
                min=int(df_weapons['Fiscal Year'].min()),
                max=int(df_weapons['Fiscal Year'].max()),
                step=1,
                value=int(df_weapons['Fiscal Year'].max()),
                marks={int(y): str(int(y)) for y in sorted(df_weapons['Fiscal Year'].dropna().unique())}
            ),
            dcc.Graph(id='weapon-bar'),
            dcc.Graph(id='weapon-trend')
        ]),
        dcc.Tab(label="Comparison 🏛️", children=[
            dcc.Graph(id='comparison-bar')
        ]),
        dcc.Tab(label="Map 🗺️", children=[
            dcc.Slider(
                id='map-year-slider',
                min=2019,
                max=2025,
                step=1,
                value=2025,
                marks={y: str(y) for y in range(2019, 2026)}
            ),
            dcc.Graph(id='map')
        ])
    ])
])

# Callbacks

@app.callback(Output('drug-bar', 'figure'), Input('drug-year-slider', 'value'))
def drug_bar(year):
    df = df_drugs[df_drugs['FY'] == year]
    data = df.groupby('Drug Type')['Sum Qty (lbs)'].sum().reset_index()
    return px.bar(data, x='Drug Type', y='Sum Qty (lbs)', title=f"Drug Seizures in {year}")

@app.callback(Output('drug-trend', 'figure'), Input('drug-year-slider', 'value'))
def drug_trend(_):
    df = df_drugs.groupby('FY')['Sum Qty (lbs)'].sum().reset_index()
    return px.line(df, x='FY', y='Sum Qty (lbs)', markers=True, title="Drug Seizures Over Time")

@app.callback(Output('weapon-bar', 'figure'), Input('weapon-year-slider', 'value'))
def weapon_bar(year):
    df = df_weapons[df_weapons['Fiscal Year'] == year]
    data = df.groupby('Category')['Quantity Seized'].sum().reset_index()
    return px.bar(data, x='Category', y='Quantity Seized', title=f"Weapons Seized in {year}")

@app.callback(Output('weapon-trend', 'figure'), Input('weapon-year-slider', 'value'))
def weapon_trend(_):
    df = df_weapons.groupby('Fiscal Year')['Quantity Seized'].sum().reset_index()
    return px.line(df, x='Fiscal Year', y='Quantity Seized', markers=True, title="Weapons Seizures Over Time")

@app.callback(Output('comparison-bar', 'figure'), Input('drug-year-slider', 'value'))
def comparison_bar(_):
    d = df_drugs.groupby('FY')['Sum Qty (lbs)'].sum().reset_index()
    w = df_weapons.groupby('Fiscal Year')['Quantity Seized'].sum().reset_index()
    merged = pd.merge(d, w, left_on='FY', right_on='Fiscal Year', how='outer')
    merged['FY'] = merged['FY'].combine_first(merged['Fiscal Year'])
    merged = merged[['FY', 'Sum Qty (lbs)', 'Quantity Seized']].fillna(0)
    melted = merged.melt(id_vars='FY', var_name='Type', value_name='Total')
    return px.bar(melted, x='FY', y='Total', color='Type', barmode='group', title="Drugs vs Weapons Seizures")

@app.callback(Output('map', 'figure'), Input('map-year-slider', 'value'))
def update_map(year):
    drugs = df_drugs[df_drugs['FY'] == year]
    weapons = df_weapons[df_weapons['Fiscal Year'] == year]

    d = drugs.groupby(['Area of Responsibility', 'lat', 'lon'])['Sum Qty (lbs)'].sum().reset_index()
    d['Type'] = 'Drugs'
    d.rename(columns={'Sum Qty (lbs)': 'Quantity'}, inplace=True)

    w = weapons.groupby(['Area of Responsibility', 'lat', 'lon'])['Quantity Seized'].sum().reset_index()
    w['Type'] = 'Weapons'
    w.rename(columns={'Quantity Seized': 'Quantity'}, inplace=True)

    combined = pd.concat([d, w], ignore_index=True)

    return px.scatter_mapbox(
        combined, lat='lat', lon='lon', color='Type', size='Quantity',
        hover_name='Area of Responsibility', zoom=3, mapbox_style='carto-positron',
        title=f"Top Regions for Drug & Weapon Seizures in {year}"
    )

if __name__ == '__main__':
    app.run(debug=True)
