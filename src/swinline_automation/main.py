from swinline_automation.mqtt.client import MQTTClient


mqtt_client = MQTTClient(
    client_id="maquina_01",
    host="localhost",
    port=1883,
    username="python",
    password="senha"
)

mqtt_client.connect()

# Enviar dados
mqtt_client.send_rfid_identification("1234567890")
mqtt_client.send_feeding_consumption_log(pig_id="suino_01", amount=2.5)
mqtt_client.send_alert("Baixo nível de ração", level="WARNING")
