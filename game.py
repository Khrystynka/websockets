class Game:
    def __init__(self):
        self.winner_idx = None
        self.x_player =None
        self.o_player = None
        self.turn = 1
        self.winner = None
        self.winner_direction = None
        self.tie = None
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.ready = False
        self.is_over = False

    def has_tie(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if not self.board[i][j]:
                    return False
        return True

    def reset(self):
        self.winner_idx = None
        self.turn = 'x'
        self.winner = None
        self.winner_direction = None
        self.tie = None
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.is_over = False

    def has_winner(self):
        for i in range(3):
            if self.board[i][0] and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0], i, "row"
            if self.board[0][i] and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i], i, 'col'
        if self.board[0][0] and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0], 0, 'diag'
        if self.board[0][2] and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2], 1, 'diag'
        return (None, -1, "")

    def update_status(self):
        self.tie = self.has_tie()
        self.winner, self.winner_idx, self.winner_direction = self.has_winner()
        self.is_over = self.tie or self.winner

    def make_move(self, row, col):
        self.board[row - 1][col - 1] = self.turn
        self.update_status()
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def is_free(self, row, col):
        return self.board[row - 1][col - 1] == None
