import requests
from django.http import JsonResponse
from django.shortcuts import render

UF_CODES = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23, "DF": 53,
    "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50, "MG": 31, "PA": 15,
    "PB": 25, "PR": 41, "PE": 26, "PI": 22, "RJ": 33, "RN": 24, "RS": 43,
    "RO": 11, "RR": 14, "SC": 42, "SP": 35, "SE": 28, "TO": 17
}

def indicadores_estado(request, uf):
    uf = uf.upper()
    if uf not in UF_CODES:
        return JsonResponse({"erro": "UF inválida"}, status=404)

    codigo_ibge = UF_CODES[uf]
    tabela_id = "4093"  #desemprego
    ano_mes = "202401"  #mes e ano
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{tabela_id}/periodos/{ano_mes}/variaveis/4099?localidades=N3[{codigo_ibge}]"

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()

        #verifica se os dados estão presentes na resposta
        resultados = dados[0].get("resultados", [])
        if not resultados:
            return JsonResponse({"erro": "Dados não encontrados para o estado informado."}, status=404)

        series = resultados[0].get("series", [])
        if not series:
            return JsonResponse({"erro": "Série de dados não encontrada para o estado informado."}, status=404)

        serie = series[0].get("serie", {})
        if not serie:
            return JsonResponse({"erro": "Dados da série não disponíveis para o estado informado."}, status=404)

        valor = serie.get(ano_mes)
        if valor is None:
            return JsonResponse({"erro": "Valor não disponível para o período especificado."}, status=404)

        periodo_formatado = f"{ano_mes[:4]}-{ano_mes[4:]}"

        return JsonResponse({
            "uf": uf,
            "desemprego": f"{valor}%",
            "inflacao": "Dados indisponíveis",
            "periodo": periodo_formatado
        })

    except Exception as e:
        return JsonResponse({"erro": "Erro ao acessar a API do IBGE"}, status=500)

def homepage(request):
    return render(request, 'main.html')