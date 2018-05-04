# -*- coding: utf-8 -*-


from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.models import Legend



def create_plot(data_list):
    p = figure(x_axis_type = 'datetime')
    props = dict(line_width=4, line_alpha=0.7)
    colors = Category10[10]
    names = 'abcdefghijklmnopqrs'
    callback_string = '{}.visible = {} in checkbox.active;'
    code_string = ''
    i = 0
    glyph_dict = {}
    labels = []
    active = []
    items = []
    
    for data in data_list:
        legend, series = data
        
        labels.append(legend)
        line = p.line(series.index, series.iloc[:,0], color=colors[i], **props)
        items.append((legend, [line]))
        name = names[i]
        line.name = name
        code_string += callback_string.format(name, str(i))
        glyph_dict.update({name:line})
        active.append(i)
        i+=1
    l = Legend(items=items,location=(0, 0))
    p.add_layout(l, 'right')
    checkbox = CheckboxGroup(labels=labels, active=active, width=200)
    glyph_dict.update({'checkbox':checkbox})
    checkbox.callback = CustomJS.from_coffeescript(args=glyph_dict, code=code_string)
    
    return checkbox, p

