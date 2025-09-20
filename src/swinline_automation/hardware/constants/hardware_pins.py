from enum import Enum


class HardwarePins(Enum):
    """Enum para pinos de hardware usados no controle do alimentador e das portas.

    Componentes de alimentação:
        FEEDER_MOTOR                  - Motor responsável por acionar o dispenser de ração

    Sensores de presença:
        INFRARED_PRESENCE_SENSOR      - Sensor infravermelho que detecta a presença do suíno na baia

    Fins de curso da porta de separação:
        SEPARATION_DOOR_LIMIT_SWITCH_CLOSED - Indica que a porta de separação está fechada
        SEPARATION_DOOR_LIMIT_SWITCH_OPEN   - Indica que a porta de separação está aberta

    Fins de curso da porta de entrada:
        ENTRY_DOOR_LIMIT_SWITCH_CLOSED      - Indica que a porta de entrada está fechada
        ENTRY_DOOR_LIMIT_SWITCH_OPEN        - Indica que a porta de entrada está aberta

    Motores da porta de separação:
        SEPARATION_DOOR_MOTOR_CLOSING  - Motor responsável por fechar a porta de separação
        SEPARATION_DOOR_MOTOR_OPENING  - Motor responsável por abrir a porta de separação

    Motores da porta de entrada:
        ENTRY_DOOR_MOTOR_CLOSING       - Motor responsável por fechar a porta de entrada
        ENTRY_DOOR_MOTOR_OPENING       - Motor responsável por abrir a porta de entrada
    """

    FEEDER_MOTOR = 22
    INFRARED_PRESENCE_SENSOR = 29

    SEPARATION_DOOR_LIMIT_SWITCH_CLOSED = 33
    SEPARATION_DOOR_LIMIT_SWITCH_OPEN = 31
    ENTRY_DOOR_LIMIT_SWITCH_CLOSED = 37
    ENTRY_DOOR_LIMIT_SWITCH_OPEN = 35

    SEPARATION_DOOR_MOTOR_CLOSING = 38
    SEPARATION_DOOR_MOTOR_OPENING = 40
    ENTRY_DOOR_MOTOR_CLOSING = 36
    ENTRY_DOOR_MOTOR_OPENING = 32
