def visualize_graph(G, label=0):
    text = ''
    text += '     '
    for j in range(len(G[0])):
        cl = label + j if isinstance(label, int) else chr(ord(label)+j)
        text += f'{cl:^4}'
    text += '\n     '
    
    for j in range(len(G[0])):
        text += '----'
    text += '\n'

    for i in range(len(G[0])):
        rl = label + i if isinstance(label, int) else chr(ord(label)+i)
        text += f'{rl:^4}|'
        for j in range(len(G[0])):
            text += f'{G[i][j]:^4}'
        text += '\n'
    return text

def visualize_partition(pi, label=0):
    viz = []
    for cell in pi:
        cviz = []
        for v in cell:
            l = label + v if isinstance(label, int) else chr(ord(label)+v)
            cviz.append(l)
        viz.append(cviz)

    s = ''
    for cell in viz:
        if isinstance(label, int):
            s += f'{cell}, '
        else:
            s += '[' + ', '.join(cell) + '], '
    s = s[:-2]
    return f'[{s}]'


def visualize_vertex(v, label=0):
    if v is None:
        return '-'
    return label + v if isinstance(label, int) else chr(ord(label)+v)

def visualize_path(path, label=0):
    s = ''
    for p in path:
        s += label + p if isinstance(label, int) else chr(ord(label)+p) + ', '

    s = s[:-2]
    return f'[{s}]'