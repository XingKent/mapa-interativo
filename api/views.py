import requests
from django.http import JsonResponse
from django.shortcuts import render

#NAO OUSE MEXER NESTA MERDA DE DICIONARIO!!!!!!
UF_CODES = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23, "DF": 53,
    "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50, "MG": 31, "PA": 15,
    "PB": 25, "PR": 41, "PE": 26, "PI": 22, "RJ": 33, "RN": 24, "RS": 43,
    "RO": 11, "RR": 14, "SC": 42, "SP": 35, "SE": 28, "TO": 17
}

#NEM NESSE!!!!!
CAPITAIS_CODIGO_IBGE = {
    "AC": "1200401", "AL": "2704302", "AP": "1600303", "AM": "1302603", "BA": "2927408",
    "CE": "2304400", "DF": "5300108", "ES": "3205309", "GO": "5208707", "MA": "2111300",
    "MT": "5103403", "MS": "5002704", "MG": "3106200", "PA": "1501402", "PB": "2507507",
    "PR": "4106902", "PE": "2611606", "PI": "2211001", "RJ": "3304557", "RN": "2408102",
    "RS": "4314902", "RO": "1100205", "RR": "1400100", "SC": "4205407", "SP": "3550308",
    "SE": "2800308", "TO": "1721000"
}

def indicadores_estado(request, uf):
    uf = uf.upper() #deixa a sigla maiuscula
    #verifica se a sigla da UF é valida
    if uf not in UF_CODES or uf not in CAPITAIS_CODIGO_IBGE:
        return JsonResponse({"erro": "UF inválida"}, status=404) #da erro se a sigla nn existe

    #pega os códigos do estado e da capital no ibge
    codigo_ibge_uf = UF_CODES[uf]
    codigo_ibge_capital = CAPITAIS_CODIGO_IBGE[uf]
    ano_mes = "202401"

    #Taxa de desemprego
    try:
        url_desemprego = f"https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/{ano_mes}/variaveis/4099?localidades=N3[{codigo_ibge_uf}]" #api
        response_desemprego = requests.get(url_desemprego)#requisicao
        response_desemprego.raise_for_status() 
        dados = response_desemprego.json() #json
        serie_desemprego = dados[0]["resultados"][0]["series"][0]["serie"] #nem eu sei como isso funciona direito mas basicamente pega o valor especifico que eu quero
        desemprego_valor = serie_desemprego.get(ano_mes, "Dados indisponíveis")
    except:
        desemprego_valor = "Dados indisponíveis"

    #Inflacao
    try:
        url_inflacao = f"https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos/{ano_mes}/variaveis/63?localidades=N6[{codigo_ibge_capital}]"
        response_inflacao = requests.get(url_inflacao)
        response_inflacao.raise_for_status()
        dados_inf = response_inflacao.json()
        serie_inflacao = dados_inf[0]["resultados"][0]["series"][0]["serie"]
        inflacao_valor = serie_inflacao.get(ano_mes, "Dados indisponíveis")
    except:
        inflacao_valor = "Dados indisponíveis"

    periodo_formatado = f"{ano_mes[:4]}-{ano_mes[4:]}"  #2024-01

    #retorna tudo organizado num json
    return JsonResponse({
        "uf": uf,
        "desemprego": f"{desemprego_valor}%" if desemprego_valor != "Dados indisponíveis" else desemprego_valor,
        "inflacao": f"{inflacao_valor}%" if inflacao_valor != "Dados indisponíveis" else inflacao_valor,
        "periodo": periodo_formatado
    })

#essa praga tirou 2 anos da minha vida mas ela só renderiza a pagina principal quando acesso a home
def homepage(request):
    return render(request, 'main.html')
