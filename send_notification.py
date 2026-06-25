import logging
import os
from pathlib import Path
from wsgiref import headers

import dotenv
import requests


def send_notification(user_id: int, title: str, message: str):
    headers: dict = {
        "X-Api-Key": os.getenv("HASH", ""),
        "Content-Type": "application/json",
    }

    data: dict = {
        "user_id": user_id,
        "title": title,
        "message": message,
    }

    logging.info(f"Enviando notificação para o usuário {user_id}...")

    try:
        response = requests.post(os.getenv("URL", ""), json=data, headers=headers)

        if response.status_code == 201:
            logging.info("Notificação enviada com sucesso!")
            logging.info(f"Resposta da API: {response.json()}")
        else:
            logging.error(f"Falha ao enviar. Código HTTP {response.status_code}")
            logging.error(f"Erro retornado: {response.text}")

    except requests.exceptions.ConnectionError:
        logging.error("Erro: Não foi possível conectar ao microserviço. Certifique-se de que ele está rodando na porta 8001.")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv(dotenv_path=Path("./.env"))

    send_notification(1, "Notificação do RH", "Você foi admitido")
    send_notification(1, "Notificação do RH", "Você foi demitido")
