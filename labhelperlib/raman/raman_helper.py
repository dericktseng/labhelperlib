import numpy as np

def gauss(x, a, b, c):
    # FWHM: 2 * sqrt(2 * ln(2)) * c
    return a * np.exp(-(x-b)**2 / (2*c**2))

def gauss_data(a,b,c):
    fwhm = abs(2 * np.sqrt(2 * np.log(2)) * c)
    height = a
    pos = b
    return pos, fwhm, height

def nearest_index(arr: np.ndarray, n: float):
    """ Returns the index of the number in `arr` closest to `n` """
    diff_arr = np.abs(arr - n)
    return np.argmin(diff_arr)

def max_in_range(x_arr: np.ndarray,
                 y_arr: np.ndarray,
                 low: float,
                 hi: float):
    """
    Returns the index of the max item in a specific range of given plot.
    x_arr: x values to check range
    y_arr: y values to check maximum
    low: lower limit of range
    hi: upper limit of range
    """
    low_i = nearest_index(x_arr, low)
    hi_i = nearest_index(x_arr, hi)
    check_arr = y_arr[low_i:hi_i + 1]
    max_i = np.argmax(check_arr)
    return max_i + low_i

def integrate_in_range(x_arr: np.ndarray,
                       y_arr: np.ndarray,
                       low: float,
                       hi: float):
    """
    Returns the integral of the function defined by x_arr, y_arr
    in the range (low, hi)
    """
    low_i = nearest_index(x_arr, low)
    hi_i = nearest_index(x_arr, hi)
    area = 0
    if y_arr.ndim == 1:
        area = np.trapezoid(y_arr[low_i:hi_i], x_arr[low_i:hi_i])
    elif y_arr.ndim == 2:
        area = np.trapezoid(y_arr[:,low_i:hi_i], x_arr[low_i:hi_i])
    return area


def connect_final_init_pt(arr: np.ndarray, set_final_pt=None):
    if set_final_pt is None:
        return np.concatenate((arr, [arr[0]]))
    else:
        return np.concatenate((arr, [set_final_pt]))

def generate_posts(points):
    frontpad = points[0] - (points[1] - points[0])
    backpad = points[-1] + (points[-1] - points[-2])
    padded = np.concatenate([[frontpad], points, [backpad]])
    return (padded[1:] + padded[:-1]) / 2

def cut(x_arr: np.ndarray,
        y_arr: np.ndarray,
        low: float,
        hi: float):
    """
    Returns a tuple (x_arr, y_arr) where the all datapoints in the
    new x_arr is between low and hi, and y_arr
    is cut to the same range.
    """
    sel_range = np.logical_and(low < x_arr, x_arr < hi)
    return x_arr[sel_range], y_arr[sel_range]
