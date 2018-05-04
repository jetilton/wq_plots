# -*- coding: utf-8 -*-

import yaml
from cwms_read.cwms_read import get_cwms
from datetime import datetime, timedelta
from checkbox import create_plot
from bokeh.layouts import layout
from bokeh.models import CheckboxGroup
from bokeh.io import curdoc



lookback = 7
now = datetime.now()
start = now - timedelta(days = lookback)
start_date  = (start.year, start.month, start.day)
end_date = (now.year, now.month, now.day)




snake = yaml.safe_load(open('snake.yml'))

for key,value in snake.items():
    for k,v in value.items():
        for label, path in v.items():
            snake[key][k][label] = get_cwms(path, start_date = start_date, end_date = end_date, fill = False)
            
for key,value in snake.items():
    for k,v in value.items():
        snake[key][k] = [(label, df) for label, df in v.items()]
        
for key,value in snake.items():
    for k,v in value.items():
        snake[key][k] = (create_plot(snake[key][k]))
        

order = ['tdg', 'flow', 'air pressure', 'temp', 'wind', 'air temp']

children = []
link = []
for key, value in snake.items():
    for k in order:
        checkbox, p = value[k]
        if k==order[0]:
            link.append(p)
        else:
            p.x_range = link[0].x_range
        if k != order[-1]:
            p.xaxis.visible = False 
        if k == 'air pressure': children.append([CheckboxGroup(width=200),p])
        else: children.append([checkbox, p])
        
    snake[key] =  layout(children)