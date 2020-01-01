import noise
import turtle
import numpy as np
from PIL import Image
import colorsys as cs
import math

seed = np.random.randint(120498)
np.random.seed(seed)

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

    palette3 = [
        np.array([156, 255, 250]),
        np.array([172, 243, 157]),
        np.array([176, 197, 146]),
        np.array([169, 124, 115]),
        np.array([175, 62, 77])
    ]

    board = None
    width = 0
    height = 0

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = np.zeros((w, h), 'uint8')


    

    def gen_random(self):
        generations = 10 * np.random.randint(2, 21)
        print("Generations: ", generations)
        kernel = 3
        p = np.random.rand()
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

        board.colorize()

        
    def generate_colors(self):
        colors = []
        
        random_hue = np.random.rand()
        random_saturation = np.random.rand()
        # random_value = np.clip(np.random.rand() + 0.25, 0, 1)
        # print("Value: ", random_value)
        base_color = np.array([random_hue, random_saturation, 1])
        colors.append(base_color)
        
        for _ in range(4):
            new_hue = math.fmod(base_color[0] + np.random.rand(), 1)
            new_sat = math.fmod(base_color[1] + np.random.rand(), 1)
            col = np.array([new_hue, new_sat, 1])
            
            colors.append(col)

        output = []
        for color in colors:
            rgb_color = cs.hls_to_rgb(color[0], color[1], color[2])
            rgb_color = np.array([rgb_color[0], rgb_color[1], rgb_color[2]])
            rgb_color = (rgb_color * 255).astype(int)
            
            output.append(rgb_color)

        hue = lambda color: color[0]
        output.sort(key=hue)
        return output


    def colorize(self):
        pal = self.generate_colors()
        print("Colors: ", pal)

       
        # reshaping
        new_matrix = np.zeros((self.width, self.height, 3), 'uint8')
        
        new_matrix[self.board == 255] = self.colors['white']
        new_matrix[self.board == 0] = pal[0]

        self.board = new_matrix
        del new_matrix

        aux_matrix = self.board
        kernel = 3
        margin = np.random.randint(5, 16)

        

        for i in range((self.width // margin) + kernel // 2, ((margin - 1) * self.width // margin) - kernel // 2):
            for j in range((self.height // margin) + kernel // 2, ((margin - 1) * self.height // margin) - kernel // 2):

                if np.array_equiv(self.board[i, j], self.colors['white']):
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


    def display(self):
        img = Image.fromarray(self.board)
        img = img.resize((800, 800))
        # img.save("imgs/"+str(seed)+".png")
        img.show()
        



if __name__ == "__main__":
    board = Board(100, 100)
    board.gen_random()
    board.display()