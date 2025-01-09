from flask import Flask, render_template, request
import requests
from datetime import datetime, date, timedelta

app = Flask(__name__)

def consumir_api_proposicoes():
    """
    Consome a API de proposições da Câmara dos Deputados com base no intervalo de datas.
    
    Args:
        data_inicio (str): Data inicial no formato 'yyyy-MM-dd'.
        data_fim (str): Data final no formato 'yyyy-MM-dd'.
        
    Returns:
        list: Lista de proposições retornadas pela API.
    """
    data_agora = date.today()
    data_inicio = data_agora - timedelta(days=7)
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "dataInicio": data_inicio,
        "dataFim": data_agora,
        "itens": 100,
        "ordem": "DESC",
        "ordenarPor": "id",
        "siglaTipo": ["PL", "PDC", "PEC", "PLP", "PRF","MPV", "PRC"]
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta um erro se o status não for 200
        data = response.json()
        return data.get("dados", [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consumir a API: {e}")
        return [] 

@app.route("/", methods=["GET", "POST"])
def index():
    proposicoes = consumir_api_proposicoes()
    return render_template("lista_preposicoes.html", proposicoes=proposicoes)

if __name__ == "__main__":
    app.run(debug=True)
