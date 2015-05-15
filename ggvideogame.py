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

def ggvideogame(df, x = None, y = None, hue = None, brightness = None,
                stick1 = None, stick2 = None, panel = None):
    '''
    :param pandas.DataFrame df: Dataset

    Everything else is either a column name (a key in the dictionaries)
    or None.
    '''

    # Determine limits.
    for aesthetic

    # Select the data for a particular facet.
    selector = True
    for factor, level in [('stick1', stick1), ('stick2', stick2), ('panel', panel)]:
        if level:
            selector = selector & (df[factor] == level)

def build_canvas(data, **kwargs):
    canvas = collections.defaultdict(list)
    for group in groups(data, kwargs['stick1'], kwargs['stick2'], kwargs['panel']):
        stick1, stick2, panel = group
        wheres = {
            kwargs['stick1']: stick1,
            kwargs['stick2']: stick2,
            kwargs['panel']: panel,
        }
        local_data = list(subset(data, wheres))
        local_canvas = {}
        for aesthetic in ['x', 'y', 'hue', 'brightness']:
            default = DEFAULT_AESTHETICS[aesthetic]
            local_canvas[aesthetic] = list(column(local_data, kwargs[aesthetic], default))

        canvas[group].append(local_canvas)
    return dict(canvas)
