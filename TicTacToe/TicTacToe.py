import sys
import time
from GameLogger.GameLogger import GameLogger


class TicTacToe:

    """Class for creation of instances of TicTacToe game."""

    def __init__(self, size, signs, menu_description, menu_options):
        self.menu_description = menu_description
        # list of options
        self.menu_options = menu_options
        # e.g. X/O
        self.game_signs = signs
        # game board will be size*size
        self.size = size
        self.GameLog = GameLogger()
        # list to store temp logs
        self.log_j = []
        print(f"Hello and welcome to the {size}x{size} TicTacToe game!")
        self.select_menu()

    # create a board size*size as a nested list
    def create_board(self):
        self.board = [list(range(1 + self.size * i, 1 + self.size * (i + 1))) for i in range(self.size)]
        return self.board

    # visualize a board in console
    def visualize(self):
        for row in self.board:
            print('\t _________')
            print(f'\t {" | ".join(str(x) for x in row)}')
        print('\t _________')

    # validate any input value with cross-check with allowed_options list
    @staticmethod
    def validate_input(user_input, allowed_options):
        user_input = TicTacToe.process_to_pattern(user_input)
        allowed_options = [i for i in allowed_options]
        while True:
            if user_input not in allowed_options:
                print(f'Sorry, it is not correct. Please try again.')
                user_input = TicTacToe.process_to_pattern(input())
                continue
            else:
                print('Thanks!')
                break
        return user_input

    def select_menu(self):
        menu_choice = TicTacToe.process_to_pattern(input(f'Here is our menu. Please make your choice. '
                                                         f'Available options: \n{self.menu_description}\n'))
        menu_choice = TicTacToe.validate_input(menu_choice, self.menu_options)
        if menu_choice == self.menu_options[0]:
            self.set_players_names()
            self.round = 1
            self.play()
        elif menu_choice == self.menu_options[1]:
            print('Loading log file.')
            time.sleep(1)
            self.GameLog.show_logs()
            time.sleep(2)
            self.select_menu()
        elif menu_choice == self.menu_options[2]:
            self.GameLog.clean_logs()
            print('Log file is empty now. Loading menu.')
            time.sleep(3)
            self.select_menu()
        elif menu_choice == self.menu_options[3]:
            sys.exit('Sorry to see you go...We will wait back for you!')

    # set players' names
    def set_players_names(self):
        self.first_player = str(input('Please enter a name of the first player: '))
        self.second_player = str(input('Please enter a name of the second player: '))

    def who_goes_first(self):
        order_choice = TicTacToe.process_to_pattern(input(f'Will {self.first_player} play '
                                                          f'{self.game_signs[0]}? (Y/N): '))
        if order_choice == 'y':
            self.players_order = {self.game_signs[0]: self.first_player, self.game_signs[1]: self.second_player}
        elif order_choice == 'n':
            self.players_order = {self.game_signs[0]: self.second_player, self.game_signs[1]: self.first_player}
        else:
            print('Incorrect input, please try again.')
            self.who_goes_first()
        return self.players_order

    # check rows, returns winner value or 0 in case of absence of match:
    @staticmethod
    def check_rows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return 0

    # check diagonals, returns winner value or 0 in case of absence of match:
    @staticmethod
    def check_diagonals(board):
        for _ in board:
            if len(set([row[i] for i, row in enumerate(board)])) == 1:
                return board[0][0]
            elif len(set([row[-i - 1] for i, row in enumerate(board)])) == 1:
                return board[0][len(board) - 1]
            else:
                return 0

    # returns true if value in lst_to_check exists in nested_list
    @staticmethod
    def check_if_exists(nested_list, lst_to_check):
        if any(i in lst for lst in nested_list for i in lst_to_check):
            return True

    # method to tranform the value to string, strip it, and make all the letters low
    @staticmethod
    def process_to_pattern(value):
        return str(value).strip().lower()

    def check_winner(self):
        # getting transposed list to check both rows and columns
        for board_matrix in [self.board, list(map(list, zip(*self.board)))]:
            result = TicTacToe.check_rows(board_matrix)
            if result:
                return result
        return TicTacToe.check_diagonals(self.board)

    def play(self):
        self.who_goes_first()
        self.create_board()
        turn = self.game_signs[0]
        while True:
            print(f'{self.players_order[turn]}\'s turn now.')
            self.visualize()
            dynamic_board = [TicTacToe.process_to_pattern(i) for row in self.board for i in row if
                             i not in self.game_signs]
            user_move = TicTacToe.validate_input(input(f'{self.players_order[turn]}, '
                                                       f'please make a choice and submit a number from the list: '
                                                       f'{" ".join(dynamic_board)}: '), dynamic_board)
            # change the board to contain user's choice
            self.board = [[turn if str(i) == user_move else i for i in row] for row in self.board]
            if self.check_winner() == turn:
                print(f'Congratulations! {self.players_order[turn]} wins!')
                self.log_j.append([self.round, self.players_order[turn]])
                break
            # checking for a possibility of draw
            elif self.check_winner() == 0 and not TicTacToe.check_if_exists(self.board, range(1, self.size ** 2 + 1)):
                print(f'We have a tie!')
                self.log_j.append([self.round, 'Friendship'])
                break
            turn = self.game_signs[1] if turn == self.game_signs[0] else self.game_signs[0]
        self.visualize()
        if self.game_in_rounds():
            self.round += 1
            self.play()
        else:
            if self.round == 1:
                self.GameLog.add_log_msg(f'One-time game. {self.log_j[0][1]} won.')
            else:
                print('Below is your round game statistics:\n')
                for i in self.log_j:
                    print(f'Round game: Round {i[0]}: {i[1]} won.\n')
                    self.GameLog.add_log_msg(f'Round game: Round {i[0]}: {i[1]} won.')
            self.log_j.clear()
            self.select_menu()

    @staticmethod
    def game_in_rounds():
        while True:
            accept_rounds = TicTacToe.process_to_pattern(input('Would you like to play one more round? (Y/N):'))
            if accept_rounds == 'y':
                return True
            elif accept_rounds == 'n':
                return False
            else:
                print('Incorrect input. Please choose either Y or N.')
