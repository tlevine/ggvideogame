import itertools
import collections

DEFAULT_AESTHETICS = {
    'x': 0, 'y': 0,
    'hue': None,
    'brightness': 0.5,
}
MAX_GROUPS = {
    'stick1': 100,
    'stick2': 100,
    'panel': 4,
}
LIMITS = {
    'x': 30,
    'y': 20,
    'hue': 1,
    'brightness': 1,
}

def ggvideogame(df, x = None, y = None, hue = None, brightness = None,
                panel = None, stick1 = None, stick2 = None):
    '''
    :param pandas.DataFrame df: Dataset

    x, y, hue, and brightness must be numeric columns.
    panel, stick1, and stick2 must have an order.

    Everything else is either a column name (a key in the dictionaries)
    or None.
    '''

    # Determine limits.
    def frame(panel_value, stick1_value, stick2_value, limits = LIMITS):
        '''
        Subset the particular frame. Use None to get everything.
        '''
        # Select the data for a particular facet.
        selector = True
        factor_levels = [(panel, panel_value), (stick1, stick1_value), (stick2, stick2_value)]
        for factor, level in factor_levels:
            if level:
                selector = selector & (df[factor] == level)
        
        return {colname: scale(df[colname],
                               df[selector][colname],
                               LIMITS[colname]) for colname in LIMITS.keys()}

def scale(column, subcolumn, n):
    normalized = (subcolumn - column.min()) / (column.max() - column.min())
    return (normalized * (n - 1)).round()
