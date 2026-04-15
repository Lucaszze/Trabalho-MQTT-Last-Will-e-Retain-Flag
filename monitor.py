import paho.mqtt.client as mqtt

# Configurações do Broker (usando o broker público da HiveMQ para testes)
BROKER = "broker.hivemq.com"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print(f"✅ Monitor conectado ao broker com código de resultado: {rc}")
    print("📡 Assinando tópicos do frigorífico...\n")
    # Assina os tópicos de status e temperatura
    client.subscribe("frigorifico/1/status")
    client.subscribe("frigorifico/1/temp")

def on_message(client, userdata, msg):
    # Decodifica a mensagem
    payload = msg.payload.decode()
    # Verifica se a mensagem veio do cache do broker (Retained)
    is_retained = "Sim" if msg.retain else "Não"
    
    print(f"[{msg.topic}] Dado: {payload} | Mensagem Retida? {is_retained}")

# Configura o cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Iniciando Monitor...")
client.connect(BROKER, PORT, 60)

# Mantém o script rodando para receber mensagens
client.loop_forever()