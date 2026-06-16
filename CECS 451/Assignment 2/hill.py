import board
import time


board_size = 5


def main():
    start = time.time()
    game = board.Board(board_size)

    # while a solution has not been found
    while game.get_fitness() > 0:
        # random starting point
        game = board.Board(board_size)

        # hill-climbing iteration
        distance_factor = 1  # number of spaces to move while checking
        current = ''

        # checks if a move was made last round and the search area has not been expanded as much as possible
        while game.encode() != current and distance_factor <= board_size:
            options = []  # array of possible moves
            current = game.encode()  # string of current game state

            # building potential move list
            for i in range(len(current)):
                if int(current[i]) - distance_factor >= 0:
                    options.append(current[:i] + str(int(current[i]) - distance_factor) + current[i+1:])
                if int(current[i]) + distance_factor < board_size:
                    options.append(current[:i] + str(int(current[i]) + distance_factor) + current[i+1:])

            # converting to games and checking fitness
            temp = board.Board(board_size)
            for i in range(len(options)):
                temp.decode(options[i])
                if temp.get_fitness() < game.get_fitness():
                    game.decode(temp.encode())
                    distance_factor = 1

            # if the best move is not to move
            if game.encode() == current:
                # widen search area (for escaping local minima)
                distance_factor += 1

    print(f'Running time: {int((time.time() - start) * 1000)}ms')
    game.print_map()


if __name__ == '__main__':
    main()
