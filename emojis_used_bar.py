from pathlib import Path

import collections

from string import printable

from random import sample

import pandas as pd

import re, datetime

from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.palettes import BrBG10

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

date_pattern = re.compile(r'^\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}')


data_json = {}
emojis_used = []
start_date = None
end_date = None


with open(chats, mode='r') as file_reader:
    data = file_reader.read()
    for item in data:
        if item not in alpha_nums:
            emojis_used.append(item)

with open(chats, mode='r') as file_reader:
    all_lines = file_reader.readlines()
    start_date = date_pattern.findall(all_lines[0])[0].replace(',', '')
    end_date = date_pattern.findall(all_lines[len(all_lines)-1])[0].replace(',', '')

    start_date = datetime.datetime.strptime(start_date, '%m/%d/%y %H:%M')
    end_date = datetime.datetime.strptime(end_date, '%m/%d/%y %H:%M')



data_json = dict(collections.Counter(emojis_used))
data_json = dict(sorted(data_json.items(), reverse=True, key=lambda item: item[1]))
# columns = list(data_json.keys())


data = {}
index = 0
for i,j in data_json.items():
    if index < 10:
        data.update({i:j})
    index+=1

        
data_json = data

emojis_used_DF = pd.Series(data_json).reset_index(name='occurences').rename(columns={'index':'emoji'})

emojis_used_DF['color'] = BrBG10

emojis_used_DF = emojis_used_DF.sort_values(
    by=['occurences'],
    ascending = False
)



output_file(filename = "emojis_used_vbar.html", title='Vertical Bar | Number of Emojis')

emojis_used_CDS = ColumnDataSource(emojis_used_DF)

emojis_used_fig = figure(
    title=f"Top 10 Emojis Used since {start_date} to {end_date}",
    x_axis_label='Emoji',
    y_axis_label='Number of Occurences',
    x_range=list(emojis_used_DF['emoji']),
    plot_height=600,
    plot_width=800,
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

