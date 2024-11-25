from random import randint
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessScheduler:
    def __init__(self, processors_coefficients: tuple[float, ...], min_exec_time=10, max_exec_time=90, tasks_num=100):
        self.coefficients = processors_coefficients
        self.min_exec_time = min_exec_time
        self.max_exec_time = max_exec_time
        self.tasks = self.generate_tasks(tasks_num)

    def run(self, max_stagnation: int, max_time: float):
        start = time.time()
        ancestor = self.generate_chromosome()
        ancestor_total_exec_time = self.calc_total_exec_time(ancestor)

        upgrades = 0
        stagnation = 0
        generation = 0
        while stagnation < max_stagnation and time.time() - start < max_time:
            offspring = self.mutate(ancestor)
            offspring_total_exec_time = self.calc_total_exec_time(offspring)

            if offspring_total_exec_time < ancestor_total_exec_time:
                ancestor = offspring
                upgrades += 1
                stagnation = 0
            else:
                stagnation += 1

            generation += 1

        asymptote = sum(self.tasks)/sum(self.coefficients)

        logger.info(f"""\n
        Asymptote:           {asymptote:.2f}
        Solution chromosome: {ancestor}
        Solution value:      {ancestor_total_exec_time} sec
        Upgrades:            {upgrades}
        Generations:         {generation}
        Execution time       {(time.time() - start):.2f} sec""")

    def calc_total_exec_time(self, chromosome: list[int]) -> float:
        times = []
        for proc_idx, coefficient in enumerate(self.coefficients):
            times.append(sum(
                coefficient * self.tasks[task_idx] for task_idx, genome in enumerate(chromosome) if genome == proc_idx))

        return max(times)

    def generate_chromosome(self) -> list[int]:
        processors_num = len(self.coefficients)
        return [randint(a=0, b=processors_num-1) for _ in range(len(self.tasks))]

    def generate_tasks(self, tasks_num) -> tuple[int, ...]:
        return tuple([randint(a=self.min_exec_time, b=self.max_exec_time) for _ in range(tasks_num)])

    @staticmethod
    def mutate(chromosome: list[int]) -> list[int]:
        offspring = chromosome.copy()
        idx_1, idx_2 = randint(0, len(chromosome) - 1), randint(0, len(chromosome) - 1)
        genome_1 = chromosome[idx_1]
        offspring[idx_1] = chromosome[idx_2]
        offspring[idx_2] = genome_1

        return offspring


if __name__ == "__main__":
    ProcessScheduler(processors_coefficients=(1,1.25, 1.5, 1.75), tasks_num=100).run(max_stagnation=1000, max_time=10000000)
