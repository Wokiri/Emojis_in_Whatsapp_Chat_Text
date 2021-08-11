from pathlib import Path

import collections

from string import printable

from random import sample

import pandas as pd

from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.palettes import inferno, Turbo256
from bokeh.io import output_file, show

from math import pi

chats = Path(r'./WhatsApp_Chat.txt')

alpha_nums = printable + '''
”“’•  —‘
♂


♀

ā
☁

¯
ツ
¯

'ê'

'''


data_json = {}
emojis_used = []


with open(chats, mode='r') as file_reader:
    data = file_reader.read()
    for item in data:
        if item not in alpha_nums:
            emojis_used.append(item)


data_json = dict(collections.Counter(emojis_used))
data_json = dict(sorted(data_json.items(), reverse=True, key=lambda item: item[1]))
# columns = list(data_json.keys())



emojis_used_DF = pd.Series(data_json).reset_index(name='occurences').rename(columns={'index':'emoji'})
emojis_used_DF['angle'] = emojis_used_DF['occurences']/emojis_used_DF['occurences'].sum() * 2*pi
# emojis_used_DF['color'] = inferno(len(data_json))

emojis_used_DF['color'] = sample(Turbo256, k=len(emojis_used_DF))

emojis_used_DF = emojis_used_DF.sort_values(
    by=['occurences'],
    ascending = False
)

# print(data_json)
# print(emojis_used_DF)



output_file(filename = "emojis_used_pie.html", title='Piechart | Number of Emojis')

emojis_used_CDS = ColumnDataSource(emojis_used_DF)

emojis_used_fig = figure(
    title="Piechart showing Emojis Used",
    plot_height=800,
    plot_width=1000,
    tooltips=[
        ('Emoji', '@emoji'),
        ('Occurrences', '@occurences'),
    ],
)


emojis_used_fig.wedge(
    x=0,
    y=1,
    radius=0.75,
    start_angle=cumsum('angle', include_zero=True),
    end_angle=cumsum('angle'),
    line_color="#ffffff",
    fill_color='color',
    source=emojis_used_CDS,
    legend_field='emoji',
)

emojis_used_fig.toolbar.active_drag = None
emojis_used_fig.title.align = "center"
emojis_used_fig.title.text_color = "darkgreen"
emojis_used_fig.title.text_font_size = "18px"


show(emojis_used_fig)