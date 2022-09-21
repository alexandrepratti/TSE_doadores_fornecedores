import requests as r
import cpfs
import pandas as pd

cookies = {
    'TS01f64d71': '0103a0ceae5e058b4db5cee1a67ab62b5a4ad4c9b453e027bcb3ea4b54cc3ddc21d1a1666754bf30825119870540fc7b18b96cb713c6289e3c3b675e21a655786f5c781da7',
    'JSESSIONID': '7opkFXsdmaTaTLTDR3fLksR07ve5jGr125i6jH5J.divulgacandcontas-01',
    '__utma': '260825096.1472600465.1662993044.1662993044.1662993044.1',
    '__utmc': '260825096',
    '__utmz': '260825096.1662993044.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmb': '260825096.1.10.1662993044',
    '_ga': 'GA1.3.1472600465.1662993044',
    '_gid': 'GA1.3.672108259.1662993061',
    '_dc18a': 'http://192.168.192.214:8180',
    'TS01efa917': '0103a0ceae226bacac9566f3c71831449e610ffca2d3712a4bc9f243535e15e933c62fbf69299c430c4e558642da40b022652c252599af66b8a5ef8fc3acb120b52bc308a2',
    '_d8a23': 'http://192.168.192.70:8180',
}

headers = {
    'authority': 'divulgacandcontas.tse.jus.br',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,az;q=0.6',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'TS01f64d71=0103a0ceae5e058b4db5cee1a67ab62b5a4ad4c9b453e027bcb3ea4b54cc3ddc21d1a1666754bf30825119870540fc7b18b96cb713c6289e3c3b675e21a655786f5c781da7; JSESSIONID=7opkFXsdmaTaTLTDR3fLksR07ve5jGr125i6jH5J.divulgacandcontas-01; __utma=260825096.1472600465.1662993044.1662993044.1662993044.1; __utmc=260825096; __utmz=260825096.1662993044.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=260825096.1.10.1662993044; _ga=GA1.3.1472600465.1662993044; _gid=GA1.3.672108259.1662993061; _dc18a=http://192.168.192.214:8180; TS01efa917=0103a0ceae226bacac9566f3c71831449e610ffca2d3712a4bc9f243535e15e933c62fbf69299c430c4e558642da40b022652c252599af66b8a5ef8fc3acb120b52bc308a2; _d8a23=http://192.168.192.70:8180',
    'referer': 'https://divulgacandcontas.tse.jus.br/',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

link = 'https://divulgacandcontas.tse.jus.br/divulga/rest/v1/doador-fornecedor/receita/detalhe/2040602022/{0}'
link2 = 'https://divulgacandcontas.tse.jus.br/divulga/rest/v1/doador-fornecedor/consulta/totalizador/2040602022/{0}'
s = r.Session()

lista = []
lista2 = []
for num, cpf in enumerate(cpfs.cpfs):
    response = s.get(link.format(cpf), cookies=cookies, headers=headers)
    response2 = s.get(link2.format(cpf), cookies=cookies, headers=headers)
    
    # Pega os doadores de campanha
    if len(response.json()) > 0:
        print(f'O {num}º CPF, de número {cpf}, foi doador de campanha')
        lista.append(response.json())
    
    # Pega os fornecedores de campanha
    if response2.json()['despesas']['valorTotalGeralDespesas'] is not None:
        print(f'O {num}º CPF, de número {cpf}, foi fornecedor de campanha')
        lista2.append(response2.json())
    print(num)

# Salva os doadores de campanha
if len(lista) > 0:
    colunas = list(lista[0][0].keys())
    resultado = pd.DataFrame(columns = colunas)
    resultado = resultado.append(lista[0])
    resultado.to_excel('Doadores.xlsx', index = False)
    print("Resultados dos doadores salvos em Doadores.xlsx")
else:
    print("Não foram obtidos resultados para Doadores de campanhas")
    
if len(lista2)>0:
    resultado2 = pd.DataFrame()
    
    #junta todos os resultados no DataFrame
    for l in lista2:
        data = l['despesas']
        resultado2 = resultado2.append(pd.json_normalize(data))
    
    resultado2.to_excel('Fornecedores.xlsx', index = False)
    print("Resultados dos fornecedores salvos em Fornecedores.xlsx")
else:
    print("Não foram obtidos resultados para Fornecedores de campanhas")
