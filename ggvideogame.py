import itertools
import collections

import pandas

DEFAULTS = {
    'x': 0, 'y': 0,
    'hue': None,
    'brightness': 0.5,
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

    aesthetics = {
        'x': x,
        'y': y,
        'hue': hue,
        'brightness': brightness,
    }

    # Determine limits.
    def frame(panel_value, stick1_value, stick2_value,
              limits = LIMITS, defaults = DEFAULTS):
        '''
        Subset the particular frame. Use None to get everything.
        '''
        # Select the data for a particular facet.
        selector = pandas.Series(list(itertools.repeat(True, df.shape[0])))
        factor_levels = [(panel, panel_value), (stick1, stick1_value), (stick2, stick2_value)]
        for factor, level in factor_levels:
            if level:
                selector = selector & (df[factor] == level)
        
        # Defaults
        df_subset = pandas.DataFrame()
        for aesthetic in limits.keys():
            default_column = list(itertools.repeat(defaults[aesthetic], selector.sum()))
            df_subset[aesthetic] = pandas.Series(default_column)

        for aesthetic in limits.keys():
            if aesthetics[aesthetic]:
                df_subset[aesthetic] = scale(df[aesthetics[aesthetic]],
                                             df[selector][aesthetics[aesthetic]],
                                             limits[aesthetic])

        return df_subset
    
    return frame

def scale(column, subcolumn, n):
    normalized = (subcolumn - column.min()) / (column.max() - column.min())
    return (normalized * (n - 1)).round()
