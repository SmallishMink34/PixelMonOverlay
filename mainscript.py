import requests
import bs4 as bs
import jaro

def get_pokemon_res(pk="pikachu"):
    #pokemon = input("Entrez le nom du pokemon : ").title()
    print("pokemon : ", pk)
    pokemon = open("pokemonlist.txt", "r")
    liste = pokemon.readlines()
    print(jaro.jaro_metric("7 Sabelette", 'Sabelette'))
    for i in range(len(liste)):
        if jaro.jaro_metric(liste[i], pk) > 0.8:
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

        except AttributeError:
            #print(bcolors.WARNING+'Pokémon non trouvé'+bcolors.ENDC)
            return 0
    else:
        return 0
    
"""if __name__ == '__main__':
    print(get_pokemon_res("Stalgamin"))"""