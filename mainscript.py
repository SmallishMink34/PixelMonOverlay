import requests
import bs4 as bs
import jaro
import pandas
from pyjarowinkler import distance
import io

def get_pokemon_res(pk="pikachu"):
    #pokemon = input("Entrez le nom du pokemon : ").title()
    print("pokemon : ", pk)
    pokemon = open("pokemonlist.txt", "r")
    liste = pokemon.readlines()
    for i in range(len(liste)):
        if distance.get_jaro_distance(liste[i],pk) > 0.8:
            print("distance : ", distance.get_jaro_distance(liste[i],pk))
            print("Remplacement : ", pk, " <- ", liste[i])
            pk = liste[i]
            break
    print("pokemon after: ", pk)
    
    if pk != None and pk != "":
        site = 'https://www.pokepedia.fr/'+pk.title().replace(' ', '-').strip()
        website = requests.get(site)
        soup = bs.BeautifulSoup(website.text, 'html.parser')

        table = soup.find('table', attrs={'class':'sensibilite'})

        """class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'"""

        try:
            pktype = [i.find("img").attrs['alt'].split(" ")[2] for i in table.find_all('td', attrs = {'colspan' : False, 'style' : True})]
            resistance = [i.get_text() if i.get_text() != '' else None for i in table.find_all('td', attrs = {'colspan' : False, 'style' : False})]

            pokemon_res = dict(zip(pktype, resistance))

            #print(pokemon_res)
            #open("pokemon.txt", "w").write(website.text)
            """print('='*20)
            for i in pokemon_res.keys():
                if pokemon_res[i] != None:
                    print(bcolors.OKBLUE+i, '\t'*1 if len(i) > 6 else '\t'*2, (bcolors.OKCYAN if pokemon_res[i].split(" ")[1] == '0' else bcolors.OKGREEN) +pokemon_res[i].split(" ")[1]+bcolors.ENDC)
            print('='*30)"""
            return pokemon_res

        except AttributeError:i
            #print(bcolors.WARNING+'Pokémon non trouvé'+bcolors.ENDC)
            return 0
    else:
        return 0


def get_pokemon_res_csv(pk="Pikachu"):
    #pokemon = input("Entrez le nom du pokemon : ").title()
    print("pokemon : ", pk)
    pokemon = io.open("pokemonlist.txt", mode="r", encoding="utf-8")
    liste = pokemon.readlines()
    for i in range(len(liste)):
        if distance.get_jaro_distance(liste[i],pk) > 0.7:
            print("Remplacement : ", pk, " <- ", liste[i])
            pk = liste[i]
            break
            print("pokemon after: ", pk, jaro.jaro_metric(liste[i], pk))
    
    if pk != None and pk != "":
        """site = 'https://www.pokepedia.fr/'+pk.title().replace(' ', '-').strip()
        website = requests.get(site)
        soup = bs.BeautifulSoup(website.text, 'html.parser')

        table = soup.find('table', attrs={'class':'sensibilite'})"""

        csv_file = pandas.read_csv("pokemon.csv", encoding = "utf-8", sep = ";", index_col = "Namefr")



        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'

        try:
            value_head = ["primary_type", "secondary_type", 'speed', 'against_normal', 'against_fire', 'against_water', 'against_electric', 'against_grass', 'against_ice', 'against_fighting', 'against_poison', 'against_ground', 'against_flying', 'against_psychic', 'against_bug', 'against_rock', 'against_ghost', 'against_dragon', 'against_dark', 'against_steel', 'against_fairy']
            value_head_2 = ["primary_type", "secondary_type", 'speed', "Normal", "Feu", "Eau", "Électrik", "Plante", "Glace", "Combat", "Poison", "Sol", "Vol", "Psy", "Insecte", "Roche", "Spectre", "Dragon", "Ténèbres", "Acier", "Fée"]
            resistance = [csv_file.loc[pk.split(), value_head].values[0][i] if csv_file.loc[pk.split(), value_head].values[0][i] != 1.0 else None  for i in range(3, 21)]
            pktype = [value_head_2[i] if csv_file.loc[pk.split(), value_head].values[0][i] != 1.0 else None  for i in range(3, 21)]
            pokemon_res = dict(zip(pktype, resistance))
            """pktype = [i.find("img").attrs['alt'].split(" ")[2] for i in table.find_all('td', attrs = {'colspan' : False, 'style' : True})]
            resistance = [i.get_text() if i.get_text() != '' else None for i in table.find_all('td', attrs = {'colspan' : False, 'style' : False})]

            pokemon_res = dict(zip(pktype, resistance))"""

            #print(pokemon_res)
            #open("pokemon.txt", "w").write(website.text)
            """print('='*20)
            for i in pokemon_res.keys():
                if pokemon_res[i] != None:
                    print(bcolors.OKBLUE+i, '\t'*1 if len(i) > 6 else '\t'*2, (bcolors.OKCYAN if pokemon_res[i].split(" ")[1] == '0' else bcolors.OKGREEN) +pokemon_res[i].split(" ")[1]+bcolors.ENDC)
            print('='*30)"""
            return pokemon_res

        except KeyError:
            #print(bcolors.WARNING+'Pokémon non trouvé'+bcolors.ENDC)
            return 0
    else:
        return 0

"""if __name__ == '__main__':
    print(get_pokemon_res_csv("Stalgamin"))"""