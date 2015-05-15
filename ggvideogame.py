import itertools
import collections

DEFAULT_AESTHETICS = {
    'x': 0, 'y': 0,
    'hue': None,
    'brightness': 0.5,
}
MAX_GROUPS = {
    'stick1': 50,
    'stick2': 50,
    'panel': 4,
}

def ggvideogame(data, x = None, y = None, hue = None, brightness = None,
                stick1 = None, stick2 = None, panel = None):
    '''
    :param list data: Dataset, a list of dictionaries

    Everything else is either a column name (a key in the dictionaries)
    or None.
    '''

def build_canvas(data, **kwargs):
    canvas = collections.defaultdict(list)
    for facet in ['stick1', 'stick2', 'panel']:
        for group in groups(data, facet, kwargs[facet]):
            local_canvas = {}
            local_data = subset(data, kwargs[facet], group)
            for aesthetic in ['x', 'y', 'hue', 'brightness']:
                local_canvas[aesthetic] = column(local_data, kwargs[aesthetic])

            canvas[facet].append(local_canvas)
    return canvas

#def build_frame(data, facet_key, facet_value

def subset(data, key, value):
    return (row for row in data if row[key] == value)

def groups(data, facet, key, max_groups = MAX_GROUPS):
    'Get groups for faceting.'
    groups = set(row[key] for row in data)
    if len(groups) > MAX_GROUPS[facet]:
        raise ValueError('Too many groups for the %s facet' % key)
    return sorted(groups)

def column(data, aesthetic, key, defaults = DEFAULT_AESTHETICS):
    if key:
        return (row[key] for row in data)
    else:
        return itertools.repeat(defaults[key], len(data))


# data = list(csv.DictReader(open('../maluku/data/voyages.csv')))
# build_canvas(data, x = 'Tonnage', y = 'Tonnage', hue = None, brightness = None, stick1 = 'Place of departure', stick2 = 'Place of arrival', panel = 'Yard')
