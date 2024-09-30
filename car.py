# Problem Solution
# It is self-contained; other modules are for testing

def car_placement_math(rc, wc):
    '''
    Function to find a mathematical solution (only one!)

    :param rc: (int) number of red cars (red count)
    :param wc: (int) number of white cars (white count)
    :return: (str) solution string or None if no solution exists.
    '''

    # First, handle exceptions.
    # Characters and floats will cause an error,
    # we won't handle them here; an error is the correct behavior in this case.

    # Floats can be handled with:
    # rc, wc = int(rc), int(wc)  # But this could lead to unexpected behavior. So we won't.

    # Tests showed that 0, 0 and negative values are processed and '' is returned instead of None,
    # but this is implicit and unpredictable behavior,
    # so we will handle these cases explicitly
    if rc <= 0 or wc <= 0:
        return None

    # First, define the patterns for tiling the row with R and W symbols
    if rc < wc:  # to avoid calculating twice when differences are in mutual replacement of R and W, we switch the tiling patterns
        rc, wc = wc, rc
        rw = 'WR'  # pattern when one car of one color is followed by a car of another color
        rwr = 'WRW'  # pattern when one car of one color is followed by two cars of another color
    else:  # here the patterns remain the same
        rw, rwr = 'RW', 'RWR'

    # Calculate the tiling option -- let's start counting:
    if rc == wc:  # if there are equal numbers of red and white cars: RW pattern
        res = rw * rc
    elif rc == 2 * wc:  # if one type is exactly twice as many as the other: RWR pattern
        res = rwr * wc
    elif rc - wc < rc / 2:  # if between n and 2n: use a combination of two patterns
        res = rw * (2 * wc - rc) + rwr * (rc - wc)
    else:  # Other options are not suitable -- no solution
        res = None
    return res


def main():
    # input two numbers, red cars X and white cars Y
    # the output is a string containing X -- R and Y -- W without spaces,
    # such that with one car of one color there is at least one car of another color next to it
    # important -- only one suitable solution is found
    x = int(input('Enter the number of red cars, X='))
    y = int(input('Enter the number of white cars, Y='))
    res = car_placement_math(x, y)
    print(res if res is not None else 'No solution')


if __name__ == '__main__':
    main()
