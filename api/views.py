import requests
from django.http import JsonResponse
from django.shortcuts import render

#NAO MEXER NESTA MERDA!!!!
UF_CODES = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23, "DF": 53,
    "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50, "MG": 31, "PA": 15,
    "PB": 25, "PR": 41, "PE": 26, "PI": 22, "RJ": 33, "RN": 24, "RS": 43,
    "RO": 11, "RR": 14, "SC": 42, "SP": 35, "SE": 28, "TO": 17
}

#NEM NESSA!!!!!!!!
INFLACAO_MOCK = {
    "RR": "0.48%", "AM": "0.23%", "PA": "0.51%", "AP": "0.62%", "RO": "0.35%", 
    "MT": "0.39%", "TO": "0.42%", "PI": "0.45%", "BA": "0.55%", "MG": "0.49%", 
    "ES": "0.41%", "RJ": "0.44%", "SP": "0.38%", "PR": "0.52%", "SC": "0.43%", 
    "RS": "0.40%", "CE": "0.47%", "RN": "0.50%", "PB": "0.36%", "PE": "0.48%", 
    "AL": "0.37%"
}

def indicadores_estado(request, uf):
    uf = uf.upper()
    if uf not in UF_CODES:
        return JsonResponse({"erro": "UF inválida"}, status=404)

    codigo_ibge = UF_CODES[uf]
    ano_mes = "202401"

    #taxa de desemprego
    url_desemprego = f"https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/%7Bano_mes%7D/variaveis/4099?localidades=N3[{codigo_ibge}]"

    #inflação
    url_inflacao = f"https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos/%7Bano_mes%7D/variaveis/63?localidades=N3[{codigo_ibge}]"

    try:
        #desemprego
        res_desemprego = requests.get(url_desemprego)
        res_desemprego.raise_for_status()
        valor_desemprego = res_desemprego.json()[0]["resultados"][0]["series"][0]["serie"].get(ano_mes, None)
        desemprego = f"{valor_desemprego}%" if valor_desemprego else "Dados indisponíveis" 
        #inflação
        res_inflacao = requests.get(url_inflacao)
        res_inflacao.raise_for_status()
        valor_inflacao = res_inflacao.json()[0]["resultados"][0]["series"][0]["serie"].get(ano_mes, None)

        #se o valor da inflacao for none ou uma string inválida usa o mock
        if not valor_inflacao or str(valor_inflacao).strip() == "...":
            inflacao = INFLACAO_MOCK.get(uf, "Dados indisponíveis")
        else:
            inflacao = f"{valor_inflacao}%"

        periodo_formatado = f"{ano_mes[:4]}-{ano_mes[4:]}"

        return JsonResponse({
            "uf": uf,
            "desemprego": desemprego,
            "inflacao": inflacao,
            "periodo": periodo_formatado
        })

    except Exception as e:
        print("Erro na requisição:", e)
        return JsonResponse({"erro": "Erro ao acessar a API do IBGE"}, status=500)

def homepage(request):
    return render(request, 'main.html')