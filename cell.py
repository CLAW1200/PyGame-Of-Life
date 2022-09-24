import pygame
import random

class Game:
    def __init__(self, width, height, cell_size):
        pygame.init()

        self.controls = [
            'Left Click: Place Cell',
            'Right Click: Remove Cell',
            'Space: Pause/Play',
            'R: Randomize Cells',
            'C: Clear Cells',
            'E: Toggle Place Cell',
            'W: Toggle Remove Cell',
            'P: Randomize Colours',
            'Up Arrow/MScroll: Speed Up',
            'Down Arrow/MScroll: Slow Down',
            'Right Arrow: Next Generation'
            ]

        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.grid = Grid(self.width, self.height, self.cell_size, self.screen)
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 500
        self.generation = 0
        self.paused = True
        self.randomize = False
        self.clear = False
        self.next_generation = False
        self.place = False
        self.remove = False
        self.update_delay = 0
        self.counter = 0
        self.alive_colour = (255, 255, 255)
        self.dead_colour = (0, 0, 0)
        self.text_colour = (255, 255, 255)
        self.setup()

    def random_colour(self):
        def random_colour_value():
            return random.randint(0, 255)
        alive_colour = (random_colour_value(), random_colour_value(), random_colour_value())
        dead_colour = (random_colour_value(), random_colour_value(), random_colour_value())
        if abs(alive_colour[0] - dead_colour[0]) < 50 and abs(alive_colour[1] - dead_colour[1]) < 50 and abs(alive_colour[2] - dead_colour[2]) < 50:
            self.random_colour()
        else:
            self.alive_colour = alive_colour
            self.dead_colour = dead_colour


    def setup(self):
        for i in range(self.grid.cell_width):
            for j in range(self.grid.cell_height):
                if i > 0:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i - 1, j))
                if i < self.grid.cell_width - 1:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i + 1, j))
                if j > 0:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i, j - 1))
                if j < self.grid.cell_height - 1:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i, j + 1))
                if i > 0 and j > 0:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i - 1, j - 1))
                if i < self.grid.cell_width - 1 and j > 0:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i + 1, j - 1))
                if i > 0 and j < self.grid.cell_height - 1:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i - 1, j + 1))
                if i < self.grid.cell_width - 1 and j < self.grid.cell_height - 1:
                    self.grid.get_cell(i, j).add_neighbor(self.grid.get_cell(i + 1, j + 1))

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.update_count()
            self.events()
            self.update()
            self.draw()

    def speed_up_game(self):
        if self.update_delay <= 0:
            self.update_delay = 0
        else:
            self.update_delay -= 1

    def slow_down_game(self):
        if self.update_delay >= 100:
            self.update_delay = 100
        else:
            self.update_delay += 1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place = True

                if event.button == 3:
                    self.remove = True

                if event.button == 4:
                    self.speed_up_game()
                if event.button == 5:
                    self.slow_down_game()
            
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                if event.key == pygame.K_e:
                    self.place = not self.place
                
                if event.key == pygame.K_w:
                    self.remove = not self.remove

                if event.key == pygame.K_r:
                    self.randomize = True
                if event.key == pygame.K_c:
                    self.clear = True
                    self.generation = 0
                if event.key == pygame.K_RIGHT:
                    self.next_generation = True
                if event.key == pygame.K_p:
                    self.random_colour()
                if event.key == pygame.K_UP:
                    self.speed_up_game()
                if event.key == pygame.K_DOWN:
                    self.slow_down_game()
                
    def update(self):
        if self.randomize:
            for i in range(self.grid.cell_width):
                for j in range(self.grid.cell_height):
                    if random.randint(0, 1) == 0:
                        self.grid.get_cell(i, j).set_alive()
                    else:
                        self.grid.get_cell(i, j).set_dead()
            self.randomize = False

        if self.clear:
            for i in range(self.grid.cell_width):
                for j in range(self.grid.cell_height):
                    self.grid.get_cell(i, j).set_dead()
            self.clear = False

        if self.next_generation:
            self.next_generation = False
            self.generation += 1
            for i in range(self.grid.cell_width):
                for j in range(self.grid.cell_height):
                    num_neighbors = self.grid.get_cell(i, j).get_num_neighbors()
                    if self.grid.get_cell(i, j).get_alive():
                        if num_neighbors < 2 or num_neighbors > 3:
                            self.grid.get_cell(i, j).set_next_dead()
                        else:
                            self.grid.get_cell(i, j).set_next_alive()
                    else:
                        if num_neighbors == 3:
                            self.grid.get_cell(i, j).set_next_alive()
                        else:
                            self.grid.get_cell(i, j).set_next_dead()
            self.grid.update()

        if self.place:
            pos = pygame.mouse.get_pos()
            x = int(pos[0] / self.cell_size)
            y = int(pos[1] / self.cell_size)
            if self.grid.get_cell(x, y).get_alive():
                pass
            else:
                self.grid.get_cell(x, y).set_alive()

            if not pygame.key.get_pressed()[pygame.K_e] and not pygame.mouse.get_pressed()[0]:
                self.place = False

        if self.remove:
            pos = pygame.mouse.get_pos()
            x = int(pos[0] / self.cell_size)
            y = int(pos[1] / self.cell_size)
            if self.grid.get_cell(x, y).get_alive():
                self.grid.get_cell(x, y).set_dead()

            if not pygame.key.get_pressed()[pygame.K_w] and not pygame.mouse.get_pressed()[2]:
                self.remove = False
                    
        if not self.paused and self.counter == self.update_delay:
            for i in range(self.grid.cell_width):
                for j in range(self.grid.cell_height):
                    num_neighbors = self.grid.get_cell(i, j).get_num_neighbors()
                    if self.grid.get_cell(i, j).get_alive():
                        if num_neighbors < 2 or num_neighbors > 3:
                            self.grid.get_cell(i, j).set_next_dead()
                        else:
                            self.grid.get_cell(i, j).set_next_alive()
                    else:
                        if num_neighbors == 3:
                            self.grid.get_cell(i, j).set_next_alive()
                        else:
                            self.grid.get_cell(i, j).set_next_dead()
            self.grid.update()
            self.generation += 1

    def update_count(self):
        if self.counter >= self.update_delay:
            self.counter = 0
        else:
            self.counter += 1
            

    def draw(self):
        self.text_colour = (255 - self.dead_colour[0], 255 - self.dead_colour[1], 255 - self.dead_colour[2])
        self.screen.fill((0, 0, 0))
        self.grid.draw()
        self.draw_text('Generation: ' + str(self.generation), 23, self.text_colour, 10, 10)
        self.draw_text('Update Speed: ' + str(100 - self.update_delay) + '/100', 23, self.text_colour, 10, 40)

        self.draw_text(str(self.controls[0]), 12, self.text_colour, 10, 100)
        self.draw_text(str(self.controls[1]), 12, self.text_colour, 10, 120)
        self.draw_text(str(self.controls[2]), 12, self.text_colour, 10, 140)
        self.draw_text(str(self.controls[3]), 12, self.text_colour, 10, 160)
        self.draw_text(str(self.controls[4]), 12, self.text_colour, 10, 180)
        self.draw_text(str(self.controls[5]), 12, self.text_colour, 10, 200)
        self.draw_text(str(self.controls[6]), 12, self.text_colour, 10, 220)
        self.draw_text(str(self.controls[7]), 12, self.text_colour, 10, 240)
        self.draw_text(str(self.controls[8]), 12, self.text_colour, 10, 260)
        self.draw_text(str(self.controls[9]), 12, self.text_colour, 10, 280)
        self.draw_text(str(self.controls[10]), 12, self.text_colour, 10, 300)

        pygame.display.update()

    def draw_text(self, text, size, colour, x, y):
        font = pygame.font.SysFont('Consolas', size)
        text = font.render(text, True, colour)
        self.screen.blit(text, (x, y))

    def start(self):
        self.run()


