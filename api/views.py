import os
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

#DOR DE CABEÇA DO CARALHGOOO
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

#NEM NESSE PORRA!!!!!!
UF_PARA_CIDADE_JSON = {
    "RR": "Rio Branco (AC)", "AM": "Rio Branco (AC)", "PA": "Belém (PA)", "AP": "Rio Branco (AC)",
    "RO": "Rio Branco (AC)", "MT": "Campo Grande (MS)", "TO": "Rio Branco (AC)", "PI": "São Luís (MA)",
    "BA": "Salvador (BA)", "MG": "Belo Horizonte (MG)", "ES": "Grande Vitória (ES)", "RJ": "Rio de Janeiro (RJ)",
    "SP": "São Paulo (SP)", "PR": "Curitiba (PR)", "SC": "Porto Alegre (RS)", "RS": "Porto Alegre (RS)",
    "CE": "Fortaleza (CE)", "RN": "Recife (PE)", "PB": "Recife (PE)", "PE": "Recife (PE)", "AL": "Aracaju (SE)"
}


#JSON externo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_PATH = os.path.join(BASE_DIR, 'data', 'dados_mock_inflacao.json')
with open(MOCK_PATH, encoding='utf-8') as mock_file:
    MOCK_JSON = json.load(mock_file)
    MOCK_VALUES = MOCK_JSON["valuesMap"]["março 2025"]

#Aqui começa uma bruxaria sinistra pfv nao toca nisso (Deus sabe lá como isso ta funcionando)
def get_ultimo_periodo_disponivel(agregado_id):
    try:
        url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado_id}/periodos"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        periodos = response.json()
        if periodos:
            return periodos[-1]['id'] 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar períodos para o agregado {agregado_id}: {e}")
    except (KeyError, IndexError) as e:
        print(f"Erro ao parsear a resposta de períodos para o agregado {agregado_id}: {e}")
    return None

def formatar_periodo(periodo_str):
    if not periodo_str or len(periodo_str) != 6:
        return "N/D"
    ano = periodo_str[:4]
    mes = periodo_str[4:]
    return f"{mes}/{ano}"

def indicadores_estado(request, uf):
    uf = uf.upper()
    if uf not in UF_CODES or uf not in CAPITAIS_CODIGO_IBGE:
        return JsonResponse({"erro": "UF inválida"}, status=404)

    codigo_ibge_uf = UF_CODES[uf]
    codigo_ibge_capital = CAPITAIS_CODIGO_IBGE[uf]
    
    #Buscar periodos sozinho
    #desemprego
    periodo_desemprego = get_ultimo_periodo_disponivel("4093")
    #inflacao
    periodo_inflacao = get_ultimo_periodo_disponivel("7060")

    desemprego_valor = "Dados indisponíveis"
    inflacao_valor = "Dados indisponíveis"

    #Buscar desemprego
    if periodo_desemprego:
        try:
            url_desemprego = f"https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/{periodo_desemprego}/variaveis/4099?localidades=N3[{codigo_ibge_uf}]"
            response_desemprego = requests.get(url_desemprego, timeout=5)
            response_desemprego.raise_for_status()
            dados = response_desemprego.json()
            serie_desemprego = dados[0]["resultados"][0]["series"][0]["serie"]
            desemprego_valor = serie_desemprego.get(periodo_desemprego, "Dados indisponíveis")
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            print(f"Erro ao buscar dados de desemprego para {uf}: {e}")
            desemprego_valor = "Dados indisponíveis"

    #Buscar inflacao
    if periodo_inflacao:
        try:
            url_inflacao = f"https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos/{periodo_inflacao}/variaveis/63?localidades=N6[{codigo_ibge_capital}]"
            response_inflacao = requests.get(url_inflacao, timeout=5)
            response_inflacao.raise_for_status()
            dados_inf = response_inflacao.json()
            serie_inflacao = dados_inf[0]["resultados"][0]["series"][0]["serie"]
            inflacao_valor = serie_inflacao.get(periodo_inflacao, "Dados indisponíveis")
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            print(f"Erro ao buscar dados de inflação para {uf}: {e}")
            inflacao_valor = "Dados indisponíveis"

    #Se valor da API for inválido, busca no mock
    if inflacao_valor in ("...", "Dados indisponíveis"):
        nome_cidade = UF_PARA_CIDADE_JSON.get(uf)
        inflacao_valor = MOCK_VALUES.get(nome_cidade, "Dados indisponíveis")

    #Formata os dados para a resposta
    return JsonResponse({
        "uf": uf,
        "desemprego": f"{desemprego_valor}%" if desemprego_valor != "Dados indisponíveis" else desemprego_valor,
        "inflacao": f"{inflacao_valor}%" if inflacao_valor != "Dados indisponíveis" else inflacao_valor,
        "periodo_desemprego": formatar_periodo(periodo_desemprego),
        "periodo_inflacao": formatar_periodo(periodo_inflacao)
    })

def homepage(request):
    return render(request, 'main.html')