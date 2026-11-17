
"""
consumidor_api.py
Responsável por se comunicar com a API Meteorológica Offline,
interpretar a resposta JSON e entregar os dados organizados para a interface.
"""

import requests

# Endpoint local da API (precisa estar rodando: uvicorn app.main:app --reload)
URL_API = "http://127.0.0.1:8000/v1/forecast"

# Coordenadas de Jaraguá do Sul - SC (definidas na atividade)
LATITUDE = -26.4851
LONGITUDE = -49.0713

# Tempo máximo de espera pela resposta, evita que o programa fique travado
TIMEOUT_SEGUNDOS = 10


class ErroConsumidorAPI(Exception):
    """Erro com mensagem amigável para a interface exibir ao usuário."""


def obter_dados_meteorologicos():
    """
    Consulta a API e retorna um dicionário com os indicadores atuais:
    temperatura, umidade_relativa, sensacao_termica, precipitacao,
    velocidade_vento, horario e as respectivas unidades.
    """
    # Parâmetros obrigatórios da API (nomes exatos da documentação)
    parametros = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
    }

    try:
        # Requisição HTTP GET ao endpoint de previsão
        resposta = requests.get(URL_API, params=parametros, timeout=TIMEOUT_SEGUNDOS)
        # Gera exceção se o status for 400, 404, 500...
        resposta.raise_for_status()
        # Converte o corpo da resposta (JSON) em dicionário Python
        dados = resposta.json()

    except requests.exceptions.ConnectionError:
        raise ErroConsumidorAPI(
            "Não foi possível conectar à API em 127.0.0.1:8000. "
            "Verifique se o Uvicorn está em execução."
        )
    except requests.exceptions.Timeout:
        raise ErroConsumidorAPI("A API demorou demais para responder (tempo limite excedido).")
    except requests.exceptions.HTTPError as erro:
        raise ErroConsumidorAPI(f"A API retornou um erro HTTP: {erro}")
    except ValueError:
        raise ErroConsumidorAPI("A resposta da API não é um JSON válido.")

    try:
        # Os valores atuais ficam dentro da chave "current"
        atuais = dados["current"]
        # As unidades ficam em "current_units" (usa dict vazio se não existir)
        unidades = dados.get("current_units", {})

        return {
            "temperatura": atuais["temperature_2m"],
            "umidade_relativa": atuais["relative_humidity_2m"],
            "sensacao_termica": atuais["apparent_temperature"],
            "precipitacao": atuais["precipitation"],
            "velocidade_vento": atuais["wind_speed_10m"],
            "horario": atuais["time"],
            "unidades": {
                "temperatura": unidades.get("temperature_2m", "°C"),
                "umidade_relativa": unidades.get("relative_humidity_2m", "%"),
                "sensacao_termica": unidades.get("apparent_temperature", "°C"),
                "precipitacao": unidades.get("precipitation", "mm"),
                "velocidade_vento": unidades.get("wind_speed_10m", "km/h"),
            },
        }
    except (KeyError, TypeError) as erro:
        # Campo ausente ou estrutura diferente da esperada
        raise ErroConsumidorAPI(f"Resposta da API incompleta. Campo ausente: {erro}")


if __name__ == "__main__":
    # Teste independente do consumidor (sem a interface)
    print(obter_dados_meteorologicos())