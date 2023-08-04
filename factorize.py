import concurrent.futures
import logging
from multiprocessing import cpu_count
from time import time


def factorize(*number):
    results = []
    for num in number:
        divisors = [i for i in range(1, num + 1) if num % i == 0]
        results.append(divisors)
    print(results)
    return results


def measure_factorize_time():
    start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    logging.debug("Time taken: {:10f} sec".format(time() - start))


def measure_multiprocess_factorize_time():
    start = time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        a, b, c, d = list(executor.map(factorize, (128, 255, 99999, 10651060)))
    logging.debug("Multiprocess time: {:10f} sec".format(time() - start))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    measure_factorize_time()
    print(f"Count cpu: {cpu_count()}")
    measure_multiprocess_factorize_time()
