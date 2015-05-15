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
        for group in groups(data, kwargs[facet], MAX_GROUPS[facet]):
            local_canvas = {}
            local_data = list(subset(data, kwargs[facet], group))
            for aesthetic in ['x', 'y', 'hue', 'brightness']:
                default = DEFAULT_AESTHETICS[aesthetic]
                local_canvas[aesthetic] = column(local_data, kwargs[aesthetic], default)

            canvas[facet].append(local_canvas)
    return canvas

#def build_frame(data, facet_key, facet_value

def subset(data, key, value):
    if value == None:
        return data
    else:
        return (row for row in data if row[key] == value)

def groups(data, key, max_groups):
    'Get groups for faceting.'
    if key:
        groups = set(row[key] for row in data)
        if len(groups) > max_groups:
            raise ValueError('Too many groups for the %s facet' % key)
        return sorted(groups)
    else:
        return [None]

def column(data, key, default):
    if key:
        return (row[key] for row in data)
    else:
        return itertools.repeat(default, len(data))


# data = list(csv.DictReader(open('../maluku/data/voyages.csv')))
# build_canvas(data, x = 'Tonnage', y = 'Tonnage', hue = None, brightness = None, stick1 = 'Place of departure', stick2 = 'Place of arrival', panel = 'Yard')
