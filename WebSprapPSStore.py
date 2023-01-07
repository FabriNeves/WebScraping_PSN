import requests, json, re
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display
import openpyxl
import time


# Cria uma planilha
book = openpyxl.Workbook()
# Criar uma pagina
book.create_sheet("Jogos")

num2 = 500
i = 1
dict_output = {}
dict_output2 = {}
count2 = 0
while i <= num2:
    pagina = str(i)
    # id="__NEXT_DATA__"
    url_alvo = ("https://store.playstation.com/pt-br/category/85448d87-aa7b-4318-9997-7d25f4d275a4/" + pagina)
    pagina = requests.get(url_alvo)
    pagina.encoding = 'utf-8'
    soup = BeautifulSoup(pagina.content, 'html.parser')
    list_of_scripts = soup.find_all('script')
    data = json.loads(soup.find('script', id='__NEXT_DATA__').text)
    dado_extrair = data['props']['apolloState']
    mylist = ["id", "name", "basePrice", "discountedPrice", "discountText", "localizedStoreDisplayClassification",
              "isFree", "isExclusive", "isTiedToSubscription", "link"]

    dict_de_valores = dict.fromkeys(mylist, 0)

    count = 0
    for d in dado_extrair:
        # print(dado_extrair)
        # Estados do apolloState
        retorno = str(re.search(r'Product', d))
        if retorno != "None":
            for n in dado_extrair[d]:
                # Verifica se algum valor do dicionario onde é a palavra chave Product é igual ao da lista de valores desejados
                for y in mylist:
                    # testa um após o outro as palavras chaves
                    if y == n:  # se valor for positivo extrai o valor  utilizando as keys do dicionario  Sendo "d" a tag de 'product' e y a tag local aonde esta a informação
                        dict_de_valores[y] = dado_extrair[d][n]
                        count = count + 1
                        if count == len(mylist):
                            print(dict_de_valores)

                            dict_output[dict_de_valores['name']] = json.dumps(dict_de_valores)
                            count2 = count2 + 1
                            count = 0
    time.sleep(0.1)
    i += 1

for k in dict_output:
    s = dict_output[k]
    s = json.loads(s)
    # print(s)
    dict_output[k] = s
'''
# Como selecionar uma pagina
jogos_page = book['Jogos']
jogos_page.append(['id', 'name', 'basePrice', 'discountedPrice', 'discountText', 'localizedStoreDisplayClassification',
              'isFree', 'isExclusive', 'isTiedToSubscription'])

for j in dict_output:
    jogos_page.append([dict_output[j]['id'], dict_output[j]['name'], dict_output[j]['basePrice'], dict_output[j]['discountedPrice'], dict_output[j]['discountText'], dict_output[j]['localizedStoreDisplayClassification'],
             dict_output[j]['isFree'], dict_output[j]['isExclusive'], dict_output[j]['isTiedToSubscription']])
'''
jogos_df = pd.DataFrame(dict_output)
jogos_df.to_pickle("output_raw.pkl")
jogos_df.to_excel('output_raw.xlsx', sheet_name='Jogos')


# Salvar a planilha
# book.save('DadosJogos10-2021.xlsx')
