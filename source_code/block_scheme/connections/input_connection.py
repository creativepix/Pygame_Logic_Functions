from source_code import global_vars
from source_code.block_scheme.connections.base_connection import BaseConnection
from source_code.block_scheme.connections.builder_base_connection import \
    BuilderBaseConnection


class InputConnection(BaseConnection):
    def attach(self, to_connection: BuilderBaseConnection) -> None:
        from source_code.block_scheme.connections.output_connection import \
            OutputConnection

        if isinstance(to_connection, OutputConnection):
            while len(self.attached_connections) > 0:
                self.detach(self.attached_connections[0])

            my_outputs = self.parent_block.outputs

            def check_inputs(connection: BaseConnection):
                for con in connection.parent_block.inputs:
                    for attached_con in con.attached_connections:
                        if attached_con in my_outputs or \
                                check_inputs(attached_con):
                            return True
                return False

            if check_inputs(to_connection):
                global_vars.ACTIVE_WINDOW.show_message(
                    'Do you want to make a max recursion error?')
                return

            self.signal = to_connection.signal
            self.attached_connections.append(to_connection)
            to_connection.attached_connections.append(self)

    def detach(self, connection: BuilderBaseConnection) -> None:
        super().detach(connection)
        self.signal = False

    @property
    def attached_connection(self):
        return self.attached_connections[0]

    @attached_connection.setter
    def attached_connection(self, value: BuilderBaseConnection):
        self.attach(value)

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('InputConnection')

    def __copy__(self):
        return InputConnection(self.base_game_window, self.parent_block,
                               self.local_coord_percents)