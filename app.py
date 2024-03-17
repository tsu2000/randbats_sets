import streamlit as st
import pandas as pd
import requests
import io

from PIL import Image
from streamlit_extras.badges import badge

# Get random battle data from API
@st.cache_resource
def get_randbats_data():
    # Obtaining up-to-date data for application
    url = 'https://pkmn.github.io/randbats/data/gen9randombattle.json'
    data = requests.get(url).json()
    
    return data


def main():
    col1, col2, col3 = st.columns([0.05, 0.265, 0.035])
    
    with col1:
        url = 'https://github.com/tsu2000/randbats_sets/raw/main/images/showdown.png'
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, output_format = 'png')

    with col2:
        st.title('PSD Random Battle Sets')

    with col3:
        badge(type = 'github', name = 'tsu2000/randbats_sets', url = 'https://github.com/tsu2000/randbats_sets')

    st.markdown('### View all sets in Pokémon Showdown Random Battles')

    # Get data
    data = get_randbats_data()

    st.markdown(f"This web app allows users to see the exact sets of Pokémon used in the Gen 9 random battle format. There are **{len(data.keys())}** different Pokémon in this format. All data was taken from this [automatically updating GitHub repository](https://pkmn.github.io/randbats/) containing the latest options for Pokémon Showdown’s standard Random Battle formats.")

    name = st.selectbox("Start typing the name of a Pokémon to view its available sets in Gen 9 Random Battles:", data.keys())

    st.markdown(f'### {name}')

    roles = data[name]['roles']

    for r in roles:
        st.markdown(f'Set: **{r}**')

        # Parse and transform the JSON data
        transformed_data = {key: [value] for key, value in roles[r].items() if key in ['abilities', 'items', 'teraTypes', 'moves']}

        # Create DataFrame
        df = pd.DataFrame.from_dict(transformed_data, orient = 'index', columns = ['Values'])

        # Set name of index
        df.index.name = 'Categories'

        # Set row index names
        df.rename(index = {'abilities': 'Ability', 'items': 'Possible Held Items', 'teraTypes': 'Possible Tera Types', 'moves': 'Possible Moves'}, inplace = True)

        st.table(df, use_container_width = True)
    
    
if __name__ == "__main__":
    st.set_page_config(page_title = 'Random Battle Sets', page_icon = '🔎')
    main()
    
