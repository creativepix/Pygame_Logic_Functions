import sqlite3
from typing import Dict, Tuple, List
from source_code.errors.block_error import BlockError


def get_connection_cmd_line(
        input_connection: int, all_connnections: Dict[int, int],
        all_blocks: Dict[Tuple[List[int], List[int]], Tuple[str, str]],
        output_connections: List[int], cur: sqlite3.Cursor = None) -> str:
    if cur is None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()

    additional_args = [all_connnections, all_blocks, output_connections, cur]

    for out, inps in all_connnections.items():
        if input_connection in inps:
            for (out_cons, inp_cons), name in all_blocks.items():
                if out in out_cons:
                    if name[0] == 'InputBlock':
                        return f'input_blocks[' \
                               f'{output_connections.index(out)}]'
                    elif name[0] == 'AndBlock':
                        arg1 = get_connection_cmd_line(
                            inp_cons[0], *additional_args)
                        arg2 = get_connection_cmd_line(
                            inp_cons[1], *additional_args)
                        return f'({arg1} and {arg2})'
                    elif name[0] == 'OrBlock':
                        arg1 = get_connection_cmd_line(
                            inp_cons[0], *additional_args)
                        arg2 = get_connection_cmd_line(
                            inp_cons[1], *additional_args)
                        return f'({arg1} or {arg2})'
                    elif name[0] == 'NotBlock':
                        arg = get_connection_cmd_line(
                            inp_cons[0], *additional_args)
                        return f'not {arg}'
                    elif name[0] == 'CustomBlock':
                        structure = cur.execute(
                            f'SELECT STRUCTURE FROM ALL_CUSTOM_BLOCKS '
                            f'WHERE BLOCK_NAME="{name[1]}"').fetchall()
                        if any(structure):
                            structure = structure[0][0]
                        else:
                            raise BlockError
                        custom_block_cmd_lines = \
                            get_cmd_line_from_structure(structure, cur)
                        custom_block_cmd_line = custom_block_cmd_lines. \
                            split('\n')[out_cons.index(out)]
                        for inp_con_id, inp_con in enumerate(inp_cons):
                            to_replace = get_connection_cmd_line(
                                inp_cons[inp_con_id], *additional_args)
                            custom_block_cmd_line = \
                                custom_block_cmd_line.replace(
                                    f'input_blocks[{inp_con_id}]', to_replace)
                        return custom_block_cmd_line
                    else:
                        raise BlockError
            raise BlockError
    return 'False'


def get_cmd_line_from_structure(structure_line: str,
                                cur: sqlite3.Cursor = None) -> str:
    if not any(structure_line):
        return 'True'

    def check_digit(elem: str):
        return int(elem) if elem.isdigit() else None

    all_connnections = dict()
    all_blocks = dict()
    input_connections = []
    output_connections = []
    for block in structure_line.split('|'):
        block_class = block.split('(')[0]
        block_name = block.split('(')[1].split(',')[0]

        connections = ''.join(block[:-1].split('>,')[1:])

        all_inp_cons = []
        all_out_cons = []

        for input_con in (connections.split('InputConnection(')[1:]):
            input_con = input_con.split('))')[0]
            input_con_id = int(input_con.split(',')[0])
            all_inp_cons.append(input_con_id)

        if 'OutputConnection(' not in connections:
            if block_class != 'OutputBlock':
                raise BlockError
            else:
                input_connections.append(all_inp_cons[0])
        else:
            for output_con in (connections.split('OutputConnection(')[1:]):
                output_con = output_con.split('))')[0]
                output_con_id = int(output_con.split(',')[0])
                all_connnections[output_con_id] = \
                    [check_digit(num) for num in
                     output_con.split('[')[1].split(']')[0].split(', ')]
                all_out_cons.append(output_con_id)

        if 'InputConnection(' not in connections:
            if block_class == 'InputBlock':
                output_connections.append(all_out_cons[0])

        all_blocks[(tuple(all_out_cons), tuple(all_inp_cons))] = \
            (block_class, block_name)

    cmd_lines = ''
    for input_connection in input_connections:
        cmd_lines += get_connection_cmd_line(
            input_connection, all_connnections, all_blocks,
            output_connections, cur)
        cmd_lines += '\n'
    return cmd_lines.strip('\n')
