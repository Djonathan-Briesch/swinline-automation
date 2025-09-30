from datetime import datetime


class SowFeedingSession:
    """
    Representa a sessão de alimentação de um suíno.

    A classe controla os dados da sessão atual, incluindo:
    - Identificação do confinamento e do suíno
    - Limite diário de alimentação e consumo
    - Datas de entrada e saída do alimentador

    Regras:
    - Atributos essenciais só podem ser definidos uma vez.
    - O consumo diário só pode ser alterado através do método `add_consumed` e
      não pode ultrapassar o limite diário.
    """

    def __init__(self):
        """Inicializa todos os atributos da sessão como None ou zero."""
        self.__confinement_id: int | None = None
        self.__sow_rfid: str | None = None
        self.__ear_tag_number: int | None = None
        self.__daily_feed_limit: int | None = None
        self.__entry_date_time: datetime | None = None
        self.__exit_date_time: datetime | None = None
        self.__daily_feed_consumed: int = 0

    # ---------------- confinement_id ----------------
    @property
    def confinement_id(self) -> int | None:
        """Retorna o ID do confinamento."""
        return self.__confinement_id

    @confinement_id.setter
    def confinement_id(self, value: int):
        """
        Define o ID do confinamento (somente uma vez).

        Args:
            value (int): ID do confinamento.

        Raises:
            AttributeError: se já estiver definido.
            TypeError: se value não for int.
        """
        if self.__confinement_id is not None:
            raise AttributeError(
                "Confinement ID já foi definido e não pode ser alterado"
            )
        if not isinstance(value, int):
            raise TypeError("Confinement ID deve ser um número inteiro")
        self.__confinement_id = value

    # ---------------- sow_rfid ----------------
    @property
    def sow_rfid(self) -> str | None:
        """Retorna o RFID do suíno."""
        return self.__sow_rfid

    @sow_rfid.setter
    def sow_rfid(self, value: str):
        """
        Define o RFID do suíno (somente uma vez).

        Args:
            value (str): RFID entre 5 e 25 caracteres.

        Raises:
            AttributeError: se já estiver definido.
            ValueError: se o valor não tiver o tamanho correto.
            TypeError: se value não for string.
        """
        if self.__sow_rfid is not None:
            raise AttributeError("Sow RFID já foi definido e não pode ser alterado")
        if not isinstance(value, str) or not (5 <= len(value) <= 25):
            raise ValueError("Sow RFID deve ser uma string entre 5 e 25 caracteres")
        self.__sow_rfid = value

    # ---------------- ear_tag_number ----------------
    @property
    def ear_tag_number(self) -> int | None:
        """Retorna o número do brinco do suíno."""
        return self.__ear_tag_number

    @ear_tag_number.setter
    def ear_tag_number(self, value: int):
        """
        Define o número do brinco do suíno (somente uma vez).

        Args:
            value (int): número do brinco.

        Raises:
            AttributeError: se já estiver definido.
            TypeError: se value não for int.
        """
        if self.__ear_tag_number is not None:
            raise AttributeError(
                "Ear tag number já foi definido e não pode ser alterado"
            )
        if not isinstance(value, int):
            raise TypeError("Ear tag number deve ser um número inteiro")
        self.__ear_tag_number = value

    # ---------------- daily_feed_limit ----------------
    @property
    def daily_feed_limit(self) -> int | None:
        """Retorna o limite diário de alimento em gramas."""
        return self.__daily_feed_limit

    @daily_feed_limit.setter
    def daily_feed_limit(self, value: int):
        """
        Define o limite diário de alimento (somente uma vez).

        Args:
            value (int): quantidade máxima de alimento em gramas.

        Raises:
            AttributeError: se já estiver definido.
            TypeError: se value não for int.
            ValueError: se value for negativo.
        """
        if self.__daily_feed_limit is not None:
            raise AttributeError(
                "Daily feed limit já foi definido e não pode ser alterado"
            )
        if not isinstance(value, int):
            raise TypeError("Daily feed limit deve ser um número inteiro")
        if value < 0:
            raise ValueError("Daily feed limit não pode ser negativo")
        self.__daily_feed_limit = value

    # ---------------- entry_date_time ----------------
    @property
    def entry_date_time(self) -> datetime | None:
        """Retorna a data/hora de entrada do suíno no alimentador."""
        return self.__entry_date_time

    @entry_date_time.setter
    def entry_date_time(self, value: datetime):
        """
        Define a data/hora de entrada do suíno (somente uma vez).

        Args:
            value (datetime): data futura de entrada.

        Raises:
            AttributeError: se já estiver definido.
            TypeError: se value não for datetime.
        """
        if self.__entry_date_time is not None:
            raise AttributeError("Entry date já foi definido e não pode ser alterado")
        if not isinstance(value, datetime):
            raise TypeError("Entry date deve ser um objeto datetime")
        self.__entry_date_time = value

    # ---------------- exit_date_time ----------------
    @property
    def exit_date_time(self) -> datetime | None:
        """Retorna a data/hora de saída do suíno do alimentador."""
        return self.__exit_date_time

    @exit_date_time.setter
    def exit_date_time(self, value: datetime):
        """
        Define a data/hora de saída do suíno (somente uma vez).

        Args:
            value (datetime): data/hora de saída.

        Raises:
            AttributeError: se já estiver definido.
            TypeError: se value não for datetime.
            ValueError: se value for anterior à entrada.
        """
        if self.__exit_date_time is not None:
            raise AttributeError("Exit date já foi definido e não pode ser alterado")
        if not isinstance(value, datetime):
            raise TypeError("Exit date deve ser um objeto datetime")
        if self.__entry_date_time and value < self.__entry_date_time:
            raise ValueError("Exit date não pode ser anterior à entry date")
        self.__exit_date_time = value

    # ---------------- daily_feed_consumed ----------------
    @property
    def daily_feed_consumed(self) -> int:
        """Retorna a quantidade de alimento consumida em gramas."""
        return self.__daily_feed_consumed

    # ---------------- método único para alterar consumo ----------------
    def add_consumed(self, amount: int):
        """
        Adiciona alimento consumido (em gramas) à sessão, validando o limite diário.

        Args:
            amount (int): quantidade de alimento a adicionar.

        Raises:
            TypeError: se amount não for inteiro.
            ValueError: se o consumo acumulado ultrapassar o limite diário.
        """
        if not isinstance(amount, int):
            raise TypeError("Amount deve ser um número inteiro")
        if (
            self.__daily_feed_limit is not None
            and (self.__daily_feed_consumed + amount) > self.__daily_feed_limit
        ):
            raise ValueError("Consumo acumulado excede o daily feed limit")
        self.__daily_feed_consumed += amount
