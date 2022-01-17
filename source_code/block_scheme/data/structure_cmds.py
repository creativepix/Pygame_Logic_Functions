import sqlite3
from typing import Dict, Tuple, List
from source_code.errors.block_error import BlockError
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.errors.no_output_block_error import NoOutputBlockError
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock


def get_connection_cmd_line(
        input_connection: int, all_connnections: Dict[int, int],
        all_blocks: Dict[Tuple[List[int], List[int]], Tuple[str, str]],
        output_connections: List[int], cur: sqlite3.Cursor) -> str:
    """метод по получению cmd линии по id-коннектора"""
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


def get_structure_from_blocks(all_blocks: List[BuilderBaseBlock])\
        -> (str, List[bool]):
    """получение структуры и инпут-сигналов из блоков"""
    inputs, structure = [], []
    for block in all_blocks:
        if isinstance(block, InputBlock):
            inputs.append(str(block.outputs[0].signal))
        structure.append(str(block))
    structure = '|'.join(structure).strip('|')
    return structure, inputs


def get_cmd_line_from_structure(structure_line: str,
                                cur_start: sqlite3.Cursor = None) -> str:
    """получение cmd линии по структурной линии"""
    if cur_start is None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
    else:
        cur = cur_start

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
                raise NoOutputBlockError
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

    if cur_start is None:
        con.close()

    return cmd_lines.strip('\n')


def custom_block_in_structure(structure: str, custom_block_name: str,
                              cur_start: sqlite3.Cursor = None)\
        -> bool:
    """определяет, есть ли название кастомного блока в структуре (нужно для
    того, чтобы убрать блоки из блок-листа в режиме песочницы, которые в
    совместности могут привести к ошибке максимальной рекурсии"""
    if cur_start is None:
        con = sqlite3.connect('./source_code/block_scheme/data/blocks.db')
        cur = con.cursor()
    else:
        cur = cur_start

    if 'CustomBlock(' not in structure:
        return False
    if f'CustomBlock({custom_block_name}' in structure:
        return True

    for custom_block in structure.split('CustomBlock(')[1:]:
        block_name = custom_block.split(',')[0]
        structure = cur.execute(
                f'SELECT STRUCTURE FROM ALL_CUSTOM_BLOCKS '
                f'WHERE BLOCK_NAME = "{block_name}"').fetchall()[0][0]
        ans = custom_block_in_structure(structure, custom_block_name, cur)
        if ans:
            return True

    if cur_start is None:
        con.close()

    return False
