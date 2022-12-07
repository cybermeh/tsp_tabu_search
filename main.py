from random import choice
import numpy as np


class TSPTabuSearch:
    def __init__(self, input_file: str, iterations: int, tabu_length: int, neighbourhood_size: int):
        self.input_file = input_file
        self.iterations = iterations
        self.tabu_length = tabu_length
        self.neighbourhood_size = neighbourhood_size
        self.matrix = np.array(self.read_input_file(self.input_file))

    @staticmethod
    def read_input_file(file_path) -> list:
        result = []

        with open(file_path, 'r+') as f:
            lines = f.readlines()

            for line in lines:
                result.append([int(x.strip()) for x in line.split('\t')])

        return result

    def calculate_score(self, solution: list) -> int:
        cost, copied_solution = 0, solution.copy()
        cost = np.double(cost)

        for i in range(0, len(self.matrix) - 1):
            first_city, second_city = copied_solution[i], copied_solution[i + 1]
            cost += self.matrix[first_city - 1, second_city - 1]

        cost += self.matrix[copied_solution[0] - 1, copied_solution[-1] - 1]

        return cost

    def candidates_generator(self, n) -> list:
        candidates = []

        for k in range(0, self.neighbourhood_size):
            while True:
                while True:
                    x, y = choice(n), choice(n)

                    if x != y:
                        break

                if [x, y] not in candidates:
                    candidates.append([x, y])
                    break

        return candidates

    @staticmethod
    def swap_method(x, y, solution) -> list:
        result = solution.copy()

        result[x] = solution[y]
        result[y] = solution[x]

        return result

    def print_result(self, solution, score):
        print(f'Solution: {solution}')
        print(f'Score: {score}')
        print(f'Neighbourhood size: {self.neighbourhood_size}')
        print(f'Iterations: {self.iterations}')
        print(f'Tabu length: {self.tabu_length}')

    def run(self):
        solution = list(range(1, len(self.matrix) + 1))
        score = self.calculate_score(solution)
        tabu = []

        i = 0
        while i != self.iterations:
            candidates = self.candidates_generator(solution)
            min_solution = solution.copy()
            min_score = score
            tabu_pair = []
            j = 0

            while j != self.neighbourhood_size:
                pair = candidates[j].copy()
                new_solution = solution.copy()

                if pair not in tabu:
                    x = new_solution.index(pair[0])
                    y = new_solution.index(pair[1])
                    new_solution = self.swap_method(x, y, new_solution)
                    new_score = self.calculate_score(new_solution)

                    if new_score < min_score:
                        min_solution = new_solution.copy()
                        min_score = new_score
                        tabu_pair = pair.copy()

                j += 1

            if min_score < score:
                solution = min_solution.copy()
                score = min_score
                tabu.append(tabu_pair)

            if len(tabu) == self.tabu_length:
                del tabu[0]

            candidates.clear()
            i += 1

        self.print_result(solution, score)


# tsp_tabu_search = TSPTabuSearch(
#     input_file='inputs/1.txt',
#     iterations=30,
#     tabu_length=10,
#     neighbourhood_size=10
# )

tsp_tabu_search = TSPTabuSearch(
    input_file='inputs/2.txt',
    iterations=4000,
    tabu_length=40,
    neighbourhood_size=400
)

tsp_tabu_search.run()