class Grid:
    def __init__(self, width, height, cell_size, screen):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = screen
        self.cells = []
        self.cell_width = int(self.width / self.cell_size)
        self.cell_height = int(self.height / self.cell_size)
        for i in range(self.cell_width):
            self.cells.append([])
            for j in range(self.cell_height):
                self.cells[i].append(Cell(i, j, self.cell_size, self.screen))

    def draw(self):
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                self.cells[i][j].draw()

    def update(self):
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                self.cells[i][j].update()

    def get_cell(self, x, y):
        return self.cells[x][y]

class Cell:
    def __init__(self, x, y, size, screen):
        self.x = x
        self.y = y
        self.size = size
        self.screen = screen
        self.colour = (255, 255, 255)
        self.neighbors = []
        self.alive = False
        self.next_alive = False

    def draw(self):
        if self.alive:
            self.colour = game.alive_colour
        else:
            self.colour = game.dead_colour

        pygame.draw.rect(self.screen, self.colour, (self.x * self.size, self.y * self.size, self.size, self.size))

    def update(self):
        self.alive = self.next_alive
        self.next_alive = False

    def set_alive(self):
        self.alive = True

    def set_dead(self):
        self.alive = False

    def set_next_alive(self):
        self.next_alive = True

    def set_next_dead(self):
        self.next_alive = False

    def get_alive(self):
        return self.alive

    def get_next_alive(self):
        return self.next_alive

    def add_neighbor(self, cell):
        self.neighbors.append(cell)

    def get_neighbors(self):
        return self.neighbors

    def get_num_neighbors(self):
        num = 0
        for cell in self.neighbors:
            if cell.get_alive():
                num += 1
        return num



if __name__ == '__main__':
    game = Game(1920, 1080, 30)
    game.start()
    pygame.quit()

