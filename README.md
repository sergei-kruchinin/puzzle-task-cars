# Car Placement Program

## Description
The program is designed to solve the problem of placing red and white cars in a row such that each car of one color is adjacent to a car of the other color. It also provides functions for finding all possible solutions and for testing them.

## Project Structure
- `car.py`: Main file containing the solution to the problem.
- `car_placement.py`: Module for automated testing and finding all possible solutions.
- `car_test.py`: Module for unit testing.
- [rus](rus) Russian-language version
## How to Run
1. Ensure you have Python 3.x installed.
2. Download or clone the repository.
3. Navigate to the project directory.

### Running the Main Script
Run the `car.py` script:
   ```sh
   python car.py
   ```

### Running Tests
Run the automated testing module:
   ```sh
   python car_placement.py
   ```
Run the unit testing module:
   ```sh
   python -m unittest car_test.py
   ```
   or simply:
   ```sh
   python car_test.py
   ```

## Usage
### `car.py`
When you run the script, the program will prompt you to input the number of red and white cars:
```
Enter the number of red cars, X=
Enter the number of white cars, Y=
```
After entering the values, the program will output a string representing the car placement or will notify you if no solution exists.

Example:
```
Enter the number of red cars, X=3
Enter the number of white cars, Y=2
Output: RWRWR
```

### `car_placement.py`
This module can be used for automated testing and finding all possible solutions to the problem.

#### Functions
- `car_placement_iter(rc, wc)`
- `car_placement_enum(rc, wc)`
- `car_placement_enum2(rc, wc)`

All these functions take the number of red and white cars and return a set of strings representing all possible solutions.

#### Testing and Self-Validation
Run the main tests and self-validation by executing `car_placement.py`:
```sh
python car_placement.py
```
This command will perform some checks and comparisons of the sets of solutions obtained by different methods.

### `car_test.py`
This module is intended for unit testing of functions.
To run the tests, use the command:
```sh
python -m unittest car_test.py
```
or simply:
```sh
python car_test.py
```
