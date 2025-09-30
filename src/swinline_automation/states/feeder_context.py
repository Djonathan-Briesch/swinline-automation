from __future__ import annotations

from swinline_automation.hardware.hardware_controller import HardwareController
from swinline_automation.interfaces import FeederStateInterface
from swinline_automation.models import SowFeedingSession
from swinline_automation.mqtt.client import MQTTClient
from swinline_automation.states import ExitState, FeedingState, WaitingState


class FeederContext:
    """
    Contexto da máquina de estados.
    Controla o estado atual e gerencia transições entre estados.
    """

    def __init__(
        self,
        hardware_controller: HardwareController,
        mqtt_client: MQTTClient,
        sow_feeding_session: SowFeedingSession,
    ):
        self.current_state: FeederStateInterface | None = None
        self.hardware_controller = hardware_controller
        self.mqtt_client = mqtt_client
        self.sow_feeding_session = sow_feeding_session

    def set_state(self, new_state: FeederStateInterface) -> None:
        """
        Altera o estado atual da máquina.
        Chama exit() do estado antigo e enter() do novo estado.
        Verifica se a transição é permitida.
        """
        if self.current_state:
            if type(new_state) not in self.current_state.allowed_transitions:
                raise ValueError(
                    f"Transição de {type(self.current_state).__name__} "
                    f"para {type(new_state).__name__} não permitida"
                )
            self.current_state.exit()

        self.current_state = new_state
        self.current_state.enter()

    def update(self) -> None:
        """Executa a lógica contínua do estado atual."""
        if self.current_state:
            self.current_state.update()

    # Métodos de transição de estado
    def start_waiting(self) -> None:
        """Transição para o estado de espera."""
        self.set_state(
            WaitingState(
                hardware_controller=self.hardware_controller,
                mqtt_client=self.mqtt_client,
                sow_feeding_session=self.sow_feeding_session,
                allowed_transitions=[FeedingState],
            )
        )

    def start_feeding(self) -> None:
        """Transição para o estado de alimentando."""
        self.set_state(
            FeedingState(
                hardware_controller=self.hardware_controller,
                mqtt_client=self.mqtt_client,
                sow_feeding_session=self.sow_feeding_session,
                allowed_transitions=[ExitState],
            )
        )

    def start_exit(self) -> None:
        """Transição para o estado de saída."""
        self.set_state(
            ExitState(
                hardware_controller=self.hardware_controller,
                mqtt_client=self.mqtt_client,
                sow_feeding_session=self.sow_feeding_session,
                allowed_transitions=[WaitingState, FeedingState],
            )
        )
