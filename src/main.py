import random
import logging
import time
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level='INFO')
logger = logging.getLogger(__file__)

BAG_VOLUME = 2500

ITEMS_NUM = 100
ITEMS_VOLUMES = [random.randint(10, 90) for _ in range(ITEMS_NUM)]

GENERATIONS_NUM = 300
CHROMOSOME_LENGTH = ITEMS_NUM


def search_while(first_parent: list[int]):
    start = time.time()
    parent = [n for n in first_parent]
    parent_volume = []

    upgrades = 0
    parents_history = np.empty(shape=GENERATIONS_NUM, dtype=np.float32)
    generation = 0

    while generation < GENERATIONS_NUM:
        parent_volume = sum([n_v for n_v, n in zip(ITEMS_VOLUMES, parent) if n])

        if parent_volume == BAG_VOLUME:
            break

        mutation_idx = random.randint(0, CHROMOSOME_LENGTH - 1)
        child = [n for n in parent]
        child[mutation_idx] = abs(child[mutation_idx] - 1)
        child_volume = sum([n_v for n_v, n in zip(ITEMS_VOLUMES, child) if n])

        # if items of child do not fit but the parent's does
        if parent_volume < BAG_VOLUME < child_volume:
            pass
        # if items of the child fit and the parent's don't
        elif child_volume < BAG_VOLUME < parent_volume:
            parent = child
            upgrades += 1
        # if the child's volume is closer to the bag volume than to the parent's volume
        elif abs(child_volume - BAG_VOLUME) < abs(parent_volume - BAG_VOLUME):
            parent = child
            upgrades += 1



        parents_history[generation] = parent_volume
        if len(set(parents_history[max(generation - 100, 0):generation + 1])) == 1 and generation > 3:
            logger.info('The same parent for 100 generations, stopping the process...')
            break
        generation += 1

    logger.info(f"""
    Solution chromosome: {parent}
    Solution value:      {parent_volume}
    Upgrades:            {upgrades}
    Generations:         {generation}
    Execution time       {time.time() - start}""")



    fig, ax = plt.subplots()
    ax.plot(parents_history[:generation], list(range(generation)))
    plt.savefig('solution_convergence.png')

    return parent, parent_volume, upgrades, generation


if __name__ == "__main__":
    init_parent = [random.getrandbits(1) for _ in range(CHROMOSOME_LENGTH)]

    results = search_while(init_parent)
