import colorsys as cs
import math
import random


import noise
import numpy as np

import cv2 as cv
from PIL import Image

# set a random seed that will be displayed to name the final file with it.
seed = np.random.randint(120498)
print("Seed:", seed)
np.random.seed(seed)
random.seed(seed)

# Class Board that generates our image.
class Board:

    # Our board is a matrix of with and height dimensions of unsigned integers. (for now)
    board = None
    width = 0
    height = 0

    # We instantiate the board with these arguments in the main program at the very bottom.
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = np.zeros((w, h), 'uint8')


    

    def gen_random(self):
        # Generate random is the main function of this program. It is based on Conway's "Game of Life" cellular
        # automata system. We generate a matrix with a random distribution of points, that will grow or die based
        # on Conway's rules.

        # Kernel to use as the shape for the neighbourhood analysis for each cell. Similar to a convolution filter.
        kernel = 3

        # Generations to be run. The more we run, the further it goes in the simulation, providing an ever increasing
        # chaos.
        generations = 10 * np.random.randint(10, 20)
        print("Generations: ", generations)
        
        # Probability distribution for the initial state of the board we are going to run our program on.
        # This is used down in bool_matrix, where p is the probability that the cell is true (white and alive)
        # or false (black and dead).
        p = random.uniform(0.45, 0.55)
        print("Initial probability dist: ", p, "\n\n")


        # Auxiliar matrix to apply the changes. If we applied them to our own board, they would stack up
        # and not give the desired result. At the end of the iteration, we simply overwrite self.board with this variable.
        aux_matrix = self.board.copy()

        # The initial state of our board. This looks like a black canvas with some spots randomly
        # distributed across it. The greater p is, the more there will be, and viceversa.
        bool_matrix = np.random.choice(a=[False, True], size=(self.width, self.height), p=[p, 1-p])
        
        # Padding applied to the image so it clips it to a smaller, centered section which gives the
        # whole image a bit more space.
        margin = np.random.randint(5, 16)

        # We take the section of the bool_matrix that we desire (in this case, it depends on the margin we 
        # just defined) and copy it to our main board. 

        # To clarify, we are taking the section 
        #   width / margin to (margin - 1) * width / margin
        # which takes the center piece based on margin. 
        
        # For example, for margin 4, we take from 1/4 of width to 3/4 of width, because
        # width / margin is 1/4 of the total's width, and (4-1) * width / 4 corresponds to
        # 3/4 of the total's width. That shaves off those 1/4 of the sides. Same applies to height.
        self.board[self.width // margin : (margin - 1) * self.width // margin, 
        self.height // margin : (margin - 1) * self.height // margin] = bool_matrix[self.width // margin : (margin - 1) * self.width // margin, 
                                                                                    self.height // margin : (margin - 1) * self.height // margin]
        
        # Our first color treatment. Let whatever it is ```true``` be white.
        self.board[self.board == True] = 255

        # Our main generation loop.
        for _ in range(generations):
            # The same logic explained above applies here
            for i in range((self.width // margin) + kernel // 2, ((margin - 1) * self.width // margin) - kernel // 2):
                for j in range((self.height // margin) + kernel // 2, ((margin - 1) * self.height // margin) - kernel // 2):

                    # We take our neighbourhood based on our kernel
                    subm = self.board[i - kernel // 2 : i + kernel // 2 + 1,
                                      j - kernel // 2 : j + kernel // 2 + 1]

                    # We calculate how many live cells are around us.
                    n_cells = np.count_nonzero(subm)
                    
                    # If we are one, we substract, as we don't count for that.
                    if self.board[i, j] == 255: n_cells -= 1
                    
                    # This is just the rules explained in Conway's Game of Life translated to code:
                    
                    # If there are less that two alive cells around us, we die for underpopulation.
                    if n_cells < 2: aux_matrix[i, j] = 0
                    
                    # If there are exactly two or three, we stay whatever we were before.
                    elif (n_cells == 2 or n_cells == 3) and self.board[i, j] == 255: pass
                    
                    # If there are more than three while being alive, we die for overpopulation.
                    elif n_cells > 3 and self.board[i, j] == 255: aux_matrix[i, j] = 0
                    
                    # If there are exactly three while being dead, we come back to life, for reproduction.
                    elif n_cells == 3 and self.board[i, j] == 0: aux_matrix[i, j] = 255

            # After all the calculations, we overwrite our board and start all over again, for as much
            # generations as there were specified.
            self.board = aux_matrix

        # We may now apply some fancy coloring to our black and white board.
        board.colorize(margin)
        self.open_close()

        
    def generate_colors(self):
        # Generate colors simply generates a palette of 5 colors to use in our board. 
        # The process is simple, we generate one totally random color and then generate
        # the other four based on the hue, saturation and value of the first one, to 
        # preserve some correlation.

        colors = []
        
        # We generate a completely random (and rather dark) color to start off.
        random_hue = random.uniform(0, 1)
        random_saturation = random.uniform(0, 0.6)
        random_value = random.uniform(0, 0.3)
        
        # We append it to our colors list.
        base_color = np.array([random_hue, random_saturation, random_value])
        colors.append(base_color)
        print("Base color:", base_color)
        
        # We generate the other four by adding some random values to the 
        # parameters of the first color. While this is random, I tried
        # to balance it so the colors are somehow related to the first one
        # and, consecutively, to each other.
        for i in range(4):
            new_hue = base_color[0] + random.uniform(0.03, 0.4)
            new_sat = random.uniform(0, 1)
            new_val = base_color[2] + random.uniform(0.3, 0.7)
            col = np.array([new_hue, new_sat, new_val])
            print("Color "+str(i)+":", col)
            
            colors.append(col)

        print()

        # We now prepare our output.
        output = []

        # This just converts the HSL color to RGB, and appends it to the output list.
        for color in colors:
            rgb_color = cs.hls_to_rgb(color[0], color[1], color[2])
            rgb_color = np.array([rgb_color[0], rgb_color[1], rgb_color[2]])
            rgb_color = (rgb_color * 255).astype(int)
            print("Color:", rgb_color)

            output.append(rgb_color)

        # This is a small, but pretty important part. We sort the colors by how bright they look. 
        # This is a weighted sum of the R, G and B values corresponding to the bayesian distribution of pixels 
        # on a screen, which is taken into account based on how, humans, perceive color. 
        # Blue is the least taken into account, while green is the most.
        # This will ouput a single number: the smaller it is, the "darker" it will feel to us.
        sort_criteria = lambda color: 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        output.sort(key=sort_criteria)
        return output


    def colorize(self, margin):
        #This function will apply some color to the final board.

        # We generate the palette we are using
        palette = self.generate_colors()
       
        # We now generate a matrix of tuples, to store 24-bit colors, instead of single gray values.
        new_matrix = np.zeros((self.width, self.height, 3), 'uint8')
        
        # Whatever was white, it is 3 times whiter. If you recall, only alive cells are white.
        new_matrix[self.board == 255] = [255, 255, 255]

        # For the background (dead cells), we use the first color on the palette, 
        # which will hopefully be the darker one, since we previously sorted them.
        new_matrix[self.board == 0] = palette[0]

        # We overwrite our matrix with the new one and delete the scaffolding.
        self.board = new_matrix
        del new_matrix

        # Very similar process as the generation one. 
        aux_matrix = self.board
        kernel = 3

        # We evaluate only the section we are interested in.
        for i in range((self.width // margin) + kernel // 2, ((margin - 1) * self.width // margin) - kernel // 2):
            for j in range((self.height // margin) + kernel // 2, ((margin - 1) * self.height // margin) - kernel // 2):
                
                # For coloring, we only color what is a live cell.
                if np.array_equiv(self.board[i, j], [255, 255, 255]):

                    # To give a more spicy look, we generate a perlin noise map, and
                    # color our cells based on the height obtained.
                    val = noise.pnoise2(i, j, octaves=6, lacunarity=0.63, persistence=2)
                    if val > -0.5 and val <= -0.25:
                        aux_matrix[i, j] = palette[1]
                    elif val > -0.25 and val <= 0:
                        aux_matrix[i, j] = palette[2]
                    elif val > 0 and val <= 0.25:
                        aux_matrix[i, j] = palette[3]
                    elif val > 0.25 and val <= 0.5:
                        aux_matrix[i, j] = palette[4]

        # We overwrite our board as usual            
        self.board = aux_matrix

        # This block essentially draws the palette on the upper left corner.
        self.board[0:1, 0:1] = palette[0]
        self.board[0:1, 1:2] = palette[1]
        self.board[0:1, 2:3] = palette[2]
        self.board[0:1, 3:4] = palette[3]
        self.board[0:1, 4:5] = palette[4]


    def open_close(self):
        # Specify Kernel Size
        kernelSize = 1
        # Create the Kernel
        element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2*kernelSize+1, 2*kernelSize+1),(kernelSize, kernelSize))
        element_h = np.array([ [1, 0, 0],
                               [1, 1, 1],
                               [0, 0, 1]], dtype=np.uint8)
        element_v = np.array([ [0, 1, 1],
                               [0, 1, 0],
                               [1, 1, 0]], dtype=np.uint8)
        element_u = np.array([1], dtype=np.uint8)
        # Perform Erosion
        self.board = cv.dilate(self.board, element_u, iterations=1)
        self.board = cv.erode(self.board, element_u, iterations=1)

    def display(self):
        # Helper function to display and save the final image. We start with low resolution
        # images and then scale them up to get that pixel-art look (which I absolutely love)
        SCALE_FACTOR = 16
        img = Image.fromarray(self.board)
        img = img.resize((self.height * SCALE_FACTOR, self.width * SCALE_FACTOR))
        
        # img.save("imgs/"+str(seed)+".png")
        img.show()
        


# Main program where we call everything we just explained.
if __name__ == "__main__":
    board = Board(200, 200)
    board.gen_random()
    # board.open_close()
    board.display()
    print("\n***Program finished***\n\n\n")
