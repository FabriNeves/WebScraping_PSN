import pandas as pd
import requests,re
from IPython.display import display
from bs4 import BeautifulSoup

head = {'User-agent': 'Mozilla/5.0 (Windows 98) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38', 'Referer': 'http://www.deathmetal.org/'}


customer_data_file = 'output_completorev01.pkl'
customers = pd.read_pickle(customer_data_file)
jogos_raw_df = pd.DataFrame(customers)
contagem = 0
for jogo in jogos_raw_df:
    link = jogos_raw_df[jogo]['link']
    if link ==0 or link == None:
        contagem +=1
        print(jogo)
        pagina = "metacritic " + jogo + " Ps4"
        url_alvo = 'https://www.google.com/search?q=' + pagina
        pagina = requests.get(url_alvo, headers=head)
        print(pagina)
        pagina.encoding = 'utf-8'
        soup = BeautifulSoup(pagina.content, 'html.parser')
        mydivs = soup.find("div", {"class": "yuRUbf"})

        match = re.search(r'href=\"https://www.metacritic.com/game/play?([^\'\" >]+)', str(mydivs))
        # nRandom = random.randint(1, 4) https://www.metacritic.com/game/playstation-4/
        # time.sleep(nRandom)
        if match:
            jogos_raw_df[jogo]['link'] = 'https://www.metacritic.com/game/play' + match.group(1)
            print(jogos_raw_df[jogo]['link'])
        else:
            print(jogo + ' : No match')
            jogos_raw_df[jogo]['link'] = None

jogos_raw_df.to_pickle('output_completorev01.pkl')
jogos_raw_df.to_excel('output_completorev01.xlsx', sheet_name='Jogos')
print(contagem)
