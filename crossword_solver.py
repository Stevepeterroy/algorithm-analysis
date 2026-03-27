# Crossword Puzzle Solver using Backtracking

grid = [
    ['-', '-', '-', '#', '-'],
    ['-', '#', '-', '-', '-'],
    ['-', '-', '#', '-', '-'],
    ['#', '-', '-', '-', '#'],
    ['-', '-', '-', '#', '-']
]

# words adjusted to match slot lengths
words = ["DOG", "CAT", "TREE", "BIRD", "FISH"]

slots = []
used_words = set()
output_log = []


def log(text):
    print(text)
    output_log.append(text)


def find_slots():
    rows = len(grid)
    cols = len(grid[0])

    # Horizontal slots
    for i in range(rows):
        j = 0
        while j < cols:
            start = j
            while j < cols and grid[i][j] != '#':
                j += 1
            length = j - start
            if length > 1:
                slots.append(("H", i, start, length))
            j += 1

    # Vertical slots
    for j in range(cols):
        i = 0
        while i < rows:
            start = i
            while i < rows and grid[i][j] != '#':
                i += 1
            length = i - start
            if length > 1:
                slots.append(("V", start, j, length))
            i += 1


def get_word_positions(slot):
    direction, r, c, length = slot
    positions = []

    for k in range(length):
        if direction == "H":
            positions.append((r, c + k))
        else:
            positions.append((r + k, c))

    return positions


def can_place(word, slot):

    if word in used_words:
        return False

    direction, r, c, length = slot

    if len(word) != length:
        return False

    positions = get_word_positions(slot)

    for i, (x, y) in enumerate(positions):
        if grid[x][y] != '-' and grid[x][y] != word[i]:
            return False

    return True


def place_word(word, slot):

    positions = get_word_positions(slot)

    for i, (x, y) in enumerate(positions):
        grid[x][y] = word[i]

    used_words.add(word)


def remove_word(word, slot):

    positions = get_word_positions(slot)

    for i, (x, y) in enumerate(positions):
        grid[x][y] = '-'

    used_words.remove(word)


def print_grid():

    for row in grid:
        line = " ".join(row)
        log(line)

    log("")


def solve(index=0):

    if index == len(slots):
        return True

    slot = slots[index]

    possible_words = [w for w in words if len(w) == slot[3]]

    log(f"\nSlot {index+1}: {slot}")
    log(f"Possible words: {possible_words}")

    for word in possible_words:

        if can_place(word, slot):

            log(f"Placing word: {word}")

            place_word(word, slot)

            print_grid()

            if solve(index + 1):
                return True

            log(f"Backtracking from word: {word}")

            remove_word(word, slot)

    return False


# MAIN
find_slots()

log("Number of slots identified: " + str(len(slots)))
log("Slots: " + str(slots))

solve()

log("\nFinal Crossword Grid:")

print_grid()

with open("crossword_solver_output.txt", "w") as f:

    for line in output_log:
        f.write(line + "\n")

print("\nOutput saved to crossword_solver_output.txt")