import sys
import math
import copy
import random

from tkinter import *

global Massiv
Massiv = []


class Board:

    def __init__(self, board_size, goal):
        self.board_size = board_size
        self.goal = goal

        self.fitness = 0
        self.queens = list(range(self.board_size))
        self.switch(self.board_size/2)


    def __del__(self):
        pass

    def switch(self, count):

        count = int(count)

        for i in range(count):
            l = random.randint(0,self.board_size - 1)
            m = random.randint(0,self.board_size - 1)

            self.queens[l], self.queens[m] = self.queens[m], self.queens[l]

        self.compute_fitness()

    def compute_fitness(self):

        self.fitness = self.goal
        for i in range(self.board_size):
            for j in range(i+1, self.board_size):
                if math.fabs(self.queens[i] - self.queens[j]) == j - i:
                    self.fitness -= 1
                if (self.queens[i] - self.queens[j]) == 0:
                    self.fitness -= 1

    def regenerate(self):
        self.switch(2)

        # get a random number if it's lower than 0.25 switch anither item
        if random.uniform(0, 1) < 0.25:
            self.switch(1)

    def print_board(self):
        ''' prints current board in a nice way!'''
        for row in range(self.board_size):
            print("", end="|")

            queen = self.queens.index(row)

            for col in range(self.board_size):
                if col == queen:
                    Massiv.append(col)
                    print("Q", end="|")
                else:
                    print("_", end="|")
            print("")


class GaQueens:

    def __init__(self, board_size, population_size, generation_size,canvas):

        self.board_size = board_size
        self.population_size = population_size
        self.generation_size = generation_size
        self.canvas = canvas
        self.generation_count = 0
        self.goal = int((self.board_size *(self.board_size - 1))/2)

        self.population = []

        self.first_generation()
        while True:
            if self.goal_isreached() == True:
                break
            if -1 < self.generation_size <= self.generation_count:
                break
            self.next_generation()
        print("|========================================|")

        if -1 < self.generation_size <= self.generation_count:
            print("Could not find a solution in %d generations" % self.generation_count)

        if self.goal_isreached() == True:
            print("We found a solution in %d generations" % self.generation_count)
            for population in self.population:
                if population.fitness == self.goal:
                    print(population.queens)
                    population.print_board()


    def goal_isreached(self):
        for population in self.population:
            if population.fitness == self.goal:
                return True
        return False

    def next_generation(self):

        self.generation_count += 1
        selections = self.random_selection()
        new_population = []
        while len(new_population) < self.population_size:
            sel = random.choice(selections)[0]
            new_population.append(copy.deepcopy(self.population[sel]))
        self.population = new_population

        for population in self.population:
            population.regenerate()

        self.print_population(selections)

    def random_selection(self):

        population_list = []
        for i in range(len(self.population)):
            population_list.append((i, self.population[i].fitness))
        population_list.sort(key=lambda pop_item: pop_item[1], reverse=True)
        return population_list[:int(len(population_list) / 3)]

    def first_generation(self):
        for i in range(self.population_size):
            self.population.append(Board(self.board_size,self.goal))
        print("First gen")
        self.print_population()

    def print_population(self, selections=None):
        ''' print all items in current population

        Population #15
            Using: [1]
            0 : (25) [6, 1, 3, 0, 2, 4, 7, 5]

        line 1: Population #15
            shows current population id
        line 2: Using: [1]
            shows id of items from last generation
            used for creating current generation
        line 3: 0 : (25) [0, 1, 2, 3, 4, 5, 6, 7]
            0 -> item is
            (25) -> fitness for current item
            [0, 1, 2, 3, 4, 5, 7] -> queen positions in current item


        '''
        print("Population #%d" % self.generation_count)

        if selections == None:
            selections = []

        print("       Using: %s" % str([sel[0] for sel in selections]))

        count = 0
        for population in self.population:
            print("%8d : (%d) %s" % (count, population.fitness, str(population.queens)))
            count += 1

def displ_queen(right,down):

    pass

if __name__ == '__main__':

    canvas_width = 480
    canvas_height = 480
    master = Tk()
    canvas = Canvas(width=canvas_width, height=canvas_height)
    canvas.pack()
    img = PhotoImage(file="dynboard.png")
    canvas.create_image(0, 0, anchor=NW, image=img)


    board_size = 8
    population_size = 3
    generation_size = -1

    if len(sys.argv) == 4:
        board_size = sys.argv[0]
        population_size = sys.argv[1]
        generation_size = sys.argv[2]

    print("Starting Genetic Algorithm !")
    print("Board size : %d\nPopulation size : %d\nGeneration size : %d\n"
          %(board_size,population_size,generation_size))
    GaQueens(board_size,population_size,generation_size,canvas)
    im1 = PhotoImage(file="rsz_1rsz_dynboard.png")
    im2 = PhotoImage(file="rsz_1rsz_dynboard.png")
    for index in range(len(Massiv)):
        if (index + Massiv[index])%2==0:
            canvas.create_image(index*60, Massiv[index]*60, anchor=NW, image=im1)
        else:
            canvas.create_image(index * 60, Massiv[index] * 60, anchor=NW, image=im2)
    master.mainloop()