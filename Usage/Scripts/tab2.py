from bqplot import (OrdinalScale, LinearScale, Bars, Figure, Axis, ColorScale, CATEGORY10)
from bqplot.interacts import BrushIntervalSelector
import ipywidgets as widgets
import bqplot as bqp
import pandas as pd
import numpy as np

class Tab2:
    
    def __init__(self, df):
        
        self.df = df
        self.widgets = dict()   #dropdown and figs
        self.paras = dict()   #X and Y
        
        self._init_update()
        
        
    def _init_update(self):
        
        self.paras['df_day'] = pd.pivot_table(self.df, values='Transaction Id', 
                                               index=['by_day'],
                                              aggfunc='count', fill_value=0)
        
        new_index = pd.date_range(start=self.df['by_day'].iloc[0].to_timestamp()
                                  ,end=self.df['by_day'].iloc[-1].to_timestamp()
                                  ,freq='D')
        new_index = new_index.to_period('D')
        self.paras['df_day'] = self.paras['df_day'].reindex(new_index)
        self.paras['df_day'].index =  self.paras['df_day'].index.astype(str)
        
        
        self.paras['start'] = self.paras['df_day'].index[0]
        self.paras['end'] = self.paras['df_day'].index[-1]
        self.paras['total'] = self.paras['df_day'].sum(axis=0, skipna=True)
        
        
#         self.paras['plt_day_x'] = self.paras['df_day'].index.strftime('%Y-%m-%d')
        self.paras['plt_day_x'] = np.array(list(self.paras['df_day'].index))
        self.paras['plt_day_y'] = np.array(self.paras['df_day']).T
        
        self._plot_fig2(self.paras['plt_day_x'], self.paras['plt_day_y'])
        
        label_str = "Under current filter, from {} to {}, there are total {} hits.".format(self.paras['start'],
                                                                                          self.paras['end'],
                                                                                          int(self.paras['total']))
        self.widgets['tab2_des'] = widgets.Label(value=label_str)
        
        
        
        self.widgets['tab2'] = widgets.VBox([
                                            self.widgets['fig2'],
                                            self.widgets['tab2_des']
                                            ])
        
               
        
    def _plot_fig2(self, plt_x, plt_y):
        
#         x_ord = OrdinalScale()
#         dt_x_brush = DateScale()
        x_brush = OrdinalScale()
        y_sc = LinearScale()
        
        plot = Bars(x=plt_x, y=plt_y, scales={'x':x_brush, 'y':y_sc}, colors=['#ff5500'],
                     tooltip=bqp.Tooltip(fields=['x', 'y'], labels=['Date', 'Reads']))
#         plot2.stroke = 'black'
        plot.align = 'center'
        
        xax = Axis(scale=x_brush, grid_lines='none', num_ticks=10)
        yax = Axis(scale=y_sc, tick_format=',d', grid_lines='none', orientation='vertical', min=0)
        
        brushsel_date = BrushIntervalSelector(scale=x_brush, marks=[plot], color='skyblue')
        
        plot.observe(self._x_brush_change_callback, names=['selected'])
        
        #Axis(**kwargs)	orientation, side, label, tick_format, scale, num_ticks, 
        #tick_values, label_location, label_color, grid_lines, grid_color, color, label_offset, visible
        
        self.widgets['fig2'] = Figure(marks=[plot], axes=[xax, yax], 
                                      padding_x=0.025, padding_y=0.025,
                                     interaction=brushsel_date)
        self.widgets['fig2'].layout.width = '800px'
        self.widgets['fig2'].layout.height = '300px'
        self.widgets['fig2'].title = 'Readership data by Day'
        
        
        
       
        
    
    def _x_brush_change_callback(self, change):
        if change.new is not None:
            self.paras['x_brush'] = change.new
            self.paras['start'] = self.paras['df_day'].index[change.new[0]]
            self.paras['end'] = self.paras['df_day'].index[change.new[-1]]
            self.paras['total'] = self.paras['df_day'].loc[self.paras['start']:self.paras['end']].sum(axis=0)
        else:
#             self.paras['x_brush'] = self.paras['df_day'].index
            self.paras['start'] = self.paras['df_day'].index[0]
            self.paras['end'] = self.paras['df_day'].index[-1]
            self.paras['total'] = self.paras['df_day'].sum(axis=0, skipna=True)
            
        label_str = "Under current filter, from {} to {}, there are total {} hits.".format(self.paras['start'],
                                                                                          self.paras['end'],
                                                                                          int(self.paras['total']))
        self.widgets['tab2_des'].value = label_str
        
        
        
    def _plot_fig2_update(self, df):
        
        self.paras['df_day'] = pd.pivot_table(df, values='Transaction Id', 
                                               index=['by_day'],
                                              aggfunc='count', fill_value=0)           
        new_index = pd.date_range(start=df['by_day'].iloc[0].to_timestamp()
                                  ,end=df['by_day'].iloc[-1].to_timestamp()
                                  ,freq='D')
        new_index = new_index.to_period('D')
        self.paras['df_day'] = self.paras['df_day'].reindex(new_index)
        self.paras['df_day'].index =  self.paras['df_day'].index.astype(str)
        
        self.paras['plt_day_x'] = np.array(list(self.paras['df_day'].index))
        self.paras['plt_day_y'] = np.array(self.paras['df_day']).T
        
        self.widgets['fig2'].marks[0].x = self.paras['plt_day_x']
        self.widgets['fig2'].marks[0].y = self.paras['plt_day_y']
        
        self.paras['start'] = self.paras['df_day'].index[0]
        self.paras['end'] = self.paras['df_day'].index[-1]
        self.paras['total'] = self.paras['df_day'].sum(axis=0, skipna=True)
        
        self.widgets['tab2_des'].value = "Under current filter, from {} to {}, there are total {} hits.".format(self.paras['start'],
                                                                                          self.paras['end'],
                                                                                          int(self.paras['total']))
        
    def show(self):
        return self.widgets['tab2']

