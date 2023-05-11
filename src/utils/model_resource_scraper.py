import os
import pathlib
import re
import sys


from bs4 import BeautifulSoup

models_url = "https://www.models-resource.com"

game_urls = []

def generate_url(game_url): # Old Function: Can Delete Eventually
    return models_url + "/" + game_url

if __name__ == "__main__":
    # SAMPLE USAGEc
    print("--------------------\nstarting program --- \"models_scraper.py\"\n--------------------")
    
    try: os.mkdir('./game_htmls/')
    except: print(f'directory \'./game_htmls\' already exists. skipping creation.')
    
    try: os.mkdir('./models/')
    except: print(f'directory \'.models/\' already exists. skipping creation.')

    for game_url in game_urls:
        # download html file for game
        game_name = game_url.split('/')[-1] # get just the game name for the output file for wget
        complete_url = generate_url(game_url)
        if os.path.exists(f'./game_htmls/{game_name}.html') is False: # download file if it doesn't exist
            os.system(f'wget -O ./game_htmls/{game_name}.html {complete_url}')
        pass

        try:
            os.mkdir(f'./models/{game_name}')
        except:
            print(f'directory \'./models/{game_name}\' already exists. skipping creation.')

    for game_html in os.listdir(f'./game_htmls/'):
        full_html_path = f'./game_htmls/{game_html}'
        model_list_list = [] # list containing lists of all models per section  

        with open(full_html_path, 'r') as game_html_content:
            soup = BeautifulSoup(game_html_content, 'html.parser')
            # print(f"soup:\n{soup.find_all('div', class_='updatesheeticons')}") # DEBUG
            model_list_list = soup.find_all('div', class_="updatesheeticons")
        
        for model_list in model_list_list:
            for a in model_list.find_all('a'):
                model_tag = a["href"][-6:-1]
                # print(a['href']) # DEBUG: print each model link
                complete_model_url = f'{models_url}{a["href"]}'
                if f'{model_tag}.zip' in os.listdir(f'./models/{game_name}') or f'{model_tag}' in os.listdir(f'./models/{game_name}'): # make sure the models don't already exist
                    print(f"model file for model {game_name}/{model_tag} already exists. skipping.")
                    pass
                else:
                    print(f"Downloading: model from {models_url}/download/{model_tag}...")
                    os.system(f'wget -O ./models/{game_name}/{model_tag}.zip {models_url}/download/{model_tag}/')
            pass
        pass

    for game_url in game_urls:
        game_name = game_url.split('/')[-1] # get just the game name so that we can get each model

        pass
    sys.exit()