import noise
import turtle
import numpy as np
from PIL import Image
from scipy import interpolate

# inp = int(input())
# np.random.seed(7777)

def map_lerp(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

class Board:

    colors = {
        'white': np.array([255, 255, 255]),
        'black': np.array([0, 0, 0]),
        'fruit': np.array([255, 66, 80]),
        'darkSand': np.array([214, 170, 75]),
        'darkGreen': np.array([34, 139, 34]),
        'lightSand': np.array([230, 210, 175]),
        'green': np.array([119, 204, 65]),
        'darkGreen': np.array([17, 74, 17]),
        'snow': np.array([220, 220, 220]),
        'mountain': np.array([139, 137, 137])
    }

    palette1 = [
        np.array([142, 177, 199]),
        #8EB1C7
        np.array([176, 46, 12]),
        #B02E0C
        np.array([235, 69, 17]),
        #EB4511
        np.array([193, 191, 181]),
        #C1BFB5
        np.array([254, 253, 255])
    ]

    palette2 = [
        np.array([240, 162, 2]),
        #F0A202
        np.array([241, 136, 5]),
        #F18805
        np.array([217, 93, 57]),
        #D95D39
        np.array([32, 44, 89]),
        #202C59
        np.array([88, 31, 24])
    ]

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
        p = 0.8
        aux_matrix = self.board.copy()

        bool_matrix = np.random.choice(a=[False, True], size=(self.width, self.height), p=[p, 1-p])
        
        self.board[self.width // 4 : 3 * self.width // 4, self.height // 4 : 3 * self.height // 4] = bool_matrix[self.width // 4 : 3 * self.width // 4, self.height // 4 : 3 * self.height // 4]
        self.board[self.board == True] = 255

        
        for _ in range(generations):
            for i in range((self.width // 4) + kernel // 2, (3 * self.width // 4) - kernel // 2):
                for j in range((self.height // 4) + kernel // 2, (3 * self.height // 4) - kernel // 2):

                    subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                      j - kernel // 2 : j + kernel // 2 + 1]

                    n_cells = np.count_nonzero(subm)
                    
                    if self.board[i, j] == 255: n_cells -= 1
                    
                    if n_cells < 2: aux_matrix[i, j] = 0
                    elif (n_cells == 2 or n_cells == 3) and self.board[i, j] == 255: pass
                    elif n_cells > 3 and self.board[i, j] == 255: aux_matrix[i, j] = 0
                    elif n_cells == 3 and self.board[i, j] == 0: aux_matrix[i, j] = 255

            self.board = aux_matrix

        ncells_array = []
        for i in range(kernel // 2, self.width - kernel // 2):
            for j in range(kernel // 2, self.height - kernel // 2):
                
                subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                  j - kernel // 2 : j + kernel // 2 + 1]

                ncells_array.append(np.count_nonzero(subm))    
        
        board.colorize()

        

    def colorize(self):
        # reshaping
        new_matrix = np.zeros((self.width, self.height, 3), 'uint8')
        
        new_matrix[self.board == 255] = self.colors['white']
        # new_matrix[self.board == 127] = self.darkSand
        # new_matrix[self.board == 20] = self.fruitColor
        new_matrix[self.board == 0] = self.colors['lightSand']

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
                
                if np.array_equiv(self.board[i, j], self.colors['white']): n_cells -= 1

                if np.array_equiv(self.board[i, j], self.colors['white']) and n_cells > 2   :
                    aux_matrix[i, j] = self.palette2[np.random.randint(len(self.palette2))]

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