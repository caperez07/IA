import json
import paho.mqtt.client as mqtt

def on_call(dados_json):
	# print("ON CALL")
	client = mqtt.Client(client_id="clientId-42wY1MttnQ", protocol=mqtt.MQTTv311)
	broker = "mqtt-dashboard.com"
	porta = 8884

	try:
		client.connect(broker, porta, 60)
		print("Conseguiu conectar ao broker")
	except Exception as e:
		print(f"Erro ao conectar ao broker: {e}")
		return

	json_data = json.dumps(dados_json) # formata o json para string
	topico = "bingo/ia"

	try:
		client.publish(topico, json_data)
		print("Conseguiu publicar")
	except Exception as e:
		print(f"Erro ao publicar: {e}")
		return
	
	client.disconnect()

	# print("ON END")
    
