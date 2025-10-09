import random
import os

try:
    import msvcrt
    def getch():
        ch = msvcrt.getch().decode()
        if ch == '\xe0': 
            ch += msvcrt.getch().decode()
        return ch

except ImportError:
    import sys
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

SCORE_FILE = "scores.txt"

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r") as f:
            lines = [line.strip().split(",") for line in f.readlines() if line.strip()]
            scores = [(name, int(score)) for name, score in lines]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
    except (IOError, ValueError):
        return []

def save_score(name, score):
    scores = load_scores()
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:3]
    with open(SCORE_FILE, "w") as f:
        for n, s in scores:
            f.write(f"{n},{s}\n")

def show_leaderboard():
    scores = load_scores()
    print("\n🏆 TOP 3 HIGH SCORES 🏆")
    if not scores:
        print("No scores yet!")
    else:
        for i, (name, score) in enumerate(scores, 1):
            print(f"{i}. {name} - {score}")

def get_high_score():
    scores = load_scores()
    if scores:
        return scores[0]
    return ("None", 0)

class Game2048:
    def __init__(self):
        self.size = 4
        self.board = [[0]*self.size for _ in range(self.size)]
        self.score = 0
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(r,c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if not empty:
            return
        r,c = random.choice(empty)
        self.board[r][c] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0]*(self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size-1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            new_row = self.compress(merged)
            if new_row != row:
                moved = True
            new_board.append(new_row)
        self.board = new_board
        return moved

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def can_move(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
                if c+1 < self.size and self.board[r][c] == self.board[r][c+1]:
                    return True
                if r+1 < self.size and self.board[r][c] == self.board[r+1][c]:
                    return True
        return False

    def is_win(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def print_board(self):
        clear_screen()
        
        high_name, high_score = get_high_score()
        print(f"Score: {self.score}    🏅 High Score: {high_score} ({high_name})")
        print("-"*(self.size*6+1))
        for row in self.board:
            print("|", end="")
            for num in row:
                if num == 0:
                    print("     |", end="")
                else:
                    print(f"{num:^5}|", end="")
            print()
            print("-"*(self.size*6+1))
        print("\n🎮 CONTROLS:")
        print("→ Arrow Keys or WASD to move.")
        print("→ Press Q to quit anytime.\n")

    def show_instructions(self):
        clear_screen()
        print("🧩 HOW TO PLAY 2048 🧩\n")
        print("1️⃣ The game starts with two tiles having numbers 2 or 4.")
        print("2️⃣ Use arrow keys or W, A, S, D to move all tiles in one direction.")
        print("3️⃣ When two tiles with the same number touch, they combine into one.")
        print("   ➤ Example: 2 + 2 = 4, 4 + 4 = 8, 8 + 8 = 16 ... up to 2048!")
        print("4️⃣ Each merge increases your score.")
        print("5️⃣ The goal is to make the 2048 tile.")
        print("6️⃣ Game ends if there are no empty spaces and no valid moves left.")
        print("\n💡 Tip: Plan your moves carefully and try to keep larger numbers together!")
        print("\nPress Enter to start playing...")
        input()

    def play(self):
        clear_screen()
        print("Welcome to 2048 Game!\n")
        show_leaderboard()
        print("\nEnter your name:")
        player_name = input(">> ").strip() or "Player"

        self.show_instructions()  

        self.print_board()
        while True:
            ch = getch()
            if ch in ('q', 'Q'):
                print("Game quit.")
                break
            
            moved = False
            if ch in ('a', 'A', '\x1b[D', '\xe0K'):  
                moved = self.move_left()
            elif ch in ('d', 'D', '\x1b[C', '\xe0M'):  
                moved = self.move_right()
            elif ch in ('w', 'W', '\x1b[A', '\xe0H'): 
                moved = self.move_up()
            elif ch in ('s', 'S', '\x1b[B', '\xe0P'):  
                moved = self.move_down()

            if moved:
                self.spawn()
                self.print_board()
                if self.is_win():
                    print("🎉 Congratulations! You reached 2048!")
                    save_score(player_name, self.score)
                    break
                if not self.can_move():
                    print("❌ Game Over! No more moves possible.")
                    save_score(player_name, self.score)
                    break

        print("\nFinal Score:", self.score)
        print("\nUpdated Leaderboard:")
        show_leaderboard()

if __name__ == "__main__":
    game = Game2048()
    game.play()