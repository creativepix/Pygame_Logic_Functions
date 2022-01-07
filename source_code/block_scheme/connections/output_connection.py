from typing import Tuple
from source_code.block_scheme.connections.base_connection import BaseConnection
from source_code.block_scheme.connections.builder_base_connection import \
    BuilderBaseConnection


class OutputConnection(BaseConnection):
    def attach(self, to_connection: BuilderBaseConnection) -> None:
        from source_code.block_scheme.connections.input_connection import \
            InputConnection

        if isinstance(to_connection, InputConnection):
            for attached_connection in to_connection.attached_connections:
                to_connection.detach(attached_connection)
            self.attached_connections.append(to_connection)
            to_connection.attached_connections.append(self)
            to_connection.signal = self.signal

    def detach(self, connection: BuilderBaseConnection) -> None:
        super().detach(connection)
        connection.signal = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('OutputConnection')

    def __copy__(self):
        return OutputConnection(self.base_game_window, self.parent_block,
                                self.local_coord_percents)
