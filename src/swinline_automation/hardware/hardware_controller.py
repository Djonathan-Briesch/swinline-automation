import RPi.GPIO as GPIO
import serial
import time

from swinline_automation.hardware.constants.hardware_pins import HardwarePins

class HardwareController:
    """
    Classe para encapsular o controle do hardware do sistema.

    Responsável por:
    - Controle de motores das portas de entrada e separação
    - Controle do alimentador
    - Leitura de sensores (Infravermelho e limit switches)
    - Leitura de tags RFID via serial
    """

    def __init__(self, motor_feed_on_time: int, serial_port: str = "/dev/serial0", baudrate: int = 115200):
        """
        Inicializa o hardware, configura os pinos GPIO e a porta serial.

        Args:
            motor_feed_on_time (int): Tempo em segundos em que o motor de alimentação fica ligado 
            serial_port (str): Porta serial para comunicação com a antena RFID.
            baudrate (int): Velocidade de comunicação serial.
        """
        # Configuração GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Setup dos pinos
        GPIO.setup(HardwarePins.INFRARED_PRESENCE_SENSOR, GPIO.IN)
        GPIO.setup(HardwarePins.FEEDER_MOTOR, GPIO.OUT)

        GPIO.setup(HardwarePins.ENTRY_DOOR_LIMIT_SWITCH_CLOSED, GPIO.IN)
        GPIO.setup(HardwarePins.ENTRY_DOOR_LIMIT_SWITCH_OPEN, GPIO.IN)
        GPIO.setup(HardwarePins.ENTRY_DOOR_MOTOR_OPENING, GPIO.OUT)
        GPIO.setup(HardwarePins.ENTRY_DOOR_MOTOR_CLOSING, GPIO.OUT)

        GPIO.setup(HardwarePins.SEPARATION_DOOR_LIMIT_SWITCH_CLOSED, GPIO.IN)
        GPIO.setup(HardwarePins.SEPARATION_DOOR_LIMIT_SWITCH_OPEN, GPIO.IN)
        GPIO.setup(HardwarePins.SEPARATION_DOOR_MOTOR_OPENING, GPIO.OUT)
        GPIO.setup(HardwarePins.SEPARATION_DOOR_MOTOR_CLOSING, GPIO.OUT)

        # Inicializa o serial
        self.__serial = serial.Serial(serial_port, baudrate)

        # Estado inicial: todos os motores desligados
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_CLOSING, 0)
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_CLOSING, 0)
        GPIO.output(HardwarePins.FEEDER_MOTOR, 0)


        # Variaveis auxiliares para controlar o motor de alimentação
        self.__motor_feed_on_time = motor_feed_on_time
        self.__feeder_motor_start_time = None
        self.__feeder_motor_is_on = False

    # -------------------- Alimentador --------------------

    def dispense_feed(self) -> None:
        """
        Liga o motor do alimentador para despejar ração.

        - Liga o motor se não estiver ligado.
        - Desliga automaticamente quando passar o tempo configurado.

        """
        if not self.__feeder_motor_is_on:
            GPIO.output(HardwarePins.FEEDER_MOTOR, 1)
            self.__feeder_motor_start_time = time.time()
            self.__feeder_motor_is_on = True
        else:
            if time.time() - self.__feeder_motor_start_time >= self.__motor_feed_on_time:
                GPIO.output(HardwarePins.FEEDER_MOTOR, 0)
                self.__feeder_motor_start_time = None
                self.__feeder_motor_is_on = False
                
    # -------------------- Porta de entrada --------------------

    def open_entry_door(self) -> None:
        """Aciona o motor para abrir a porta de entrada."""
        if self.__is_entry_door_open():
            self.__stop_entry_door()
            return
        
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_OPENING, 1)
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_CLOSING, 0)

    def close_entry_door(self) -> None:
        """Aciona o motor para fechar a porta de entrada."""
        if self.__is_entry_door_closed():
            self.__stop_entry_door()
            return
        
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_CLOSING, 1)

    def __stop_entry_door(self) -> None:
        """Para o motor da porta de entrada."""
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.ENTRY_DOOR_MOTOR_CLOSING, 0)

    def __is_entry_door_open(self) -> bool:
        """Retorna True se o limit switch indicar que a porta de entrada está aberta."""
        return GPIO.input(HardwarePins.ENTRY_DOOR_LIMIT_SWITCH_OPEN) == 1

    def __is_entry_door_closed(self) -> bool:
        """Retorna True se o limit switch indicar que a porta de entrada está fechada."""
        return GPIO.input(HardwarePins.ENTRY_DOOR_LIMIT_SWITCH_CLOSED) == 1

    # -------------------- Porta de separação --------------------

    def open_separation_door(self) -> None:
        """Aciona o motor para abrir a porta de separação."""
        if self.__is_separation_door_open():
            self.__stop_separation_door()
            return

        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_OPENING, 1)
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_CLOSING, 0)

    def close_separation_door(self) -> None:
        """Aciona o motor para fechar a porta de separação."""
        if self.__is_separation_door_closed():
            self.__stop_separation_door()
            return

        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_CLOSING, 1)

    def __stop_separation_door(self) -> None:
        """Para o motor da porta de separação."""
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_OPENING, 0)
        GPIO.output(HardwarePins.SEPARATION_DOOR_MOTOR_CLOSING, 0)

    def __is_separation_door_open(self) -> bool:
        """Retorna True se o limit switch indicar que a porta de separação está aberta."""
        return GPIO.input(HardwarePins.SEPARATION_DOOR_LIMIT_SWITCH_OPEN) == 1

    def __is_separation_door_closed(self) -> bool:
        """Retorna True se o limit switch indicar que a porta de separação está fechada."""
        return GPIO.input(HardwarePins.SEPARATION_DOOR_LIMIT_SWITCH_CLOSED) == 1

    # -------------------- Sensores --------------------

    def read_infrared_presence(self) -> bool:
        """Retorna True se o sensor PIR detectar presença."""
        return GPIO.input(HardwarePins.INFRARED_PRESENCE_SENSOR) == 1

    def read_serial_rfid(self) -> str | None:
        """
        Lê uma tag RFID enviada via serial.

        Returns:
            str | None: Tag lida, ou None se não houver dados disponíveis.
        """
        if self.__serial.in_waiting > 0:
            return self.__serial.readline().decode("utf-8").rstrip()
        return None