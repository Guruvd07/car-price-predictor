import pandas as pd
import requests
import json

# Load and analyze the dataset
url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/cleaned_cardekho_data-Iupg6W6knXPiGSbamR56eqEOOrAoku.csv"
response = requests.get(url)

# Save the CSV file
with open('cleaned_cardekho_data.csv', 'wb') as f:
    f.write(response.content)

# Load and analyze the data
df = pd.read_csv('cleaned_cardekho_data.csv')

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

print("\nUnique values for dropdowns:")
print("Brands:", sorted(df['Model'].unique()))
print("Fuel Types:", sorted(df['Fuel Type'].unique()))
print("Transmissions:", sorted(df['Transmission'].unique()))
print("Cities:", sorted(df['City'].unique()))

# Extract year from Brand column (seems to contain year data)
print("Years:", sorted(df['Brand'].unique()))

print("\nSample data structure:")
for col in df.columns:
    print(f"{col}: {df[col].iloc[0]}")
