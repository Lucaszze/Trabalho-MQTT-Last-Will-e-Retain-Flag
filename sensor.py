import paho.mqtt.client as mqtt
import time
import sys

BROKER = "broker.hivemq.com"
PORT = 1883

client = mqtt.Client()

# ====================================================================
# 1. LAST WILL AND TESTAMENT (LWT)
# Deve ser configurado ANTES de conectar ao broker!
# Se o sensor desconectar abruptamente, o broker publica isso:
# ====================================================================
client.will_set("frigorifico/1/status", payload="INATIVO/ERRO (LWT Acionado)", qos=1, retain=True)

print("🔌 Conectando o sensor ao broker...")
client.connect(BROKER, PORT, 60)
client.loop_start()

client.publish("frigorifico/1/status", payload="Ativo e Operacional", qos=1, retain=True)
time.sleep(1)

# ====================================================================
# 2. RETAINED MESSAGE
# Publicamos a temperatura com retain=True. O broker vai guardar este valor.
# ====================================================================
print("🌡️ Publicando a temperatura atual...")
client.publish("frigorifico/1/temp", payload="2°C", qos=1, retain=True)

print("\n✅ Sensor operando normalmente.")
print("⚠️ Pressione Ctrl+C para simular uma QUEDA DE ENERGIA (Crash abrupto).")
print("   (Isso fará com que o broker dispare o Last Will no monitor)\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nBOOM! Queda de energia simulada. O script foi fechado abruptamente.")
    sys.exit(1)