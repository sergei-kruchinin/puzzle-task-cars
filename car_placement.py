# The module is used for automatic testing in car_test.py
# The module contains three variations of functions for finding all solutions for a given number of red and white cars.
# The module contains a self-validation tool that compares the three variations for finding all solutions in a loop.
# The module can also be used as a source of test cases since it is easier
# to generate a set of solutions for a case and manually verify them rather than manually creating them initially.
# The functions should not be used for a large number of cars, roughly more than 15 cars in total.

import itertools
import time
import car

# output -- set of solutions
def car_placement_iter(rc, wc):
    '''
    Variation of enumeration using the iter module
    generate all possible options and yield only suitable ones
    :param rc: (int) number of red cars
    :param wc: (int) number of white cars
    :return: set( str... ) set of solutions or empty set
    '''
    if rc <= 0 or wc <= 0:
        return set()

    res = set()
    for i in itertools.product('RW', repeat=rc + wc):
        example = ''.join(i)
        if (
                example.count('R') == rc and example.count('W') and
                not example.startswith('RR') and not example.startswith('WW') and
                not example.endswith('RR') and not example.endswith('WW') and
                ('RRR' not in example) and
                ('WWW' not in example)
        ):
            res.add(str(example))
    # we can add a single None value if empty, but we won't for now
    return res

# Enumeration variant based on iteration over combinations of binary 0 and 1
# The function enumerates only half of the possible solutions since the second half is obtained by inverting 0 and 1
# iteration from 10..00 to 11..11 inclusive. This is a slightly optimized version of the car_placement_enum2 function

# output -- set of solutions
def car_placement_enum(rc, wc):
    '''

    :param rc: (int) number of red cars
    :param wc: (int) number of white cars
    :return: set( str... ) set of solutions or empty set
    '''

    if rc <= 0 or wc <= 0:
        return set()
    res = set()
    length = rc + wc
    start_point = 1 << (length - 1)  # 100..000
    end_point = 2 ** length  # number one greater than #111..111
    for i in range(start_point, end_point):
        example = format(i, f'#0{length + 2}b')[2:]
        if (example.count('0') == rc) or (example.count('0') == wc):
            # if 0 matches, then 1 does not need to be checked, as the options are identical
            if (
                    not example.startswith('00') and not example.startswith('11') and
                    not example.endswith('00') and not example.endswith('11') and
                    '000' not in example and '111' not in example
            ):
                if example.count('0') == rc:
                    res.add(example.replace('0', 'R').replace('1', 'W'))
                    if rc == wc:  # add a symmetric variant too, when the number of R == W
                        res.add(example.replace('1', 'R').replace('0', 'W'))
                else:
                    res.add(example.replace('1', 'R').replace('0', 'W'))
    # we can add a single None value if empty, but we won't for now
    return res


# Less optimized version of enumeration based on iteration over combinations of binary 0 and 1
# This variant iterates over all options starting from 01..00 to 11..11 (inclusive)
# options earlier than 01..00 (up to 001..11 inclusive) are not checked as they are obviously invalid solutions

# output -- set of solutions
def car_placement_enum2(rc, wc):
    '''

    :param rc: (int) number of red cars
    :param wc: (int) number of white cars
    :return: set(str...) set of solutions (strings) or empty set
    '''
    if rc <= 0 or wc <= 0:
        return set()
    res = set()
    length = rc + wc
    start_point = 1 << (length - 2)  # 010..000
    end_point = 2 ** length  # number one greater than #111..111

    for i in range(start_point, end_point):
        example = format(i, f'#0{length + 2}b')[2:]
        if (example.count('0') == rc) or (example.count('1') == wc):
            if (
                    not example.startswith('00') and not example.startswith('11') and
                    not example.endswith('00') and not example.endswith('11') and
                    '000' not in example and '111' not in example
            ):
                if example.count('0') == rc:
                    res.add(example.replace('0', 'R').replace('1', 'W'))
                else:
                    res.add(example.replace('1', 'R').replace('0', 'W'))

    # we can add a single None value if empty, but we won't for now
    return res

# Further checks of what we got (self-validation)

# The function allows checking the range of input conditions.
# Iterates over all options of each of the three enumeration functions:
# x1, x2 -- range of Red values; y1, y2 -- range of White values.
# If y1 == 0, then iterate from the current x to y2
# show=True to display the found sets, show=False to hide them
def car_placement_compare(x1, x2, y1, y2, show=False):
    success_count = 0
    fail_count = 0

    for i in range(x1, x2):
        # If y1 == 0, iterate from i to avoid repeating identical inverted arrangements
        y1_actual = i if y1 == 0 else y1
        for j in range(y1_actual, y2):
            print(f'R={i}, W={j}')

            time_start = time.perf_counter()
            example = car.car_placement_math(i, j)
            time_end = time.perf_counter()
            time0 = round((time_end - time_start) * 1000)

            time_start = time.perf_counter()
            res1 = car_placement_enum(i, j)
            time_end = time.perf_counter()
            time1 = round((time_end - time_start) * 1000)
            if show:
                print('enum:', res1)

            time_start = time.perf_counter()
            res2 = car_placement_enum2(i, j)
            time_end = time.perf_counter()
            time2 = round((time_end - time_start) * 1000)
            if show:
                print('enu2:', res2)

            time_start = time.perf_counter()
            res3 = car_placement_iter(i, j)
            time_end = time.perf_counter()
            time3 = round((time_end - time_start) * 1000)
            if show:
                print('iter:', res3)

            print(f'math_len: 1, enum_len: {len(res1)}, enum2_len: {len(res2)}, iter_len: {len(res3)}')
            print(f'math_time: {time0} ms, enum_time: {time1} ms, enum2_time: {time2} ms, iter_time: {time3} ms')
            res_equal = res1 == res2 == res3
            print('enum_set==enum2_set==item_set:', res_equal)

            # check if the three methods are equivalent
            # whether the mathematically found solution is in the set of solutions?
            # if both solutions are empty (None and empty set)
            # consider it as included (initially it was not considered included)
            if res_equal:
                if (
                        (example is None and len(res1) == 0) or
                        (example in res1)
                ):
                    print(f"Math solution '{example}' is in enum_set")
                    success_count += 1
                else:
                    print(f"Math solution '{example}' is not in enum_set")
                    fail_count += 1
            else:
                fail_count += 1
    return success_count, fail_count

# The function is used to test this module when run as __main__
# check possible options to avoid long-running tests
# written to verify this module,
# which is necessary for car_test.py


def main():
    success_count, fail_count = car_placement_compare(1, 7, 1, 7, show=True)
    print('Success count:', success_count)
    print('Fail count:', fail_count)

    success_count2, fail_count2 = car_placement_compare(7, 11, 0, 13)

    print('Success count:', success_count2)
    print('Fail count:', fail_count2)
    print('Total\n' + '=' * 5)
    print('Success count:', success_count + success_count2)
    print('Fail count:', fail_count + fail_count2)


# if run as
# python3 car_placement.py
# run self-validation
if __name__ == '__main__':
    main()

    # Is it true that 10 white and 13 red cars produce 4563 placement options according to the condition?
    # Let's check
    # res = car_placement_enum(10, 13)
    # c = 1
    # for i in res:
    #     print(c, i)
    #     c += 1
    # It turns out, it's true
