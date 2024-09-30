import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.cleanup()

try:
    # Config initial
	motor_in1 = 17
	motor_in2 = 18
	motor_pwm1 = 12
	
	motor_in3 = 22
	motor_in4 = 23
	motor_pwm2 = 13
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(motor_in1, GPIO.OUT)
	GPIO.setup(motor_in2, GPIO.OUT)
	GPIO.setup(motor_in3, GPIO.OUT)
	GPIO.setup(motor_in4, GPIO.OUT)
	GPIO.setup(motor_pwm1, GPIO.OUT)
	GPIO.setup(motor_pwm2, GPIO.OUT)

	pwm1 = GPIO.PWM(motor_pwm1, 300)  # Cria um objeto PWM com frequência de 100 Hz
	pwm1.start(0)  # Inicializa o PWM com ciclo de trabalho 0 (motor desligado)
	
	pwm2 = GPIO.PWM(motor_pwm2, 300)
	pwm2.start(0)
	
	def set_motor_direction(direction):
		if direction == "forward":
			GPIO.output(motor_in1, GPIO.HIGH)
			GPIO.output(motor_in2, GPIO.LOW)
			GPIO.output(motor_in3, GPIO.HIGH)
			GPIO.output(motor_in4, GPIO.LOW)
		elif direction == "back":
			GPIO.output(motor_in1, GPIO.LOW)
			GPIO.output(motor_in2, GPIO.HIGH)
			GPIO.output(motor_in3, GPIO.LOW)
			GPIO.output(motor_in4, GPIO.HIGH)
		elif direction == "stop":
			GPIO.output(motor_in1, GPIO.LOW)
			GPIO.output(motor_in2, GPIO.LOW)
			GPIO.output(motor_in3, GPIO.LOW)
			GPIO.output(motor_in4, GPIO.LOW)
		elif direction == "right":
			GPIO.output(motor_in1, GPIO.HIGH)
			GPIO.output(motor_in2, GPIO.LOW)
			GPIO.output(motor_in3, GPIO.LOW)
			GPIO.output(motor_in4, GPIO.HIGH)
		elif direction == "left":
			GPIO.output(motor_in1, GPIO.LOW)
			GPIO.output(motor_in2, GPIO.HIGH)
			GPIO.output(motor_in3, GPIO.HIGH)
			GPIO.output(motor_in4, GPIO.LOW)
		else:
			print("Foi enviado uma instrução inválida para o motor.")
			
	def set_motor_speed(speed):
		pwm1.ChangeDutyCycle(speed)
		pwm2.ChangeDutyCycle(speed)
		
	def on_message(client, userdata, message):
		payload = message.payload.decode("utf-8")
		print("Mensagem recebida:", payload)
		direction = payload.split(",")[0] 
		speed = int(payload.split(",")[1])
		set_motor_direction(direction)  # Define a direção do motor (True para frente)
		set_motor_speed(speed)
		
	# Configuração do cliente MQTT
	client = mqtt.Client(client_id="raspsergio", protocol=mqtt.MQTTv311)

	# Conexão e configuração das funções de callback
	client.connect(host="mqtt-dashboard.com")
	client.on_message = on_message

	client.loop_start()
	client.subscribe("robot-controlls")

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		pass
	
    # pwm.stop()
	
except Exception as error:
	print("ERRO AQUI:", error)
	GPIO.cleanup()