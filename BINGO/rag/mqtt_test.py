import json
import paho.mqtt.client as mqtt

def enviar_json_mqtt(broker, porta, topico, dados_json):
    # Cria um cliente MQTT
    client = mqtt.Client(client_id="clientId-42wY1MttnQ", protocol=mqtt.MQTTv311)
    
    # Conecta ao broker MQTT
    client.connect(broker, porta, 60)
    
    # Converte o dicionário Python para JSON
    dados_json_str = json.dumps(dados_json)
    
    # Publica o JSON no tópico especificado
    client.publish(topico, dados_json_str)
    
    # Desconecta do broker
    client.disconnect()

# Exemplo de uso da função
if __name__ == "__main__":
    # Define os dados que você deseja enviar
    dados = {
        "temperatura": 23.5,
        "umidade": 60
    }
    
    # Parâmetros do broker e tópico
    broker = "mqtt-dashboard.com"  # Broker público para testes
    porta = 8884                   # Porta padrão do MQTT
    topico = "bingo"

    # Envia os dados JSON via MQTT
    enviar_json_mqtt(broker, porta, topico, dados)
    print("Dados enviados com sucesso!")