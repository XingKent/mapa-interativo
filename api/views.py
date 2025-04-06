from django.http import JsonResponse

def indicadores_estado(request, uf):
    dados_mock = {
        "BA": {"desemprego": "10.1%", "inflacao": "4.6%", "periodo": "2024-04"},
        "RJ": {"desemprego": "9.0%", "inflacao": "4.4%", "periodo": "2024-04"},
        "SP": {"desemprego": "7.5%", "inflacao": "4.2%", "periodo": "2024-04"},
    }

    dados = dados_mock.get(uf.upper())
    if dados:
        return JsonResponse({"uf": uf.upper(), **dados})
    else:
        return JsonResponse({"erro": "Estado não encontrado"}, status=404)
