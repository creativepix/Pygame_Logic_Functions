def split_line(line: str, max_symbols: int):
    new_lines = [[]]
    for i, elem in enumerate(line):
        new_lines[-1].append(elem)
        if elem == ' ':
            try:
                if len(new_lines[-1]) + (line.index(' ', i + 1) - i) > \
                        max_symbols:
                    new_lines[-1] = ''.join(new_lines[-1])
                    new_lines.append([])
            except ValueError:
                new_lines[-1].append(line[i + 1:])
                new_lines[-1] = ''.join(new_lines[-1])
                break
    return new_lines
