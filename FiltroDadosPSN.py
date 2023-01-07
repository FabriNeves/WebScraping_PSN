
import pandas as pd


customer_data_file = 'output_raw.pkl'

customers = pd.read_pickle(customer_data_file)
jogos_df = pd.DataFrame(customers)

# display(jogos_df)

for jogos in jogos_df:

    valorJogo = jogos_df[jogos]['basePrice']
    valorJogoDescontado = jogos_df[jogos]['discountedPrice']

    if valorJogoDescontado == "Gratuito" or valorJogoDescontado == "Indisponível" \
            or valorJogo == "Gratuito" or valorJogo == "Indisponível":
        jogos_df = jogos_df.drop(jogos, axis=1)
    else:
        # print(valorJogo, valorJogoDescontado)
        valorJogo = valorJogo.replace("R$", "")
        jogos_df[jogos]['basePrice'] = float(valorJogo.replace(',', '.'))
        valorJogoDescontado = valorJogoDescontado.replace("R$", "")
        jogos_df[jogos]['discountedPrice'] = float(valorJogoDescontado.replace(',', '.'))

jogos_df.to_pickle('output_filtrado.pkl')
jogos_df.to_excel('output_filtrado.xlsx', sheet_name='Jogos')

'''
for jogos in jogos_df:
    temp_Str = "Metacritic " + jogos + " PS4"
    time.sleep(10)
    print(jogos)
    for resultados in search(temp_Str, stop=1):
        print(resultados)
        jogos_df[jogos]['link'] = resultados
display(jogos_df)

jogos_df.to_excel('output_baseDados.xlsx', sheet_name='Jogos')
jogos_df.to_excel('output_baseDados.xlsx', sheet_name='Jogos')
jogos_df = jogos_df.transpose()
jogos_df.to_excel('output_trans.xlsx', sheet_name='Jogos')
'''