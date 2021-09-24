import pygame as pg
import sys
import time

pg.init()
CLOCK = pg.time.Clock()

# loading the images as python object

o_img = pg.image.load("letter_o.png")
x_img = pg.image.load("letter_x.png")

# resizing images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))


class Board():

    def __init__(self):
        self.width = 400
        self.height = 400
        self.board_color = (255, 255, 255)
        self.line_color = (0, 0, 0)
        self.cross_line_color = (255, 0, 0)
        self.screen = pg.display.set_mode((self.width, self.height + 100))
        self.caption = "Tic Tac Toe"
        pg.display.set_caption(self.caption)

    def game_initiating_window(self):
        print('Im trying to display game board')

        self.screen.fill(self.board_color)

        pg.draw.line(self.screen, self.line_color, (0, 100), (self.width, 100), 7)
        pg.draw.line(self.screen, self.line_color, (0, self.height + 100), (self.width, self.height + 100), 7)

        pg.draw.line(self.screen, self.line_color, (self.width / 3, 100), (self.width / 3, self.height + 100), 7)
        pg.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 100), (self.width / 3 * 2, self.height + 100),
                     7)

        pg.draw.line(self.screen, self.line_color, (0, 100 + self.height / 3), (self.width, 100 + self.height / 3), 7)
        pg.draw.line(self.screen, self.line_color, (0, 100 + self.height / 3 * 2),
                     (self.width, 100 + self.height / 3 * 2), 7)
        pg.draw.line(self.screen, self.line_color, (0, 100), (0, 100 + self.height), 7)
        pg.draw.line(self.screen, self.line_color, (self.width, 100), (self.width, 100 + self.height), 7)

    def cross_winner(self, i, direction):
        if direction == 'row':
            coords = ((30, 170 + self.height / 3 * i), (self.width - 30, 170 + self.height / 3 * i))
        elif direction == 'col':
            coords = ((self.width / 3 * i + 70, 130), (self.width / 3 * i + 70, self.height + 100 - 30))
        elif i == 0:
            coords = ((30, 130), (self.width - 30, self.height + 100 - 30))
        else:
            coords = ((self.width - 30, 130), (30, self.height + 100 - 30))
        pg.draw.line(self.screen, self.line_color, coords[0], coords[1], 7)
        pg.display.update()

    def display_game_status(self, status):
        print ('Im tryingto display status')
        self.screen.fill((0, 0, 0), (0, 0, 500, 100))

        if status == "win":
                message = f"YOU WON!"
                self.screen.fill((255, 0, 0), (0, 0, 500, 100))
        if status == 'lost':
                message = f"YOU LOST!"
                self.screen.fill((120, 120, 120), (0, 0, 500, 100))

        elif status == 'tie':
            message = "Game over!"
        elif status == 'move':
                message = f"Make your move"
        else:
                message = "Wait for opponent"
        font = pg.font.SysFont("comicsans", 40)

        img = font.render(message, True, (255, 255, 255))


        rect = img.get_rect(center=(self.width / 2, 50))
        self.screen.blit(img, rect)
        # pg.draw.rect(img, (0,255,0), rect, 4)
        pg.display.update()

    def detect_square(self, pos):
        x = pos[0]
        y = pos[1]
        if x < self.width / 3:
            col = 1
        elif x < self.width / 3 * 2:
            col = 2
        else:
            col = 3
        if y < 100:
            row = None
        elif y < 100 + self.height / 3:
            row = 1
        elif y < 100 + self.height / 3 * 2:
            row = 2
        else:
            row = 3
        return (row, col)

    # added turn to params
    def mark_board(self, row, col, turn):

        print(f"Marking row{row} and col{col}with{turn}")
        margin_x = 30
        margin_y = 130
        if col == 1:
            x = margin_x
        if col == 2:
            x = self.width / 3 + margin_x
        if col == 3:
            x = self.width / 3 * 2 + margin_x

        if row == 1:
            y = margin_y

        if row == 2:
            y = self.height / 3 + margin_y

        if row == 3:
            y = self.height / 3 * 2 + margin_y

        if turn == 1:
            self.screen.blit(x_img, (x, y))
        else:
            self.screen.blit(o_img, (x, y))
        pg.display.update()

    # def reset_game(self):
    #
    #     time.sleep(1)
    #     game.reset()
    #     self.game_initiating_window()

    # game_initiating_window()

    # while (True):
    #
    #     # display_game_status()
    #     pg.display.update()
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             pg.quit()
    #             sys.exit()
    #         elif event.type == pg.MOUSEBUTTONDOWN:
    #             pos = pg.mouse.get_pos()
    #             print('Clicked!')
    #             process_click(pos)
    #             if (game.is_over):
    #                 display_game_status()
    #                 pg.display.update()
    #
    #                 pg.time.Clock().tick(60)
    #
    #                 reset_game()
    #     pg.time.Clock().tick(10)
