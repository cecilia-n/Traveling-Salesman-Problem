import numpy as np
import math
import time


class BranchAndBound:
    def __init__(self, matrix):

        self.matrix = matrix
        self.min_edge = np.where(matrix > 0, matrix, np.inf).min()

        self.num_towns = len(matrix)
        self.towns = list(range(len(matrix)))  # Ex: numTowns = 3 →  [0, 1,  2]

        self.best_path = None
        self.best_cost = math.inf

    def heuristic(self, path):
        """
        Heuristic to estimate cost from current path node to goal
        """
        num_unvisited = self.num_towns - len(path)
        h_n = num_unvisited * self.min_edge
        return h_n

    def isComplete(self, path):
        """
        Checks if our current path is a complete path (returns back to the start node !!!)
        """
        if len(path) == self.num_towns + 1:
            return True

    def computeCost(self, path):  # returns (float)
        """
        Calculates total cost of the path so far
        """
        cost = 0
        for i in range(len(path) - 1):
            cost += self.matrix[path[i], path[i + 1]]
        return cost

    def print_path(self):
        print(" → ".join([str(i) for i in self.best_path]))
        return

    def branchAndBound(self):
        start_time = time.time()
        root = 0  # Assume starting town is always 0
        stack = []
        stack.append([root])

        while len(stack) != 0:
            current = stack.pop()  # remove and retrieve last item put into the stack

            if self.computeCost(current) + self.heuristic(current) < self.best_cost:
                if self.isComplete(current):  # complete if returns back to the start node !!!
                    self.best_path = current
                    self.best_cost = self.computeCost(current)
                else:  # if not a complete path
                    if len(current) < self.num_towns:
                        for t in self.towns:
                            if t not in current:
                                new = current + [t]
                                stack.append(new)
                    elif len(current) == self.num_towns:
                        new = current + [0]
                        stack.append(new)

        # print best path
        print("--------------------------------------------------------------------")
        print("Ending cost: {}".format(float(self.best_cost)))
        print("Ending path:\n")
        print("{}".format(self.print_path()))
        print("--------------------------------------------------------------------")
        print("Total time taken for {} cities: {} seconds".format(self.num_towns, time.time() - start_time))
        print("--------------------------------------------------------------------")
        print("Solution with path cost {}".format(self.best_cost))

        self.write_to_file("\n")
        self.write_to_file("Ending cost: {}\n".format(float(self.best_cost)))
        self.write_to_file("Ending path:\n")
        self.write_to_file("{}\n".format(self.print_path()))
        self.write_to_file("\n")
        self.write_to_file("Total time taken for {} cities: {} seconds\n".format(self.num_towns, time.time()-start_time))
        self.write_to_file("\n")
        self.write_to_file("Solution with path cost {}\n".format(self.best_cost))


        return

    def write_to_file(self, content):
            f = open("results.txt", "a")
            f.write(content)
            f.close()

            return

def read_cities_from_file(filename="10_0.0_1.0.out"):
    """
    Read in distance matrix from file, clean and assign to BnB object.
    """

    with open(filename, 'r') as file:
        lines = file.readlines()
    m = [line.split(' ') for line in lines[1:]]
    m = [list(map(lambda x: np.float32(x.strip('\n')), i)) for i in m]
    m = np.matrix(m)
    np.fill_diagonal(m, 0)

    return np.squeeze(np.asarray(m))

if __name__ == "__main__":
    for file in os.listdir():
        if file[-3:]=='out':
            m = read_cities_from_file(file)
            bnb = BranchAndBound(m)
            bnb.write_to_file('==================================================================\n')
            bnb.write_to_file('Run for filename: {}\n'.format(file))
            bnb.branchAndBound()