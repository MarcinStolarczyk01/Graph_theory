from random import randint
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessScheduler:
    def __init__(
        self,
        processors_coefficients: tuple[float, ...],
        min_exec_time=10,
        max_exec_time=90,
        tasks_num=100,
    ):
        logger.info("Setting parameters.")
        self.coefficients = processors_coefficients
        self.min_exec_time = min_exec_time
        self.max_exec_time = max_exec_time
        self.tasks = self.generate_tasks(tasks_num)

    def run(self, max_stagnation: int, max_time: float) -> float:
        start = time.time()
        ancestor = self.generate_chromosome()
        ancestor_total_exec_time = self.calc_total_exec_time(ancestor)

        upgrades = 0
        stagnation = 0
        generation = 0
        logger.info("Starting optimization process...")
        while stagnation < max_stagnation and time.time() - start < max_time:
            offspring = self.mutate(ancestor)
            offspring_total_exec_time = self.calc_total_exec_time(offspring)

            if offspring_total_exec_time < ancestor_total_exec_time:
                ancestor = offspring
                ancestor_total_exec_time = self.calc_total_exec_time(ancestor)
                upgrades += 1
                stagnation = 0
            else:
                stagnation += 1

            generation += 1

        processors_runtime = {
            f"P{proc_idx}-{coefficient}: ": sum(
                [
                    self.tasks[idx]
                    for idx, proc in enumerate(ancestor)
                    if proc == proc_idx
                ]
            )
            * coefficient
            for proc_idx, coefficient in enumerate(self.coefficients)
        }
        logger.info("Optimization process finished.")
        logger.info(
            f"""\n
{10*'='}RESULTS{10*'='}
Processors runtimes: {processors_runtime}
Solution chromosome: {ancestor}
Solution value:      {ancestor_total_exec_time} sec
Upgrades:            {upgrades}
Generations:         {generation}
Execution time       {(time.time() - start):.2f} sec"""
        )
        return ancestor_total_exec_time / self.calc_theoretical_best_time()

    def calc_total_exec_time(self, chromosome: list[int]) -> float:
        times = []
        for proc_idx, coefficient in enumerate(self.coefficients):
            times.append(
                sum(
                    coefficient * self.tasks[task_idx]
                    for task_idx, genome in enumerate(chromosome)
                    if genome == proc_idx
                )
            )

        return max(times)

    def generate_chromosome(self) -> list[int]:
        processors_num = len(self.coefficients)
        return [randint(a=0, b=processors_num - 1) for _ in range(len(self.tasks))]

    def generate_tasks(self, tasks_num) -> tuple[int, ...]:
        return tuple(
            [
                randint(a=self.min_exec_time, b=self.max_exec_time)
                for _ in range(tasks_num)
            ]
        )

    def calc_theoretical_best_time(self) -> float:
        total_workload = sum(self.tasks)
        speeds = [1 / coefficient for coefficient in self.coefficients]
        speed_sum = sum(speeds)

        proportional_workload = [speed / speed_sum * total_workload for speed in speeds]

        theoretical_times = [
            workload * coefficient
            for workload, coefficient in zip(proportional_workload, self.coefficients)
        ]

        return max(theoretical_times)

    @staticmethod
    def mutate(chromosome: list[int]) -> list[int]:
        offspring = chromosome.copy()
        idx_1, idx_2 = randint(0, len(chromosome) - 1), randint(0, len(chromosome) - 1)
        genome_1 = chromosome[idx_1]
        offspring[idx_1] = chromosome[idx_2]
        offspring[idx_2] = genome_1

        return offspring


if __name__ == "__main__":
    optimum_percentage = []
    for _ in range(10):
        optimum_percentage.append(
            100
            * ProcessScheduler(
                processors_coefficients=(1, 1.25, 1.5, 1.75), tasks_num=100
            ).run(max_stagnation=int(1e6), max_time=10)
        )
    logger.info(f"\n\nPercentage_of_optimum: {optimum_percentage}")
