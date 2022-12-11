from time import time
from multiprocessing import Pool, cpu_count


def factorize(*number) -> dict:
    output = {}
    for i in number:
        division_numbers = []
        min_count = 1

        while min_count <= i:
            if i % min_count == 0:
                division_numbers.append(min_count)
                min_count += 1
            else:
                min_count += 1

        output[i] = division_numbers

    return output


if __name__ == '__main__':
    processors = cpu_count()
    t1 = time()
    result = factorize(128, 255, 99999, 10651060)
    print(f'час виконання лінійно: {time() - t1}')
    print(result)
    t2 = time()
    pool = Pool(processors)
    result = pool.apply_async(factorize, (128, 255, 99999, 10651060))
    print(f'час виконання на {processors} процесорах {time() - t2}')
    print(result.get())

'''
час виконання лінійно: 0.6330089569091797 
{128: [1, 2, 4, 8, 16, 32, 64, 128], 255: [1, 3, 5, 15, 17, 51, 85, 
255], 99999: [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999], 10651060: [1, 2, 4, 5, 7, 10, 14, 20, 28, 
35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]} 

час виконання на 16 процесорах 0.10199809074401855 
{128: [1, 2, 4, 8, 16, 32, 64, 128], 255: [1, 3, 5, 15, 17, 51, 
85, 255], 99999: [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999], 10651060: [1, 2, 4, 5, 7, 10, 14, 20, 
28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 
10651060]} 
'''
