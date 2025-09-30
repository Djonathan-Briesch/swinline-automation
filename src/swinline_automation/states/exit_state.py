from swinline_automation.hardware.hardware_controller import HardwareController
from swinline_automation.interfaces import FeederStateInterface
from swinline_automation.models import SowFeedingSession
from swinline_automation.mqtt.client import MQTTClient


class ExitState(FeederStateInterface):
    """Estado de saída da máquina de alimentação."""

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
        Ex.: inicializa temporizador de saída, trava portas se necessário.
        """
        pass

    def exit(self) -> None:
        """Chamado automaticamente ao sair do estado.
        Ex.: limpa temporizadores ou sinalizações usadas pelo estado.
        """
        pass

    def update(self) -> None:
        """Chamado continuamente enquanto estiver neste estado.
        Executa a lógica periódica associada à saída do animal.
        """
        pass
