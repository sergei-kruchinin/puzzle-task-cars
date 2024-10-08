import unittest
import car_placement
import car

class CarTest(unittest.TestCase):

    # Testing found solutions using the car_placement module, which solves the problem differently
    # That's what it was written for
    # Do not use it for a large number of cars (more than 15 in total)
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

    # Testing invalid input values that are integers but not valid within the problem context
    def test_is_not_valid_input(self):
        self.assertIsNone(car.car_placement_math(0, 0))
        self.assertIsNone(car.car_placement_math(1, 0))
        self.assertIsNone(car.car_placement_math(-10, -10))
        self.assertIsNone(car.car_placement_math(-10, 0))
        # Applied corrections based on the results!

    # Are we wrong in full enumeration functions written for verification? ###
    # def test_is_not_valid_for_car_placement(self):
    #     self.assertEqual(car_placement.car_placement_enum(0, 0), set())
    #     self.assertEqual(car_placement.car_placement_enum(1, 0), set())
    #     self.assertEqual(car_placement.car_placement_enum(-10, -10), set())
    #     self.assertEqual(car_placement.car_placement_enum(-10, 0), set())
    # Added <=0 handling and calmed down for now ###

    # Check cases where there is no solution
    def test_is_none_decisions(self):
        self.assertIsNone(car.car_placement_math(1, 10))
        self.assertIsNone(car.car_placement_math(17, 8))
        self.assertIsNone(car.car_placement_math(10, 21))
        self.assertIsNone(car.car_placement_math(10, 30))
        self.assertIsNone(car.car_placement_math(1, 3))

    # Check (not universal) that a known solution is still output
    # Use with caution since it provides only one value, may not match another valid solution
    def test_equal_to_known_decisions(self):
        # Here you need to consider the pattern used for generation and the ratio R >= W
        self.assertEqual(car.car_placement_math(1, 1), 'RW')
        self.assertEqual(car.car_placement_math(1, 2), 'WRW')
        # Best for testing large values, which cannot be verified with car_placement
        self.assertEqual(car.car_placement_math(4, 4), 'RWRWRWRW')
        self.assertEqual(car.car_placement_math(8, 4), 'RWRRWRRWRRWR')
        self.assertEqual(car.car_placement_math(10, 10), 'RW' * 10)
        self.assertEqual(car.car_placement_math(20, 10), 'RWR' * 10)

    # On some variants of correct answers. The downside is that a very large set cannot be specified,
    # but this is for testing with car_placement, see above
    def test_decision_in_known_decisions_sets(self):
        self.assertIn(car.car_placement_math(1, 1), {'RW', 'WR'})
        self.assertIn(car.car_placement_math(2, 2), {'RWRW', 'WRWR', 'WRRW', 'RWWR'})
        self.assertIn(car.car_placement_math(3, 5), {'WRWRWWRW', 'RWWRWWRW', 'WRWWRWRW', 'WRWWRWWR'})
        self.assertIn(car.car_placement_math(3, 3), {
            'RWWRRW', 'RWRWWR', 'WRRWRW', 'WRRWWR',
            'RWWRWR', 'WRWRRW', 'WRWRWR', 'RWRWRW'})

    # Next:
    # Tests for the count (R matches, W matches)
    # Tests for compliance with rules (no RR or WW at the start and end, no RRR WWW in the middle)
    # Tests for the length of the solution.
    # They won't work if there's no solution.
    # These tests are suitable for a very large number of cars

    # Test that there's no RR or WW on the left
    # Will give an error if there's no solution, solutions are assumed here
    def test_left_condition(self):
        self.assertNotIn(car.car_placement_math(3, 5)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 5)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(10, 20)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 15)[0:2], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(800, 815)[0:2], {'RR', 'WW'})

    # Test that there's no RR or WW on the right
    # Will give an error if there's no solution, solutions are assumed here
    def test_right_condition(self):
        self.assertNotIn(car.car_placement_math(3, 5)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 5)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(10, 20)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(8, 15)[-2:], {'RR', 'WW'})
        self.assertNotIn(car.car_placement_math(500, 600)[-2:], {'RR', 'WW'})

    # Test that there are no three red cars in a row
    def test_no_lonely_red_in_the_middle(self):
        self.assertEqual(car.car_placement_math(3, 5).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(3, 3).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(10, 20).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(10, 15).count('RRR'), 0)
        self.assertEqual(car.car_placement_math(3000, 3020).count('RRR'), 0)

    # Test that there are no three white cars in a row
    def test_no_lonely_white_in_the_middle(self):
        self.assertEqual(car.car_placement_math(3, 5).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(3, 3).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(10, 20).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(10, 15).count('WWW'), 0)
        self.assertEqual(car.car_placement_math(2000, 2100).count('WWW'), 0)

    # Test that the number of red cars matches the solution
    def test_red_count(self):
        self.assertEqual(car.car_placement_math(3, 5).count('R'), 3)
        self.assertEqual(car.car_placement_math(5, 5).count('R'), 5)
        self.assertEqual(car.car_placement_math(10, 20).count('R'), 10)
        self.assertEqual(car.car_placement_math(20, 40).count('R'), 20)
        self.assertEqual(car.car_placement_math(2000, 2040).count('R'), 2000)

    # Test that the number of white cars matches the solution
    def test_white_count(self):
        self.assertEqual(car.car_placement_math(3, 5).count('W'), 5)
        self.assertEqual(car.car_placement_math(4, 8).count('W'), 8)
        self.assertEqual(car.car_placement_math(20, 10).count('W'), 10)
        self.assertEqual(car.car_placement_math(15, 14).count('W'), 14)
        self.assertEqual(car.car_placement_math(2000, 2060).count('W'), 2060)

    # Test that the length of the solution matches R+W
    def test_length(self):
        self.assertEqual(len(car.car_placement_math(3, 5)), 3 + 5)
        self.assertEqual(len(car.car_placement_math(4, 8)), 4 + 8)
        self.assertEqual(len(car.car_placement_math(20, 10)), 20 + 10)
        self.assertEqual(len(car.car_placement_math(15, 14)), 15 + 14)
        self.assertEqual(len(car.car_placement_math(2000, 2050)), 2000 + 2050)

# To run the test, you need to execute the command:
# python3 -m unittest car_test.py
# or simply:
# python3 car_test.py
# thanks to the line:
if __name__ == "__main__":
    unittest.main()
