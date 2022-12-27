import multiprocessing
import os.path
import pathlib
import uuid
from itertools import product
from multiprocessing import Pool
from string import ascii_lowercase, digits

BASE_DIR = pathlib.Path(__file__)
STORAGE = BASE_DIR.parent.joinpath("words_storage")


class Combinator:
    def __init__(self, alphabet, str_len):
        self.alphabet = alphabet
        self.str_len = str_len

    def product(self):
        with Pool(processes=multiprocessing.cpu_count() - 1) as pool:
            result = pool.map(self._get_for_char, self.alphabet)
            # print(result)
            for name in result:
                with open("result.txt", mode="a") as file_result:
                    with open(name, mode="r") as producer:
                        file_result.write(producer.read())

    def _generate_base_combinations(self):
        return tuple(product(self.alphabet, repeat=self.str_len-1))

    def _get_for_char(self, char) -> pathlib.Path:
        result = []
        file_name = STORAGE.joinpath(f"{uuid.uuid4()}.txt")
        for starter_combination in product(self.alphabet, repeat=self.str_len-1):
            combination = [char]
            combination.extend(starter_combination)
            result.append(combination)
        with open(file_name, mode="w") as file:
            file.write(Combinator.writer(result)+"\n")
        return file_name

    @staticmethod
    def writer(result_list: list[list]):
        return "\n".join(["".join(el) for el in result_list])

    @staticmethod
    def write_result_part(to_write: list[list[str]]):
        str1 = "\n".join(["".join(el) for el in to_write])
        with open("result.txt", mode="a") as file:
            file.write(str1 + "\n")


if __name__ == '__main__':
    # alphabet_for_combinations = ["a", "b", "c", "d", "e"]
    repeats = 5
    alphabet_for_combinations = ascii_lowercase + digits
    combinator = Combinator(alphabet_for_combinations, repeats)
    combinator.product()
