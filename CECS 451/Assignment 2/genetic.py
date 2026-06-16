import board
import time
import random

board_size = 5
batch_size = 8  # must be even
assert batch_size % 2 == 0


def weighted_prob(p_array: list):
    # normalize values
    s = sum(i for i in p_array)
    p_array = [i / s for i in p_array]

    # random choice
    r = random.random()
    for i in range(len(p_array)):
        if r < p_array[i]:
            return i
        else:
            r -= p_array[i]


def main():
    start = time.time()
    states = []
    for i in range(batch_size):
        states.append(board.Board(board_size))
    best_game = states[0]

    # while a solution has not been found
    while best_game.get_fitness() > 0:
        # selection
        probabilities = [i.get_fitness() for i in states]
        new_states = []
        for i in range(batch_size):
            new_states.append(states[weighted_prob(probabilities)].encode())

        states = new_states
        new_states = [i for i in states]

        # crossover
        for i in range(len(states) // 2, len(states)):
            partner = i - (len(new_states) // 2)
            split = random.randint(1, board_size - 2)
            new_states[i] = states[i][:split] + states[partner][split:]
            new_states[partner] = states[partner][:split] + states[i][split:]

        states = new_states
        new_states = []

        # mutation
        for entry in states:
            # states will have a 50/50 chance to mutate one randomly chosen value
            index = random.randint(0, (board_size * 2) - 1)
            if index < board_size:
                new_states.append(entry[:index] + str(random.randint(0, board_size - 1)) + entry[index + 1:])
            else:
                new_states.append(entry)

        temp = board.Board(board_size)
        for i in range(len(new_states)):
            temp.decode(new_states[i])
            # check for better states
            if temp.get_fitness() < best_game.get_fitness():
                best_game.decode(temp.encode())
            states[i] = temp

    print(f'Running time: {int((time.time() - start) * 1000)}ms')
    best_game.print_map()


if __name__ == '__main__':
    main()
