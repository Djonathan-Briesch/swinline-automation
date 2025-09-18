from enum import Enum


class MQTTTopics(Enum):
    """Enum para tópicos MQTT usados na comunicação com a API.

    Tópicos que o cliente recebe da API:
        RECEIVE_FEEDER_SETTINGS       - Receber as configurações da máquina
        RECEIVE_DAILY_FEEDING         - Receber o plano alimentar do suíno
        RECEIVE_ALERT_PARAMETER       - Receber as condições para envio de alertas

    Tópicos que o cliente envia para a API:
        SEND_RFID_IDENTIFICATION      - Enviar o RFID para identificar o suíno
        SEND_FEEDING_CONSUMPTION_LOG  - Enviar registro de consumo (alimentação)
        SEND_ALERT                    - Enviar alertas quando necessário
    """

    RECEIVE_FEEDER_SETTINGS = "swinefarm/machine/configurations/update"
    RECEIVE_DAILY_FEEDING = "swinefarm/swine/feeding_plan/response"
    RECEIVE_ALERT_PARAMETER = "swinefarm/receive/alert_parameter"

    SEND_RFID_IDENTIFICATION = "swinefarm/swine/identification/rfid"
    SEND_FEEDING_CONSUMPTION_LOG = "swinefarm/swine/consumption/log"
    SEND_ALERT = "swinefarm/alerts"
