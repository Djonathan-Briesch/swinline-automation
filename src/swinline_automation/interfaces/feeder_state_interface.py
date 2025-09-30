from __future__ import annotations

from abc import ABC, abstractmethod


class FeederStateInterface(ABC):
    """
    Interface abstrata para os estados de uma máquina de alimentação.

    Cada estado deve implementar os métodos enter, exit e update.

    Attributes:
        allowed_transitions (list[type[FeederStateInterface]]):
            Classes de estados para os quais a transição é permitida.
    """

    allowed_transitions: list[type[FeederStateInterface]] = []

    @abstractmethod
    def enter(self) -> None:
        """
        Chamado automaticamente quando o estado é ativado.
        Inicializa qualquer configuração ou variável necessária para o estado.
        """
        pass

    @abstractmethod
    def exit(self) -> None:
        """
        Chamado automaticamente quando o estado é encerrado.
        Limpa ou finaliza qualquer configuração ou variável usada pelo estado.
        """
        pass

    @abstractmethod
    def update(self) -> None:
        """
        Chamado continuamente enquanto o estado está ativo.
        Executa a lógica periódica associada ao estado.
        """
        pass
