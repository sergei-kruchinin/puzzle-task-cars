# Модуль используется для автоматического тестирования в car_test.py
# Модуль содержит три варианта функции для поиска всех решений для указанного количества красных и белых машин.
# Модуль содержит инструмент самопроверки -- сравнение трех вариантов поиска всех решений в цикле.
# Модуль также может использоваться источником кейсов для тестирования, ведь проще
# сгенерировать множество решений для кейса, и проверить вручную, чем изначально составлять ручками.
# Функции не стоит использовать для большого количества машин, примерно более чем 15 машин в сумме

import itertools
import time
import car


#
#


# на выходе -- множество решений
def car_placement_iter(rc, wc):
    '''
    Вариант перебора с использованием модуля iter
    генерируем всевозможные варианты и выдаем только подходящие
    :param rc: (int)  количество красных
    :param wc: (int) количество белых
    :return: set( str... ) множество решений или пустое множество
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
    # можно добавить единственное значение None, если пусто, но не будем пока
    return res


# Вариант перебора на основе итерации по комбинациям бинарных 0 и 1
# Функция перебирает только половину возможных решений, так как вторая половина получается инверсией 0 и 1
# итерация от 10..00 до 11..11 включительно. Это чуть оптимизированный вариант функции car_placement_enum2

# на выходе -- множество решений
def car_placement_enum(rc, wc):
    '''

    :param rc: (int) количество красных машин
    :param wc: (int) количество белых машин
    :return: set(str... ) множество решений или пустое множество
    '''

    if rc <= 0 or wc <= 0:
        return set()
    res = set()
    length = rc + wc
    start_point = 1 << (length - 1)  # 100..000
    end_point = 2 ** length  # число на единицу больше чем #111..111
    for i in range(start_point, end_point):
        example = format(i, f'#0{length + 2}b')[2:]
        if (example.count('0') == rc) or (example.count('0') == wc):
            # если 0 совпал, то 1 проверять не надо, так как варианты идентичны
            if (
                    not example.startswith('00') and not example.startswith('11') and
                    not example.endswith('00') and not example.endswith('11') and
                    '000' not in example and '111' not in example
            ):
                if example.count('0') == rc:
                    res.add(example.replace('0', 'R').replace('1', 'W'))
                    if rc == wc:  # симметричный вариант тоже добавим, когда число R==W
                        res.add(example.replace('1', 'R').replace('0', 'W'))
                else:
                    res.add(example.replace('1', 'R').replace('0', 'W'))
    # можно добавить единственное значение None, если пусто, но не будем пока
    return res


# Менее оптимизированный вариант перебора на основе итераций по комбинациям бинарных 0 и 1
# Вариант осуществляет перебор всех вариантов начиная с 01..00 до 11..11 (включительно)
# варианты ранее 01..00 (до 001..11 включительно) не проверяются так как заведомо не верные решения

# на выходе -- множество решений


def car_placement_enum2(rc, wc):
    '''

    :param rc: (int) количество красных машин
    :param wc: (int) количество белых машин
    :return: set(str...) множество решений (строк) или пустое множество
    '''
    if rc <= 0 or wc <= 0:
        return set()
    res = set()
    length = rc + wc
    start_point = 1 << (length - 2)  # 010..000
    end_point = 2 ** length  # число на единицу больше чем #111..111

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

    # можно добавить единственное значение None, если пусто, но не будем пока
    return res


# Далее уже проверки того, что получилось (самопроверка)


# Функция позволяет проверить диапазон входных условий.
# Осуществляется перебор всех вариантов каждой из трех функций перебора:
# x1, x2 -- диапазон значений Red; y1, y2 -- диапазон значений White.
# Если y1 == 0, то от текущего x до y2
# show=True показывать найденные множества, show=False нет
def car_placement_compare(x1, x2, y1, y2, show=False):
    success_count = 0
    fail_count = 0

    for i in range(x1, x2):
        # Если y1 == 0, то идем от i, чтобы не повторять идентичные, но инверсные расстановки
        y1_actual = i if y1 == 0 else y1
        for j in (y1_actual, y2):
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

            print(f'math_len: 1, enum_len: {len(res1)}, enum2_len: {len(res2)}, iter_Len: {len(res3)}')
            print(f'math_time: {time0} ms, enum_time: {time1} ms, enum2_time: {time2} ms, iter_time: {time3} ms')
            res_equal = res1 == res2 == res3
            print('enum_set==enum2_set==item_set:', res_equal)

            # сделаем проверку (в случае если три способа эквивалентны)
            # а собственно входит ли найденное математически решение во множество решений?
            # при этом если оба решения пустые (None и пустое множество)
            # то считаем что входит (изначально не входило в задумку)
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


# Функция служит для проверки этого модуля, используется при запуске непосредственно его как __main__
# (main для этого модуля)
# проверяем возможные варианты, чтобы не сильно долго
# собственно, написано для проверки этого модуля,
# сам же модуль необходим для car_test.py


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


# если запустили как
# python3 car_placement.py
# запускаем самопроверку


if __name__ == '__main__':
    main()

    # А правда ли, что 10 белых и 13 красных машин дают 4563 варианта расстановок согласно условию?
    # Проверим
    # res = car_placement_enum(10, 13)
    # c = 1
    # for i in res:
    #     print(c, i)
    #     c += 1
    # Оказывается, правда
