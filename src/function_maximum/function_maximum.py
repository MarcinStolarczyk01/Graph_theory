from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FunctionMaximum:

    def __init__(
        self,
        individuals_num: int,
        function: Callable[[float, float], float],
        x_domain: tuple[float, float],
        y_domain: tuple[float, float],
    ):
        if individuals_num % 2 != 0:
            raise ValueError("Individuals number must be an even number.")

        self._individuals_num = individuals_num
        self._function = function
        self._x_domain = x_domain
        self._y_domain = y_domain

        self._records = np.full(shape=(10**6, 2), fill_value=-1, dtype=np.float16)

    def run(self, time_limit: float = 10, stagnation_limit: int = 10):
        stagnation = 0
        start = time.time()
        generation = 0

        population = self._create_initial_population()

        best_unit = population[0]

        while stagnation < stagnation_limit and time.time() - start < time_limit:
            offsprings = self._crossover(population)
            mutated_offsprings = self._mutate(offsprings)
            population = np.vstack((population, mutated_offsprings))

            top = self._make_tournament(population)
            if self._function(*top[0]) > self._function(*best_unit):
                best_unit = top[0]
            else:
                stagnation += 1

            generation += 1
            population = top
            self._records[generation] = self._function(*top[0]), time.time() - start

        logger.info("Optimization process finished.")
        logger.info(
            f"""\n
        {10 * '='}RESULTS{10 * '='}
        Solution chromosome: x={population[0][0]}, y={population[0][1]}
        Solution value:      {self._function(*best_unit)}
        Generations:         {generation}
        Execution time       {(time.time() - start):.2f} sec\n"""
        )
        self._plot()

    def _create_initial_population(self) -> np.ndarray:
        x_values = np.random.uniform(
            low=self._x_domain[0], high=self._x_domain[1], size=self._individuals_num
        )
        y_values = np.random.uniform(
            low=self._y_domain[0], high=self._y_domain[1], size=self._individuals_num
        )
        matrix = np.column_stack((x_values, y_values))

        return matrix

    @staticmethod
    def _crossover(population: np.ndarray) -> np.ndarray:
        offsprings = np.zeros_like(population, dtype=float)
        for i in range(0, len(offsprings), 2):
            parent1 = population[i]
            parent2 = population[random.randint(0, len(population) - 1)]

            offspring1 = np.array([parent1[0], parent2[1]])
            offspring2 = np.array([parent1[1], parent2[0]])

            offsprings[i] = offspring1
            offsprings[i + 1] = offspring2

        return np.vstack((population, offsprings))

    def _make_tournament(self, population: np.ndarray) -> np.ndarray:
        values = np.array(
            [self._function(chromosome[0], chromosome[1]) for chromosome in population]
        )
        arg_sort = np.argsort(values)[::-1][: self._individuals_num]

        return population[arg_sort]

    @staticmethod
    def _mutate(population: np.ndarray) -> np.ndarray:
        # mutate less than 20% of the population
        x_mutation = np.random.choice(
            a=[0.999, 1, 1.001], p=[0.05, 0.9, 0.05], size=len(population)
        )
        y_mutation = np.random.choice(
            a=[0.999, 1, 1.001], p=[0.05, 0.9, 0.05], size=len(population)
        )

        mutation = np.column_stack((x_mutation, y_mutation))

        return population * mutation

    def _plot(self) -> None:
        plt.plot(self._records[:, 0], self._records[:, 1])
        plt.savefig("function_maximum.png")


def main():
    func = lambda x, y: abs(
        np.sin(x)
        + np.sin(2 * x)
        + np.sin(4 * x)
        + np.cos(y)
        + np.cos(2 * y)
        + np.cos(4 * y)
    )
    FunctionMaximum(
        100, function=func, x_domain=(0, 2 * np.pi), y_domain=(0, 2 * np.pi)
    ).run(time_limit=5, stagnation_limit=10**5)


if __name__ == "__main__":
    main()
