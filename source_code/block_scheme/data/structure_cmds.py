import sqlite3

from source_code.block_scheme.blocks.and_block import AndBlock
#from source_code.block_scheme.blocks.custom_block import CustomBlock
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.or_block import OrBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.block_scheme.connections.base_connection import BaseConnection
from source_code.errors.block_error import BlockError
from source_code.windows.base_game_window import BaseGameWindow


def get_cmd_line_from_structure(structure_line: str,
                                cursor: sqlite3.Cursor = None) -> str:
    if not any(structure_line):
        return 'True'

    if cursor is None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cursor = con.cursor()

    def check_digit(elem: str):
        return int(elem) if elem.isdigit() else None

    all_connnections = dict()
    all_blocks = dict()
    outputs = []
    for block in structure_line.split('|'):
        block_name = block.split('(')[0]
        connections = ''.join(block[:-1].split('>,')[1:])

        all_inp_cons = []

        for inp_con in (connections.split('InputConnection(')[1:]):
            inp_con = inp_con.split('))')[0]
            all_connnections[int(inp_con.split(',')[0])] = \
                [check_digit(num) for num in
                 inp_con.split('[')[1].split(']')[0].split(',')]
            all_inp_cons.append(int(inp_con.split(',')[0]))

        if 'OutputConnection(' not in connections:
            if block_name != 'OutputBlock':
                raise BlockError
            else:
                if len(all_inp_cons) != 1:
                    raise BlockError
                outputs.append(all_inp_cons[0])
        else:
            output_con = connections.split('OutputConnection(')[1].split('))')[0]
            all_connnections[int(output_con.split(',')[0])] = \
                [check_digit(num) for num in
                 output_con.split('[')[1].split(']')[0].split(',')]
            if output_con is None:
                raise BlockError
            all_blocks[(output_con, tuple(all_inp_cons))] = block_name


#    def get_my_cmd_line(output_connection: int) -> str:
#        for inp, out in all_connnections.items():
#            if out == output_connection:
#                for (out_con, inp_cons), name in all_blocks.items():
#
#                raise BlockError
#        raise BlockError
#
#    for output in outputs:
#        print(get_my_cmd_line(output))
    print()
    return ''
#    cmd_line = f'[{", ".join([])}]\n'
#
#    outputs = [ for block in  if block.startswith('OutputBlock(')]
#
#    for out_b_id in range(len(output_blocks)):
#        cmd_line += f'\noutputs[{out_b_id}] = '
#
#        def get_my_line(attached_connection: BaseConnection):
#            if attached_connection is None:
#                return '(True)'
#            block = attached_connection.parent_block
#            if isinstance(block, InputBlock):
#                return f'(inputs[{input_blocks.index(block)}])'
#            if isinstance(block, NotBlock):
#                got_line = get_my_line(block.inputs[0].attached_connection)
#                return f'(not {got_line})'
#            if isinstance(block, AndBlock):
#                got_line1 = get_my_line(block.inputs[0].attached_connection)
#                got_line2 = get_my_line(block.inputs[1].attached_connection)
#                return f'({got_line1} and {got_line2})'
#            if isinstance(block, OrBlock):
#                got_line1 = get_my_line(block.inputs[0].attached_connection)
#                got_line2 = get_my_line(block.inputs[1].attached_connection)
#                return f'({got_line1} or {got_line2})'
#            if isinstance(block, CustomBlock):
#                needed_id = block.outputs.index(attached_connection)
#                # for line in block.command_line.split('\n'):
#                #     if line.startswith(f'outputs[{needed_id}] = '):
#                #         needed_line = \
#                #             line.replace(f'outputs[{needed_id}] = ', '')
#                #         for con_id, input_connection in \
#                #                 enumerate(block.inputs):
#                #             needed_line = needed_line.replace(
#                #                 f'inputs[{con_id}]',
#                #                 get_my_line(
#                #                     input_connection.attached_connection
#                #                 ).strip(')').strip('(')
#                #             )
#                #         return needed_line
#                # raise BlockError
#            if not any(block.inputs[0].attached_connections):
#                raise BlockError
#            return get_my_line(block.inputs[0].attached_connection)
#
#        cmd_line += get_my_line(output_blocks[out_b_id].inputs[0])
#    return cmd_line
