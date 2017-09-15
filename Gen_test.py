#!/usr/bin/python3
import sys
import copy
import math
import random


class Board:
    def __init__(self, board_size, goal):
        ''' initialize a board'''
        self.board_size = board_size
        self.goal = goal

        self.fitness = 0

        # put first items in bord
        self.queens = list(range(self.board_size))
        # switch half of them randomly
        self.switch(self.board_size / 2)

    def __del__(self):
        pass

    def switch(self, count):
        ''' swithed queen places 'count' times'''
        count = int(count)

        for i in range(count):
            j = random.randint(0, self.board_size - 1)
            k = random.randint(0, self.board_size - 1)
            self.queens[j], self.queens[k] = self.queens[k], self.queens[j]

        # recheck fitness after moving queens
        self.compute_fitness()

    def regenerate(self):
        ''' randomly moves 3 queens
        used for creating new generation'''

        # randomly switvh 2 itmes
        self.switch(2)

        # get a random number if it's lower than 0.25 switch anither item
        if random.uniform(0, 1) < 0.25:
            self.switch(1)

    def compute_fitness(self):
        ''' computes fitness of current board
        bigger number is better'''
        self.fitness = self.goal

        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                if math.fabs(self.queens[i] - self.queens[j]) == j - i:
                    # for each queen guarding another one reduce fitness by 1
                    self.fitness -= 1

    def print_board(self):
        ''' prints current board in a nice way!'''
        for row in range(self.board_size):
            print("", end="|")

            queen = self.queens.index(row)

            for col in range(self.board_size):
                if col == queen:
                    print("Q", end="|")
                else:
                    print("_", end="|")
            print("")


class GaQueens:
    def __init__(self, board_size, population_size, generation_size):
        # store values to class properties
        self.board_size = board_size
        self.population_size = population_size
        self.generation_size = generation_size

        # counts how many generations checked
        self.generation_count = 0
        # fitness value of goal
        self.goal = int((self.board_size * (self.board_size - 1)) / 2)

        # current populations will go here
        self.population = []

        # creates the first population
        self.first_generation()

        while True:
            # if current population reached goal stop checking
            if self.is_goal_reached() == True:
                break
            # don't create more generations if program reached generation_size
            if -1 < self.generation_size <= self.generation_count:
                break

            # create another generation from last generation
            # (discards old generation)
            self.next_generation()

        # prints program result and exits
        print("==================================================================")

        # if couldn't find answer
        if -1 < self.generation_size <= self.generation_count:
            print("Couldn't find result in %d generations" % self.generation_count)
        # if there was a result, print it
        elif self.is_goal_reached():
            print("Correct Answer found in generation %s" % self.generation_count)
            for population in self.population:
                if population.fitness == self.goal:
                    # print result as a one lined list
                    print(population.queens)
                    # print result as a nice game board
                    population.print_board()

    def __del__(self):
        pass

    def is_goal_reached(self):
        ''' returns True if current population reached goal'''
        for population in self.population:
            if population.fitness == self.goal:
                return True
        return False

    def random_selection(self):
        ''' select some items from current population for next generation
        selection are items with highest fit value
        returns a list of selections'''
        population_list = []
        for i in range(len(self.population)):
            population_list.append((i, self.population[i].fitness))
        population_list.sort(key=lambda pop_item: pop_item[1], reverse=True)
        return population_list[:int(len(population_list) / 3)]

    def first_generation(self):
        ''' creates the first generation '''
        for i in range(self.population_size):
            self.population.append(Board(self.board_size, self.goal))

        self.print_population()

    def next_generation(self):
        ''' creates next generations (all except first one)'''

        # add to generation counter
        self.generation_count += 1

        # get a list of selections to create next generation
        selections = self.random_selection()

        # creates a new population using given selection
        new_population = []
        while len(new_population) < self.population_size:
            sel = random.choice(selections)[0]
            new_population.append(copy.deepcopy(self.population[sel]))
        self.population = new_population

        # make random changes to current population
        for population in self.population:
            population.regenerate()

        self.print_population(selections)

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


if __name__ == '__main__':
    # default values
    # size of board also shows how many queens are in game
    board_size = 14
    # size of each generation
    population_size = 10
    # how many generations should I check
    # -1 for no generation limit. (search to find a result)
    generation_size = -1

    # if there is arguments use them instead of default values
    if len(sys.argv) == 4:
        board_size = int(sys.argv[1])
        population_size = int(sys.argv[2])
        generation_size = int(sys.argv[3])

    # print some information about current quest!
    print("Starting:")
    print("    board size      : ", board_size)
    print("    population size : ", population_size)
    print("    generation size : ", generation_size)
    print("==================================================================")

    # Run!
    GaQueens(board_size, population_size, generation_size)