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


emojis_used_DF['color'] = sample(Turbo256, k=len(emojis_used_DF))

emojis_used_DF = emojis_used_DF.sort_values(
    by=['occurences'],
    ascending = False
)



output_file(filename = "emojis_used_vbar.html", title='Vertical Bar | Number of Emojis')

emojis_used_CDS = ColumnDataSource(emojis_used_DF)

emojis_used_fig = figure(
    title="V.Bar showing Emojis Used since 2/13/21 22:15 to 8/10/21 00:51",
    x_axis_label='Emoji',
    y_axis_label='Number of Occurences',
    x_range=list(emojis_used_DF['emoji']),
    plot_height=800,
    plot_width=2400,
    tooltips=[
        ('Emoji', '@emoji'),
        ('Occurrences', '@occurences'),
    ],
)


emojis_used_fig.vbar(
    x='emoji',
    top='occurences',
    width=0.850,
    fill_color='color',
    line_color ='midnightblue',
    source=emojis_used_CDS,
    legend_field='emoji',
)

emojis_used_fig.toolbar.active_drag = None
emojis_used_fig.title.align = "center"
emojis_used_fig.title.text_color = "darkgreen"
emojis_used_fig.title.text_font_size = "18px"
emojis_used_fig.xaxis.major_label_text_color = 'darkgreen'
emojis_used_fig.yaxis.major_label_text_color = 'darkgreen'
emojis_used_fig.xgrid.grid_line_color = None
emojis_used_fig.y_range.start=1

show(emojis_used_fig)