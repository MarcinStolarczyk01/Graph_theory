from random import randint
import time
import logging
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SalesmanNavigator:
    def __init__(self, cities_num: int, min_distance: int, max_distance: int):
        logger.info("Setting parameters.")
        self.cities_number: int = cities_num
        self.min_distance: int = min_distance
        self.max_distance: int = max_distance
        self.distance_matrix: np.ndarray = self._generate_distances(cities_num)

        self._records = np.zeros(shape=10**7, dtype=np.uint16)

    def run(self, max_stagnation: int, max_time: float, plot: bool = True) -> float:
        start = time.time()
        ancestor = self._generate_chromosome()
        ancestor_total_distance = self._cumulative_distance(ancestor)

        upgrades = 0
        stagnation = 0
        generation = 0
        logger.info("Starting optimization process...")
        while stagnation < max_stagnation and time.time() - start < max_time:
            offspring = self._mutate(ancestor)
            offspring_total_distance = self._cumulative_distance(offspring)

            if offspring_total_distance < ancestor_total_distance:
                ancestor = offspring
                ancestor_total_distance = self._cumulative_distance(ancestor)
                upgrades += 1
                stagnation = 0
            else:
                stagnation += 1

            self._records[generation] = ancestor_total_distance
            generation += 1

        logger.info("Optimization process finished.")
        logger.info(
            f"""\n
{10 * '='}RESULTS{10 * '='}
Solution chromosome: {ancestor}
Solution value:      {ancestor_total_distance} km
Upgrades:            {upgrades}
Generations:         {generation}
Execution time       {(time.time() - start):.2f} sec\n"""
        )
        if plot:
            logger.info("Creating plot...")
            records = self._records[self._records > 0]
            plt.plot([i for i in range(1, len(records) + 1)], records)
            plt.xlabel("Generations")
            plt.title("Salesman path VS solution generation")
            plt.ylabel("Total distance [km]")
            plt.savefig("Salesman.png")

        return ancestor_total_distance

    def _cumulative_distance(self, chromosome: np.ndarray):
        indices = np.arange(chromosome.size - 1)
        first = chromosome[indices]
        second = chromosome[indices + 1]
        return np.sum(self.distance_matrix[first, second])

    def _generate_chromosome(self) -> np.ndarray:
        cities = np.arange(start=1, stop=self.cities_number, dtype=int)
        np.random.shuffle(cities)
        return cities

    def _generate_distances(self, cities_num: int) -> np.ndarray:
        distances = np.random.randint(
            self.min_distance, self.max_distance, size=cities_num * cities_num
        ).reshape(cities_num, cities_num)
        np.fill_diagonal(distances, 0)

        return distances

    @staticmethod
    def _mutate(chromosome: np.ndarray[int]) -> np.ndarray[int]:
        offspring = chromosome.copy()
        idx_1, idx_2 = randint(0, len(chromosome) - 1), randint(0, len(chromosome) - 1)
        genome_1 = chromosome[idx_1]
        offspring[idx_1] = chromosome[idx_2]
        offspring[idx_2] = genome_1

        return offspring


if __name__ == "__main__":
    min_distance = SalesmanNavigator(100, 10, 100).run(10000, 10)
