import sys

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    if all(cell != "" for row in board for cell in row):
        return "draw"
    return None


def bot_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if empty_cells:
        import random
        return random.choice(empty_cells)
    return None


class MockState:
    def __init__(self):
        self.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        self.current_player = "O"
        self.game_over = True
        self.winner = "X"
        self.scores = {"X": 5, "O": 3, "draw": 2}
        self.board_key = 10


def reset_game(state):
    state.board = [["" for _ in range(3)] for _ in range(3)]
    state.current_player = "X"
    state.game_over = False
    state.winner = None
    state.board_key += 1


def run_tests():
    tests_passed = 0
    tests_failed = 0
    
    tests = [
        ("check_winner horizontal X", lambda: check_winner([["X", "X", "X"], ["", "", ""], ["", "", ""]]) == "X"),
        ("check_winner horizontal O", lambda: check_winner([["", "", ""], ["O", "O", "O"], ["", "", ""]]) == "O"),
        ("check_winner vertical X", lambda: check_winner([["X", "", ""], ["X", "", ""], ["X", "", ""]]) == "X"),
        ("check_winner vertical O", lambda: check_winner([["", "O", ""], ["", "O", ""], ["", "O", ""]]) == "O"),
        ("check_winner diagonal X", lambda: check_winner([["X", "", ""], ["", "X", ""], ["", "", "X"]]) == "X"),
        ("check_winner diagonal O", lambda: check_winner([["", "", "O"], ["", "O", ""], ["O", "", ""]]) == "O"),
        ("check_winner draw", lambda: check_winner([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == "draw"),
        ("check_winner incomplete", lambda: check_winner([["X", "", ""], ["", "", ""], ["", "", ""]]) is None),
        ("bot_move returns empty cell", lambda: bot_move([["X", "", ""], ["", "O", ""], ["", "", ""]]) in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]),
        ("bot_move no empty cells", lambda: bot_move([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) is None),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"PASS: {name}")
                tests_passed += 1
            else:
                print(f"FAIL: {name}")
                tests_failed += 1
        except Exception as e:
            print(f"FAIL: {name} - {e}")
            tests_failed += 1
    
    print(f"\nTotal: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
