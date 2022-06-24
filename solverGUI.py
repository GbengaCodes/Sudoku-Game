# GUI.py
# RUN THIS FILE
import sys

import pygame
from solver import sudoku_solver, isValid, print_board
import time

pygame.font.init()


class Grid:
    # To change the starting board change this
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if isValid(self.model, val, (row, col)) and sudoku_solver(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, pygame.Color("Black"), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, pygame.Color("Black"), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comics", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, "Grey")
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, "Black")
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, "red", (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, play_time, strikes):
    win.fill("White")
    # Draw time
    fnt = pygame.font.SysFont("comics", 30)
    text = fnt.render("Time: " + format_time(play_time), 1, "Black")
    win.blit(text, (560 - 170, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    screen = pygame.display.set_mode((540, 600))
    img = pygame.image.load('sudoku_final.jpg')
    screen.blit(img, (3, 30))
    fnt = pygame.font.SysFont("Times", 20)
    fnt2 = pygame.font.SysFont("comics", 18)
    esc_text = fnt.render("Welcome to Play Sudoku:", True, "Red")
    screen.blit(esc_text, (20 * (9 // 2), 50 * (9 // 2)))
    esc_text = fnt2.render("PRESS 'ESC': End game anytime", True, "Black")
    screen.blit(esc_text, (50 * (9 // 2), 65 * (9 // 2)))
    esc_text = fnt2.render("PRESS 'SPACE': Auto solve", True, "Black")
    screen.blit(esc_text, (50 * (9 // 2), 70 * (9 // 2)))
    esc_text = fnt.render("Game Loading...", True, "Blue")
    screen.blit(esc_text, (20 * (9 // 2), 80 * (9 // 2)))
    pygame.display.update()
    time.sleep(2)
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    auto_solved = False
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            fnt = pygame.font.SysFont("comics", 20)
                            esc_second = fnt.render("Sudoku Completed", True, "White")
                            esc_time = fnt.render("Time: " + str(play_time) + " seconds", True, "White")
                            win.fill('Black')
                            time.sleep(1)
                            win.blit(esc_text, (35 * (9 // 2), 60 * (9 // 2)))
                            win.blit(esc_second, (35 * (9 // 2), 65 * (9 // 2)))
                            win.blit(esc_time, (35 * (9 // 2), 70 * (9 // 2)))
                            pygame.display.update()
                            time.sleep(4)
                            pygame.quit()
                            sys.exit()
                            print("Game over")
                            run = False
                if event.key == pygame.K_SPACE:
                    sudoku_solver(board.board)
                    for i in range(len(board.board)):
                        for j in range(len(board.board[0])):
                            board.cubes[i][j].set(board.board[i][j])
                            if board.cubes[i][j].value == 0:
                                board.place(board.cubes[i][j])
                    auto_solved = True
                if event.key == pygame.K_ESCAPE:
                    if auto_solved:
                        esc_text = fnt.render("Solved by computer", True, "White")
                        esc_second = fnt.render("Sudoku Completed", True, "White")
                        esc_time = fnt.render("PlayTime: "+str(play_time)+" seconds", True, "White")
                        win.fill('Black')
                        win.blit(esc_text, (35 * (9 // 2), 60 * (9 // 2)))
                        win.blit(esc_second, (35 * (9 // 2), 65 * (9 // 2)))
                        win.blit(esc_time, (35 * (9 // 2), 70 * (9 // 2)))
                        pygame.display.update()
                        time.sleep(2)
                        pygame.quit()
                        sys.exit()
                    else:
                        fnt = pygame.font.SysFont("comics", 50)
                        fnt2 = pygame.font.SysFont("comics", 20)
                        esc_text = fnt.render("GOOD BYE PLAYER", True, "White")
                        game_status = fnt2.render("Sudoku not solved", True, "White")
                        esc_time = fnt2.render("PlayTime: "+str(play_time)+" seconds", True, "White")
                        win.fill('Black')
                        win.blit(esc_text, (30 * (9 // 2), 70 * (9 // 2)))
                        win.blit(game_status, ((9 // 2), 55 * (9 // 2)))
                        win.blit(esc_time, ((9 // 2), 60 * (9 // 2)))
                        pygame.display.update()
                        time.sleep(4)
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
