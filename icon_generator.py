import noise
import turtle
import numpy as np
from PIL import Image
import colorsys as cs
import math
import random

seed = np.random.randint(120498)
np.random.seed(seed)
random.seed(seed)

class Board:

    board = None
    width = 0
    height = 0

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = np.zeros((w, h), 'uint8')


    

    def gen_random(self):
        kernel = 3

        generations = 10 * np.random.randint(2, 21)
        print("Generations: ", generations)
        
        p = random.uniform(0.3, 1)
        print("Initial probability dist: ", p)

        aux_matrix = self.board.copy()
        bool_matrix = np.random.choice(a=[False, True], size=(self.width, self.height), p=[p, 1-p])
        
        margin = np.random.randint(5, 16)

        self.board[self.width // margin : (margin - 1) * self.width // margin, 
        self.height // margin : (margin - 1) * self.height // margin] = bool_matrix[self.width // margin : (margin - 1) * self.width // margin, 
                                                                                    self.height // margin : (margin - 1) * self.height // margin]
        self.board[self.board == True] = 255

        
        for _ in range(generations):
            for i in range((self.width // margin) + kernel // 2, ((margin - 1) * self.width // margin) - kernel // 2):
                for j in range((self.height // margin) + kernel // 2, ((margin - 1) * self.height // margin) - kernel // 2):

                    subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                      j - kernel // 2 : j + kernel // 2 + 1]

                    n_cells = np.count_nonzero(subm)
                    
                    if self.board[i, j] == 255: n_cells -= 1
                    
                    if n_cells < 2: aux_matrix[i, j] = 0
                    elif (n_cells == 2 or n_cells == 3) and self.board[i, j] == 255: pass
                    elif n_cells > 3 and self.board[i, j] == 255: aux_matrix[i, j] = 0
                    elif n_cells == 3 and self.board[i, j] == 0: aux_matrix[i, j] = 255

            self.board = aux_matrix

        board.colorize(margin)

        
    def generate_colors(self):
        colors = []
        
        random_hue = np.random.rand()
        random_saturation = np.random.rand()
        random_value = random.uniform(0.25, 1)
        
        base_color = np.array([random_hue, random_saturation, random_value])
        colors.append(base_color)
        
        for _ in range(4):
            new_hue = math.fmod(base_color[0] + random.uniform(-.35, .35), 1)
            new_sat = math.fmod(base_color[1] + random.uniform(-.35, .35), 1)
            new_val = math.fmod(base_color[2] + random.uniform(-.35, .35), 1)
            col = np.array([new_hue, new_sat, new_val])
            
            colors.append(col)

        output = []
        for color in colors:
            rgb_color = cs.hls_to_rgb(color[0], color[1], color[2])
            rgb_color = np.array([rgb_color[0], rgb_color[1], rgb_color[2]])
            rgb_color = (rgb_color * 255).astype(int)
            
            output.append(rgb_color)

        sort_criteria = lambda color: 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        output.sort(key=sort_criteria)

        return output


    def colorize(self, margin):
        pal = self.generate_colors()

       
        # reshaping
        new_matrix = np.zeros((self.width, self.height, 3), 'uint8')
        
        new_matrix[self.board == 255] = [255, 255, 255]
        new_matrix[self.board == 0] = pal[0]

        self.board = new_matrix
        del new_matrix

        aux_matrix = self.board
        kernel = 3

        for i in range((self.width // margin) + kernel // 2, ((margin - 1) * self.width // margin) - kernel // 2):
            for j in range((self.height // margin) + kernel // 2, ((margin - 1) * self.height // margin) - kernel // 2):

                if np.array_equiv(self.board[i, j], [255, 255, 255]):
                    val = noise.pnoise2(i, j, octaves=4, lacunarity=0.23, persistence=2)

                    if val > -0.5 and val <= -0.25:
                        aux_matrix[i, j] = pal[1]
                    elif val > -0.25 and val <= 0:
                        aux_matrix[i, j] = pal[2]
                    elif val > 0 and val <= 0.25:
                        aux_matrix[i, j] = pal[3]
                    elif val > 0.25 and val <= 0.5:
                        aux_matrix[i, j] = pal[4]
                        
        self.board = aux_matrix
        self.board[0:5, 0:1] = [2, 2, 2]
        self.board[0:1, 0:5] = [2, 2, 2]
        self.board[0:5, 0:5] = pal[0]
        self.board[5:10, 0:5] = pal[1]
        self.board[10:15, 0:5] = pal[2]
        self.board[15:20, 0:5] = pal[3]
        self.board[20:25, 0:5] = pal[4]



    def display(self):
        img = Image.fromarray(self.board)
        img = img.resize((800, 800))
        # img.save("imgs/"+str(seed)+".png")
        img.show()
        



if __name__ == "__main__":
    board = Board(100, 100)
    board.gen_random()
    board.display()
    print("\n***Program finished***\n\n\n")