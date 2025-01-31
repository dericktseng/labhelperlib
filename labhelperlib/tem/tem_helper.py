def unit_multiplier(given, convert):
    """
    given - original units (e.g. 'c' for cm)
    convert - new units (e.g. 'u' for um)
    empty string for just 'm'
    """
    units = {
        'M':  6,
        'K':  3,
        '' :  0,
        'c': -2,
        'm': -3,
        'u': -6,
        'n': -9,
        'p': -12
    }
    return 10**(units[given] - units[convert])

