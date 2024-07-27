import unittest
import car_placement
import car


class CarTest(unittest.TestCase):

    # тестирование найденных решений с помощью модуля car_placement, решающего задачу по другому
    # для этого он и был написан
    # Не стоит использовать для большого количества машин (больших чем 15 в сумме)
    def test_in_set_by_enum(self):
        self.assertIn(car.car_placement_math(5, 5), car_placement.car_placement_enum(5, 5))
        self.assertIn(car.car_placement_math(5, 10), car_placement.car_placement_enum(5, 10))
        self.assertIn(car.car_placement_math(5, 8), car_placement.car_placement_enum(5, 8))
        self.assertIn(car.car_placement_math(10, 5), car_placement.car_placement_enum(10, 5))
        self.assertIn(car.car_placement_math(8, 5), car_placement.car_placement_enum(8, 5))

    def test_in_set_by_iter(self):
        self.assertIn(car.car_placement_math(3, 3), car_placement.car_placement_iter(3, 3))
        self.assertIn(car.car_placement_math(3, 5), car_placement.car_placement_iter(3, 5))
        self.assertIn(car.car_placement_math(3, 6), car_placement.car_placement_iter(3, 6))
        self.assertIn(car.car_placement_math(5, 3), car_placement.car_placement_iter(5, 3))
        self.assertIn(car.car_placement_math(5, 6), car_placement.car_placement_iter(5, 6))

    # проверки на int, но не валидные в рамках задачи значения
    def test_is_not_valid_input(self):
        self.assertIsNone(car.car_placement_math(0, 0))
        self.assertIsNone(car.car_placement_math(1, 0))
        self.assertIsNone(car.car_placement_math(-10, -10))
        self.assertIsNone(car.car_placement_math(-10, 0))
        # по итогам внесли правки!

    # А не ошиблись мы в самих функциях полного перебора, написанных для проверки? ###
    # def test_is_not_valid_for_car_placement(self):
    #     self.assertEqual(car_placement.car_placement_enum(0, 0), set())
    #     self.assertEqual(car_placement.car_placement_enum(1, 0), set())
    #     self.assertEqual(car_placement.car_placement_enum(-10, -10), set())
    #     self.assertEqual(car_placement.car_placement_enum(-10, 0), set())
    # добавили обработку <=0 и успокоились пока на этом ###

    # проверка на те случаи, когда решения нет
    def test_is_none_decisions(self):
        self.assertIsNone(car.car_placement_math(1, 10))
        self.assertIsNone(car.car_placement_math(17, 8))
        self.assertIsNone(car.car_placement_math(10, 21))
        self.assertIsNone(car.car_placement_math(10, 30))
        self.assertIsNone(car.car_placement_math(1, 3))

    # проверка (не универсальная) на то, что известное решение по-прежнему выдается
    # применять с осторожностью, так как дает только одно значение, может не совпадать с другим верным решением
    def test_equal_to_known_decisions(self):
        # тут нужно учитывать паттерн, который используется в генерации и соотношение R >= W
        self.assertEqual(car.car_placement_math(1, 1), 'RW')
        self.assertEqual(car.car_placement_math(1, 2), 'WRW')
        # больше всего подойдет для проверки больших значений, которых с car_placement не проверить
        self.assertEqual(car.car_placement_math(4, 4), 'RWRWRWRW')
        self.assertEqual(car.car_placement_math(8, 4), 'RWRRWRRWRRWR')
        self.assertEqual(car.car_placement_math(10, 10), 'RW' * 10)
        self.assertEqual(car.car_placement_math(20, 10), 'RWR' * 10)

    # На некоторых вариантах правильных ответов. Недостаток -- сильно большое множество не задашь, но для
    # этого тестирование с car_placement, см. выше
    def test_desisio_in_known_decisions_sets(self):
        self.assertIn(car.car_placement_math(1, 1), {'RW', 'WR'})
        self.assertIn(car.car_placement_math(2, 2), {'RWRW', 'WRWR', 'WRRW', 'RWWR'})
        self.assertIn(car.car_placement_math(3, 5), {'WRWRWWRW', 'RWWRWWRW', 'WRWWRWRW', 'WRWWRWWR'})
        self.assertIn(car.car_placement_math(3, 3), {
            'RWWRRW', 'RWRWWR', 'WRRWRW', 'WRRWWR',
            'RWWRWR', 'WRWRRW', 'WRWRWR', 'RWRWRW'})

    # Далее:
    #  Проверки на подсчет (что R совпадает, W совпадает)
    #  Проверки на соответствие правилу (нет RR или WW вначале и конце, RRR WWW в середине)
    #  И проверки на длину решения.
    #  Не сработают, если решения нет.
    #  Эти проверки подойдут для очень большого количества машин

    # Проверка, что слева нет RR или WW
    # Если решений нет, выдаст ошибку, здесь заведомо решения есть
    def test_left_condition(self):
        self.assertNotIn(car.car_placement_math(3, 5)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 5)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(10, 20)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 15)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(800, 815)[0:2], {'RR', 'WW'})

    # Проверка, что справа нет RR или WW
    # Если решений нет, выдаст ошибку, здесь заведомо решения есть
    def test_right_condition(self):
        self.assertNotIn(car.car_placement_math(3, 5)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 5)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(10, 20)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 15)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(500, 600)[-2:], {'RR', 'WW'})

    # Проверка, что нет трех красных подряд машин
    def test_no_lonely_red_in_the_middle(self):
        self.assertEqual(car.car_placement_math(3, 5).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(3, 3).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(10, 20).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(10, 15).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(3000, 3020).count('RRR'), 0)

    # Проверка, что нет трех белых подряд машин
    def test_no_lonely_white_in_the_middle(self):
        self.assertEqual(car.car_placement_math(3, 5).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(3, 3).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(10, 20).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(10, 15).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(2000, 2100).count('WWW'), 0)

    # Проверка, что количество красных соответствует решению
    def test_red_count(self):
        self.assertEqual(car.car_placement_math(3, 5).count('R'), 3)
        self.assertEqual(car.car_placement_math(5, 5).count('R'), 5)
        self.assertEqual(car.car_placement_math(10, 20).count('R'), 10)
        self.assertEqual(car.car_placement_math(20, 40).count('R'), 20)
        self.assertEqual(car.car_placement_math(2000, 2040).count('R'), 2000)

    # Проверка, что количество белых соответствует решению
    def test_white_count(self):
        self.assertEqual(car.car_placement_math(3, 5).count('W'), 5)
        self.assertEqual(car.car_placement_math(4, 8).count('W'), 8)
        self.assertEqual(car.car_placement_math(20, 10).count('W'), 10)
        self.assertEqual(car.car_placement_math(15, 14).count('W'), 14)
        self.assertEqual(car.car_placement_math(2000, 2060).count('W'), 2060)

    # Проверка, что длина решения соответствует R+W
    def test_length(self):
        self.assertEqual(len(car.car_placement_math(3, 5)), 3 + 5)
        self.assertEqual(len(car.car_placement_math(4, 8)), 4 + 8)
        self.assertEqual(len(car.car_placement_math(20, 10)), 20 + 10)
        self.assertEqual(len(car.car_placement_math(15, 14)), 15 + 14)
        self.assertEqual(len(car.car_placement_math(2000, 2050)), 2000 + 2050)


# Чтобы запустить тест, нужно выполнить команду:
# python3 -m unittest car_test.py
# или даже просто:
# python3 car_test.py
# благодаря строке:
if __name__ == "__main__":
    unittest.main()
