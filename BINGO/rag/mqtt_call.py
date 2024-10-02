import asyncio
import json
import paho.mqtt.client as mqtt

from rag.mqtt_test import send_mqtt

def on_call(dados_json):
	# print("ON CALL")
	# client = mqtt.Client(client_id="roma", protocol=mqtt.MQTTv311)
	# broker = "broker.mqtt-dashboard.com"
	# porta = 8884

	# try:
	# 	client.on_connect = lambda client, userdata, flags, rc: print(f"Conectado com código: {rc}")
	# 	client.connect(broker, porta)
	# 	print("Conseguiu conectar ao broker")
	# except Exception as e:
	# 	print(f"Erro ao conectar ao broker: {e}")
	# 	return

	# json_data = json.dumps(dados_json) # formata o json para string
	# print(f"json_data: {json_data}")
	# topico = "bingo"

	# try:
	# 	client.loop_start()
	# 	rc, mid = client.publish(
	# 		topic=topico, 
	# 		payload=json_data, qos=2,
	# 		retain=True)
	# 	print(f"res: {rc}, {mid}")
	# 	print("Conseguiu publicar")
	# except Exception as e:
	# 	print(f"Erro ao publicar: {e}")
	# 	return
	
	# client.loop_stop()
	# client.disconnect()

	# print("ON END")
    
	asyncio.run(send_mqtt(json.dumps(dados_json)))
    
