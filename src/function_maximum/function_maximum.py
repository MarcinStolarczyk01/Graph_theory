from typing import Callable
import numpy as np
import random


class FunctionMaximum:

    def __init__(
        self,
        individuals_num: int,
        function: Callable[[float, float], float],
        x_domain: tuple[float, float],
        y_domain: tuple[float, float],
    ):
        self._individuals_num = individuals_num
        self._function = function
        self._x_domain = x_domain
        self._y_domain = y_domain

    def run(self, time_bound: float, stagnation_bound: int):
        population = self._create_initial_population()

    def _create_initial_population(self) -> np.ndarray:
        x_values = np.random.uniform(
            low=self._x_domain[0], high=self._x_domain[1], size=self._individuals_num
        )
        y_values = np.random.uniform(
            low=self._y_domain[0], high=self._y_domain[1], size=self._individuals_num
        )
        matrix = np.column_stack((x_values, y_values))

        return matrix

    def _crossover(self, population: np.ndarray) -> np.ndarray:
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
        # todo: pick 100 best chromosomes!
        pass

    def _mutate(self, population: np.ndarray) -> np.ndarray:
        pass


def main():
    func = lambda x, y: abs(np.sin(x) + np.cos(y))
    FunctionMaximum(
        100, function=func, x_domain=(0, 2 * np.pi), y_domain=(0, 2 * np.pi)
    ).run(time_bound=5, stagnation_bound=10**5)


if __name__ == "__main__":
    main()
