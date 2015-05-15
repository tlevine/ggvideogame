import itertools

DEFAULT_AESTHETICS = {
    'x': 0, 'y': 0,
    'hue': None,
    'brightness': 0.5,
}
MAX_GROUPS = {
    'stick1': 20,
    'stick2': 20,
    'panel': 4,
}

def ggvideogame(data, x = None, y = None, hue = None, brightness = None,
                stick1 = None, stick2 = None, panel = None):
    '''
    :param list data: Dataset, a list of dictionaries

    Everything else is either a column name (a key in the dictionaries)
    or None.
    '''
    canvas = {}
    for facet in ['stick1', 'stick2', 'panel']:
        canvas[facet] = []
        for group in groups(data, locals()[facet]):
            local_canvas = {}
            local_data = subset(data, locals()[facet], group)
            for aesthetic in ['x', 'y', 'hue', 'brightness']:
                local_canvas[aesthetic] = column(facet_data, locals()[aesthetic])
            canvas[facet].append(local_canvas)
    return canvas

def subset(data, key, value):
    return (row for row in data if row[key] == value)

def groups(data, key, max_groups = MAX_GROUPS):
    'Get groups for faceting.'
    groups = set(row[key] for row in data)
    if len(groups) > MAX_GROUPS:
        raise ValueError('Too many groups for the %s facet' % key)
    return sorted(groups)

def column(data, key, defaults = DEFAULT_AESTHETICS):
    if key:
        return (row[key] for row in data)
    else:
        return itertools.repeat(defaults[key], len(data))
