from swinline_automation.hardware.hardware_controller import HardwareController
from swinline_automation.interfaces import FeederStateInterface
from swinline_automation.models import SowFeedingSession
from swinline_automation.mqtt.client import MQTTClient


class WaitingState(FeederStateInterface):
    """Estado de espera da máquina."""

    def __init__(
        self,
        hardware_controller: HardwareController,
        mqtt_client: MQTTClient,
        sow_feeding_session: SowFeedingSession,
        allowed_transitions: list[type[FeederStateInterface]],
    ):
        self.hardware_controller = hardware_controller
        self.mqtt_client = mqtt_client
        self.sow_feeding_session = sow_feeding_session
        self.allowed_transitions = allowed_transitions

    def enter(self) -> None:
        """Chamado automaticamente ao entrar no estado.
        Ex.: inicializa sensores de presença, reseta flags de leitura de RFID.
        """
        pass

    def exit(self) -> None:
        """Chamado automaticamente ao sair do estado.
        Ex.: limpa temporizadores e sinalizações usadas pelo estado de espera.
        """
        pass

    def update(self) -> None:
        """Chamado continuamente enquanto estiver neste estado.
        Executa a lógica periódica de espera do animal, como verificar presença.
        """
        pass
