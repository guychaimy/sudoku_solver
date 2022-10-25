"""
Coding a Sudoku solver in Python using recursion/backtracking

base on the video: https://www.youtube.com/watch?v=tvP_FZ-D9Ng
"""


import sys
import cv2


class Puzzle():

    def __init__(self, filename):
        self.height = 9
        self.width = 9
        self.filename = filename

        # 1. Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

        # Determine height and width of puzzle
        # contents = contents.splitlines()

        # 2. build the sudoku puzzle --> self.puzzle
        self.puzzle = []
        for r in range(self.width):
            row = []
            for c in range(self.height):
                if c < len(contents[r]) and contents[r][c].isnumeric():
                    row.append(int(contents[r][c]))
                else:
                    row.append(-1)
            self.puzzle.append(row)


    def __repr__(self):
        return ('\n\r'.join([''.join(['{:4}'.format(item) for item in row])
                           for row in self.puzzle]))


    def check_puzzle_validity(self):
        # check validity of the puzzle
        for i in range(9):
            # 1. check row and Check columns
            row_vals = []
            col_vals = []
            row_vals = [self.puzzle[i][j] for j in range(9) if self.puzzle[i][j] != -1]
            col_vals = [self.puzzle[j][i] for j in range(9) if self.puzzle[j][i] != -1]
            if len(row_vals) != len(set(row_vals)) or len(col_vals) != len(set(col_vals)):
                return False

        # 2. Check all squares
        for r in range(3):
            for c in range(3):
                # Get the values of a sudoku square
                sqr_vals = []
                start_row = r * 3
                start_col = c * 3
                sqr_vals = [self.puzzle[start_row + r][start_col: start_col + 3] for r in range(3)]
                # flattern the 2d list
                sqr_vals = [j for sub in sqr_vals for j in sub if j != -1]
                # check for duplicates
                if len(sqr_vals) != len(set(sqr_vals)):
                    return False
        return True


    def find_next_empty(self, puzzle):
        # Find the next available place in puzzle if there is any
        # retrun the row and col of that cell. empty cell represented by -1
        # If no empty cell return None, None
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] == -1:
                    return row, col
        return None, None


    def is_valid(self, puzzle, guess, row, col):
        # return True is the guess is valid
        # else retrun False
        # 1. check row
        row_vals = puzzle[row]
        if guess in row_vals:
            return False
        # 2. check column
        col_vals = []
        col_vals = [puzzle[r][col] for r in range(9)]
        if guess in col_vals:
            return False
        # 3. check square
        sqr_vals = []
        # find the square
        # start row: row // 3, start col: col // 3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        sqr_vals = [puzzle[start_row + r][start_col: start_col + 3] for r in range(3)]
        if guess in sqr_vals:
            return False
        # 4. if all check pass return it's valid guess
        return True


    def solve_sudoku(self):
        # solve sudoku by using recursion function.
        # the function check if a solution exist and return the solution (if exist)

        # 1. find an empty cell in the puzzle
        row, col = self.find_next_empty(self.puzzle)
        # 1.1 if there isn't any return a massage to user "No solution"
        if row == None:
            return True
        # 2. make a guess for the empty cell
        for guess in range(1, 10):
            # 3. check if this a valid guss
            if self.is_valid(self.puzzle, guess, row, col):
                # 3.1 if valid , place the guess in puzzle
                self.puzzle[row][col] = guess
                # Now recurse using this puzzle
                # 4. recursively call the puzzle
                if self.solve_sudoku():
                    return True
            # 5. if guess is not valid OR doesn't solve the puzzle backtrack and try new guess
            self.puzzle[row][col] = -1
        # 6. if no solution this puzzle is un solvable
        return False


    def output_image(self, filename):
        """Generates image with all houses and hospitals."""
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "white"
        )
        # The numbers
        font1 = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 65)
        # The name of the puzzle
        font2 = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 30)
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            #  take off all the -1 from the puzzle
            f = list(map(lambda x: x if x > -1 else " ", self.puzzle[i]))
            for j in range(self.width):

                # Draw cell
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="black")

                #  Draw the numbers from the puzzle
                draw.text(
                    (rect[0][0]+30,rect[0][1]+5), str(f[j]),
                    fill="white",
                    font=font1,
                )

        # Add cost
        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "black"
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Puzzle: {self.filename}",
            fill="white",
            font=font2
        )

        img.save(filename)
        
        
def main():
    # make sure a puzzle file has been assigned
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    # Open the txt file and build the initial puzzle state
    p = Puzzle(sys.argv[1])

    # print intial puzzle state
    print(sys.argv[1])
    print("Initial puzzle:\n", p)

    # check if this is a valid and legal puzzle
    if p.check_puzzle_validity():
        filename = sys.argv[1].split(".")[-2]
        p.output_image(filename+"-initial.png")
        # try to solve the sudoku and print result if there is
        if p.solve_sudoku():
            print("Solved puzzle:\n", p)
            p.output_image(filename+"-solved.png")
        else:
            print("This puzzle can't be solved")
    else:
        print(f"Puzzle {sys.argv[1]} is not a legal sudoku puzzle")


if __name__ == '__main__':
    main()
