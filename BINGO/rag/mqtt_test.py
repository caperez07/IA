import nest_asyncio
import asyncio
from gmqtt import Client as MQTTClient

# Permite o uso de asyncio no Colab
nest_asyncio.apply()

# Função de callback para quando o cliente se conectar ao broker
def on_connect(client, flags, rc, properties):
    print('Conectado com sucesso!')

# Função de callback para quando a mensagem for publicada
def on_publish(client, mid):
    print(f'Mensagem publicada com sucesso com mid: {mid}')

async def send_mqtt(message):
    # Cria o cliente MQTT com um ID único
    client = MQTTClient("client_id_bingo")

    # Define as funções de callback
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Conecta ao broker público HiveMQ
    await client.connect('mqtt-dashboard.com')

    # Publica a mensagem no tópico 'bingo/teste' com o conteúdo de `message`
    client.publish('bingo/teste', message)

    # Aguarda um curto intervalo para garantir que a mensagem seja publicada
    await asyncio.sleep(0.5)

    # Desconecta do broker
    await client.disconnect()

# Exemplo de execução, passando uma mensagem para enviar
# asyncio.run(send_mqtt("Sua mensagem personalizada"))
