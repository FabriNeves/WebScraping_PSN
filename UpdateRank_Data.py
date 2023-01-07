import pandas as pd
import requests,re
from IPython.display import display
from bs4 import BeautifulSoup


customer_data_file = 'output_completorev01.pkl'

head = {'User-agent': 'Mozilla/5.0 (Windows 98) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
        'Referer': 'http://www.deathmetal.org/'}

customers = pd.read_pickle(customer_data_file)
jogos_df = pd.DataFrame(customers)

# jogos_df.to_pickle('output_restruturado.pkl')
display(jogos_df)
jogos_dict = jogos_df.to_dict()

for jogos in jogos_dict:
    print('---')
    print('Nome :'+jogos)
    url_alvo = jogos_dict[jogos]['link']
    print('Url :'+str(url_alvo))
    print('Rating '+str(jogos_dict[jogos]['Rating']))
    if str(jogos_dict[jogos]['Rating']) == "nan":
        try:
            pagina = requests.get(url_alvo, headers=head)

        except Exception:
            print('error')

        if pagina.status_code == 200:
            soup = BeautifulSoup(pagina.content, 'html.parser')

            rating = soup.find("span", {"itemprop": "ratingValue"})

            combinacao = re.search('[0-9][0-9]', str(rating))
            if combinacao:

                jogos_dict[jogos]['Rating'] = int(combinacao.group(0))
                print(jogos_dict[jogos]['Rating'])
            else:
                print('Sem dados')

            data_ = soup.find_all("span", {"class": "data"})

            combinacao = re.search('\w\w\w [0-9][0-9], [0-2][0][0-3][0-9]', str(data_))
            if combinacao:

                jogos_dict[jogos]['Data'] = combinacao.group(0)
                print(jogos_dict[jogos]['Data'])
            else:
                print('Sem dados')
    print('---')


jogos_df = pd.DataFrame(jogos_dict)
display(jogos_df)

jogos_df.to_pickle('output_com03.pkl')
jogos_df.to_excel('output_com03.xlsx', sheet_name='Jogos')