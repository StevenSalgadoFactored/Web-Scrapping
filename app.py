import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Define the URL of the webpage
url = "https://pokemondb.net/pokedex/all"

# Send an HTTP GET request and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Locate the table and extract rows
table = soup.find('table', class_='data-table', id='pokedex')
rows = table.find_all('tr')[1:]  # Exclude the header row

data_list = []

for row in rows:
    cols = row.find_all('td')
    
    # Check for the presence of the <small> element and use its content when available
    name_element = cols[1].find('a', class_='ent-name')
    small_name_element = cols[1].find('small', class_='text-muted')
    
    # Determine if it's a Mega Evolution
    is_mega_evolution = bool(small_name_element)
    
    if is_mega_evolution:
        pokemon_name = small_name_element.text.strip()
    else:
        pokemon_name = name_element.text.strip()
    
    # Extract the sprite image URL
    sprite_url = cols[0].find('img')['src']
    
    # Extract the rest of the data
    pokemon_number = pd.to_numeric(cols[0].find('span', class_='infocard-cell-data').text.strip())
    pokemon_types = [a.text.strip() for a in cols[2].find_all('a', class_='type-icon')]
    total_stats = pd.to_numeric(cols[3].text.strip())
    individual_stats = [pd.to_numeric(stat.text.strip()) for stat in cols[4:10]]
    
    data = {
        'Number': pokemon_number,
        'Name': pokemon_name,
        'Type 1': pokemon_types[0],
        'Type 2': pokemon_types[1] if len(pokemon_types) > 1 else np.nan,
        'Total Stats': total_stats,
        'HP': individual_stats[0],
        'Attack': individual_stats[1],
        'Defense': individual_stats[2],
        'Sp. Atk': individual_stats[3],
        'Sp. Def': individual_stats[4],
        'Speed': individual_stats[5],
        'Sprite URL': sprite_url,
        'Is Mega Evolution': is_mega_evolution,
    }
    data_list.append(data)

# Create a Pandas DataFrame
df = pd.DataFrame(data_list)

# Create a 'data' folder (if it doesn't exist)
import os
if not os.path.exists('data'):
    os.mkdir('data')

# Export the DataFrame as a CSV file in the 'data' folder
csv_file_path = 'data/pokemon_data.csv'
df.to_csv(csv_file_path, index=False)

# Print a message to confirm the export
print(f"Data exported to {csv_file_path}")
