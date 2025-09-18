import json
import paho.mqtt.client as mqtt
from typing import Optional
from swinline_automation.mqtt.constants.mqtt_topics import MQTTTopics
from dto.feeder_settings_dto import FeederSettingsDTO
from dto.daily_feeding_dto import DailyFeedingDTO
from dto.rfid_dto import RFIDDTO
from dto.feeding_consumption_log_dto import FeedingConsumptionLogDTO
from dto.alert_create_dto import AlertCreateDTO
from dto.alert_parameter_dto import AlertParameterDTO

from queue import Queue


class MQTTClient:
    """
    Cliente MQTT para comunicação com a API SwineFarm.
    - Callbacks específicos para tópicos recebidos.
    - Métodos auxiliares para publicar em tópicos de envio.
    """

    def __init__(
        self, client_id: str, host: str, port: int, username: str, password: str
    ):
        self.client = mqtt.Client(client_id=client_id, clean_session=False)
        self.client.username_pw_set(username, password)

        # Callbacks de conexão
        self.client.on_connect = self.on_connect

        # Configura conexão
        self.host = host
        self.port = port

        # Filas para receber dados
        self.feeder_queue: Queue[FeederSettingsDTO] = Queue()
        self.daily_feeding_queue: Queue[DailyFeedingDTO] = Queue()
        self.alert_parameter_queue: Queue[AlertParameterDTO] = Queue()

        # Adiciona callbacks específicos
        self.client.message_callback_add(
            MQTTTopics.RECEIVE_FEEDER_SETTINGS.value, self.on_feeder_settings
        )
        self.client.message_callback_add(
            MQTTTopics.RECEIVE_DAILY_FEEDING.value, self.on_daily_feeding
        )

    # ----------------------------
    # Conexão
    # ----------------------------
    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("✅ Conectado ao broker com código:", rc)
        # Assinar somente os tópicos que recebe
        client.subscribe(MQTTTopics.RECEIVE_FEEDER_SETTINGS.value)
        client.subscribe(MQTTTopics.RECEIVE_DAILY_FEEDING.value)

    # ----------------------------
    # Callbacks específicos de recebimento
    # ----------------------------

    # PARA USAR
    # while True:
    #     feeder_dto = mqtt_client.feeder_queue.get()
    #     print("Feeder recebido:", feeder_dto)
    #     mqtt_client.feeder_queue.task_done()

    # # Processando daily feeding
    # while True:
    #     daily_dto = mqtt_client.daily_feeding_queue.get()
    #     print("Daily feeding recebido:", daily_dto)
    #     mqtt_client.daily_feeding_queue.task_done()

    def on_feeder_settings(self, client, userdata, message) -> None:
        payload = message.payload.decode()
        data = json.loads(payload)
        dto = FeederSettingsDTO(**data)
        self.feeder_queue.put(dto)

    def on_daily_feeding(self, client, userdata, message) -> None:
        payload = message.payload.decode()
        data = json.loads(payload)
        dto = DailyFeedingDTO(**data)
        self.daily_feeding_queue.put(dto)

    def on_alert_parameter(self, client, userdata, message) -> None:
        payload = message.payload.decode()
        data = json.loads(payload)
        dto = AlertParameterDTO(**data)
        self.alert_parameter_queue.put(dto)

    # ----------------------------
    # Métodos auxiliares de envio
    # ----------------------------
    def send_rfid_identification(self, rfid_dto: RFIDDTO):
        """
        Envia o RFID do animal via MQTT.

        Args:
            rfid_dto (RFIDDTO): DTO contendo o RFID do animal.

        Returns:
            bool: True se a mensagem foi enviada corretamente, False em caso de erro no envio.
        """
        payload = rfid_dto.model_dump_json(ensure_ascii=False)
        try:
            info = self.client.publish(
                MQTTTopics.SEND_RFID_IDENTIFICATION.value, payload, qos=1
            )
            return info.wait_for_publish()
        except Exception as e:
            return False

    def send_feeding_consumption_log(
        self, feeding_consumption: FeedingConsumptionLogDTO
    ) -> bool:
        payload = feeding_consumption.model_dump_json(ensure_ascii=False)
        try:
            info = self.client.publish(
                MQTTTopics.SEND_FEEDING_CONSUMPTION_LOG, payload, qos=1
            )
            info.wait_for_publish()
        except Exception as e:
            return False

    def send_alert(self, alert_dto: AlertCreateDTO):
        payload = alert_dto.model_dump_json(ensure_ascii=False)
        try:
            info = self.client.publish(MQTTTopics.SEND_ALERT, payload, qos=1)
            info.wait_for_publish()
        except Exception as e:
            return False
