import pandas as pd
import requests,re
from IPython.display import display
from bs4 import BeautifulSoup


customer_data_file = 'output_com03.pkl'

head = {'User-agent': 'Mozilla/5.0 (Windows 98) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
        'Referer': 'http://www.deathmetal.org/'}

customers = pd.read_pickle(customer_data_file)
jogos_df = pd.DataFrame(customers)

for jogos in jogos_df:

    url_alvo = "https://store.playstation.com/pt-br/product/"+jogos_df[jogos]['id']
    print('Nome :' + jogos + ' Url :'+str(url_alvo)+' Valor Atual : '+ str(jogos_df[jogos]['basePrice']) )
    try:
        pagina = requests.get(url_alvo, headers=head)
        print(pagina.status_code)
    except Exception:
        print('error')
    soup = BeautifulSoup(pagina.content, 'html.parser')

    valor_final = soup.find("span", {"data-qa": "mfeCtaMain#offer0#finalPrice"})
    jogos_df[jogos]['discountedPrice'] = valor_final
    print(valor_final)

jogos_df.to_pickle('output_com04.pkl')
jogos_df.to_excel('output_com04.xlsx', sheet_name='Jogos')
