import asyncio
import json
from rag.mqtt_test import send_mqtt

def on_call(topic, dados_json):
    try:
        # Verifica se já existe um loop de evento em execução
        loop = asyncio.get_event_loop()

        # Usa nest_asyncio para permitir eventos aninhados, caso seja necessário
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            # Executa a função MQTT no loop de evento já existente
            asyncio.ensure_future(send_mqtt(topic, json.dumps(dados_json)))
        else:
            # Executa a função MQTT criando um novo loop de eventos
            asyncio.run(send_mqtt(topic, json.dumps(dados_json)))
    except Exception as e:
        print(f"Erro no envio MQTT: {e}")
