import logging
import multiprocessing
import pathlib
import uuid
from itertools import product
from logging import Logger
from multiprocessing import Pool
from string import ascii_lowercase, digits
from typing import Iterable

BASE_DIR = pathlib.Path(__file__)
STORAGE = BASE_DIR.parent.joinpath("words_storage")


def init_logger() -> Logger:
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    return logger


class Combinator:
    def __init__(self, alphabet: Iterable, str_len: int, purge_after: bool = True, logger: Logger = init_logger()):
        self.alphabet = alphabet
        self.str_len = str_len
        self.purge_after = purge_after
        self.logger = logger

    def product(self):
        self.logger.info("[START] Combining started [START]")
        with Pool(processes=multiprocessing.cpu_count() - 1) as pool:
            result = pool.map(self._get_for_char, self.alphabet)
            self.logger.info("[PROCESS] List of filenames received [PROCESS]")
            for name in result:
                self.logger.info(f"[PROCESS] Extracting combinations from {name} [PROCESS]")
                with open("result.txt", mode="a") as file_result:
                    with open(name, mode="r") as producer:
                        file_result.write(producer.read())
        if self.purge_after:
            self.logger.info("[CLEANING] Purging created .txt files in storage [CLEANING]")
            Combinator.purge_files()
        self.logger.info("[END] All combinations created successfully. See result.txt file [END]")

    def _get_for_char(self, char) -> pathlib.Path:
        self.logger.info(f"[PROCESS] Processing char: {char} [PROCESS]")
        result = []
        file_name = STORAGE.joinpath(f"{uuid.uuid4()}.txt")
        for starter_combination in product(self.alphabet, repeat=self.str_len - 1):
            combination = [char]
            combination.extend(starter_combination)
            result.append(combination)
        with open(file_name, mode="w") as file:
            file.write(Combinator.writer(result) + "\n")
        return file_name

    @staticmethod
    def writer(result_list: list[list]) -> str:
        return "\n".join(["".join(el) for el in result_list])

    @staticmethod
    def purge_files():
        for file in STORAGE.glob("*.txt"):
            STORAGE.joinpath(file).unlink()


if __name__ == "__main__":
    # alphabet_for_combinations = ["a", "b", "c", "d", "e"]
    repeats = 5
    alphabet_for_combinations = ascii_lowercase + digits
    combinator = Combinator(alphabet_for_combinations, repeats, purge_after=False)
    combinator.product()
