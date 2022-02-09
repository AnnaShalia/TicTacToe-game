from TicTacToe.TicTacToe import TicTacToe

# input data
data = {
    'menu': {
        'options': ['start', 'log', 'clean', 'exit'],
        'description': 'start - start new game;\n'
                       'log - view log file;\n'
                       'clean - clean logs;\n'
                       'exit - exit game.'
    },
    'game': {
        'options': ['x', 'O']
    }
}


def main():
    # setting the params and calling function
    TicTacToe(3, data['game']['options'], data['menu']['description'], data['menu']['options'])


if __name__ == '__main__':
    main()
