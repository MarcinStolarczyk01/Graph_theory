from typing import Callable
import numpy as np


class FunctionMaximum:

    def __init__(
        self,
        individuals_num: int,
        function: Callable[[float, float], float],
        x_domain: float,
        y_domain: float,
    ):
        self._individuals_num = individuals_num
        self._function = function
        self._x_domain = x_domain
        self._y_domain = y_domain

    def run(self, time_bound: float, stagnation_bound: int):
        pass

    def _create_initial_population(self) -> np.ndarray:
        pass


def main():
    func = lambda x, y: abs(np.sin(x) + np.cos(y))
    FunctionMaximum(100, func).run(time_bound=5, stagnation_bound=10**5)


if __name__ == "__main__":
    main()
