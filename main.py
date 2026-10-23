import pandas as pd
import requests

# data.
df = pd.read_csv("https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# metadata
metadata = requests.get("https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

print(metadata["columns"].keys())
print(df["year"].unique())
