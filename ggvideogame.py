#!/usr/bin/env python2
import itertools
import collections

import pygame, led
import pandas

PANEL_WIDTH = 20
PANEL_HEIGHT = 20
PANEL_Y = 0
def panel_x(panel_number):
    '''
    Panel number starts at 0.
    '''
    return 1 + (panel_number * (2 + PANEL_WIDTH))

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

def example():
    df = pandas.io.parsers.read_csv('~/git/maluku/data/voyages.csv')
    df = df[(df['Yard'] == 'Amsterdam') | (df['Yard'] == 'Zeeland')]

    ggvideogame(df, panel = 'Yard')

def ggvideogame(df, serial_port = None, fallback_size = (90, 20),
                x = None, y = None, hue = None, brightness = None,
                panel = None, stick1 = None, stick2 = None, _return_frame = False):
    '''
    :param pandas.DataFrame df: Dataset

    x, y, hue, and brightness must be numeric columns.
    panel, stick1, and stick2 must have an order.

    Everything else is either a column name (a key in the dictionaries)
    or None.
    '''
    led_display = led.teensy.TeensyDisplay(serial_port, fallback_size)
    size = led_display.size()
    max_panels = size[0] / PANEL_WIDTH # These are ints, so they round down.
    simulated_display = led.sim.SimDisplay(size)
    screen = pygame.Surface(size)

    frame = build_frame(df, x, y, hue, brightness, panel, stick1, stick2)

    while True:
        stick1_value, stick2_value = read_sticks()
        for i, panel_value in enumerate(list(df[panel].unique())):
            if i > max_panels:
                raise ValueError('Too many panels')
            frame_df = frame(panel_value, stick1_value, stick2_value)
            render(screen, i, frame_df)

        simulated_display.update(screen)
        led_display.update(screen)

def render(screen, i, frame_df):
    '''
    Render the data frame to the panel.
    '''

    x_0, y_0 = panel_x(i), PANEL_Y
    for point in zip(frame_df['x'] + x_0, frame_df['y'] + y_0):
        screen.set_at(point, (0, 0, 255))

def build_frame(df, x, y, hue, brightness, panel, stick1, stick2):
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

        # Not defaults
        for aesthetic in limits.keys():
            if aesthetics[aesthetic]:
                df_subset[aesthetic] = scale(df[aesthetics[aesthetic]],
                                             df[selector][aesthetics[aesthetic]],
                                             limits[aesthetic])
        return df_subset
    return frame

def read_sticks(): 
    '''
    Return only on change.
    '''
    import time
    time.sleep(1)
    return None, None

def scale(column, subcolumn, n):
    normalized = (subcolumn - column.min()) / (column.max() - column.min())
    return (normalized * (n - 1)).round()

if __name__ == '__main__':
    example()
