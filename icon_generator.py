import noise
import turtle
import numpy as np
from PIL import Image

# inp = int(input())
np.random.seed(7777)

class Board:
    white = np.array([255, 255, 255])
    black = np.array([0, 0, 0])
    fruitColor = np.array([255, 66, 80])

    darkSand = np.array([214, 170, 75])
    green = np.array([34, 139, 34])
    sand = np.array([240, 233, 175])
    lightGreen = np.array([119, 204, 65])
    darkGreen = np.array([17, 74, 17])
    snow = np.array([220, 220, 220])
    mountain = np.array([139, 137, 137])

    board = None
    width = 0
    height = 0

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = np.zeros((w, h), 'uint8')

    def gen_icon(self):
        generations = 10 * 10
        kernel = 3
        p = 0.4
        aux_matrix = self.board.copy()

        bool_matrix = np.random.choice(a=[False, True], size=(self.width, self.height), p=[p, 1-p])
        self.board[bool_matrix] = 255
        
        for _ in range(generations):
            for i in range(kernel // 2, self.width - kernel // 2):
                for j in range(kernel // 2, self.height - kernel // 2):

                    subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                      j - kernel // 2 : j + kernel // 2 + 1]

                    n_cells = np.count_nonzero(subm)
                    
                    if self.board[i, j] == 255: n_cells -= 1
                    
                    if n_cells < 2: aux_matrix[i, j] = 0
                    elif (n_cells == 2 or n_cells == 3) and self.board[i, j] == 255: pass
                    elif n_cells > 3 and self.board[i, j] == 255: aux_matrix[i, j] = 0
                    elif n_cells == 3 and self.board[i, j] == 0: aux_matrix[i, j] = 255

        # for i in range(kernel // 2, self.width - kernel // 2):
        #     for j in range(kernel // 2, self.height - kernel // 2):

        #         if n_cells < 2: aux_matrix[i, j] = 0
        #         elif (n_cells == 2 or n_cells == 3) and self.board[i, j] == 255: pass
        #         elif n_cells > 3 and self.board[i, j] == 255: aux_matrix[i, j] = 0
        #         elif n_cells == 3 and self.board[i, j] == 0: aux_matrix[i, j] = 255


            self.board = aux_matrix
        
        board.colorize()

        

    def colorize(self):
        # reshaping
        new_matrix = np.zeros((self.width, self.height, 3), 'uint8')
        
        new_matrix[self.board == 255] = self.white
        # new_matrix[self.board == 127] = self.darkSand
        # new_matrix[self.board == 20] = self.fruitColor
        new_matrix[self.board == 0] = self.black

        self.board = new_matrix
        del new_matrix

        aux_matrix = self.board
        kernel = 3
        avg = []

        for i in range(kernel // 2, self.width - kernel // 2):
            for j in range(kernel // 2, self.height - kernel // 2):

                subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                  j - kernel // 2 : j + kernel // 2 + 1]

                n_cells = np.count_nonzero(subm) // 3
                # avg.append(n_cells)
                
                if not np.array_equiv(self.board[i, j], self.black): n_cells -= 1

                if np.array_equiv(self.board[i, j], self.white) and n_cells >= 3:

                    self.board[i, j] = self.lightGreen
                    new_color = self.board[i, j] + np.array([(n_cells + 20) % 255, (n_cells + 20) % 255, (n_cells + 20) % 255])
                    
                    aux_matrix[i, j] = new_color

        self.board = aux_matrix
        # print('Average', np.average(avg), 'Deviation', np.std(avg), 'Max', np.max(avg))

    def display(self):
        img = Image.fromarray(self.board)
        img = img.resize((800, 800))
        img.show()
        # img.save(f'imgs/{inp}.png')



if __name__ == "__main__":
    board = Board(80, 80)
    board.gen_icon()
    board.display()