from bqplot import (OrdinalScale, LinearScale, Bars, Lines, Label, Figure, Axis, ColorScale, CATEGORY10, ColorScale)
import ipywidgets as widgets
import bqplot as bqp
import pandas as pd
import numpy as np

class Tab1:
    
    def __init__(self, df):
        
        self.df = df
        self.widgets = dict()   #dropdown and figs
        self.paras = dict()   #X and Y
        
        self._init_update()       

        
    
    def _init_update(self):
        
        self.widgets['dropdown'] = widgets.Dropdown(description='Frequency', options=['Year', 'Quarter', 'Month'])
        self.widgets['dropdown'].value = 'Year'
        self.widgets['dropdown'].observe(self._plot_update, 'value')
        
        self._data_process(self.df)
        
        self._plot_fig11(self.paras['plt_year_class_x'], self.paras['plt_year_y'])
        self._plot_fig12(self.paras['plt_year_class_x'], self.paras['plt_year_class_y'], 
                                                            self.paras['df_year_class'])
        
        self.widgets['tab1'] = widgets.VBox([self.widgets['dropdown'],
                                             self.widgets['fig11']
                                             ,self.widgets['fig12']
                                            ])
    
    
    
    def _data_process(self, df):
    
        self.paras['df_year_class'] = pd.pivot_table(df, values='Transaction Id', 
                                       index=['by_yr'], columns=['Class Number'],
                                      aggfunc='count', fill_value=0)
        self.paras['df_qrt_class'] = pd.pivot_table(df, values='Transaction Id', 
                                       index=['by_qrt'], columns=['Class Number'],
                                      aggfunc='count', fill_value=0)
        self.paras['df_mon_class'] = pd.pivot_table(df, values='Transaction Id', 
                                       index=['by_mon'], columns=['Class Number'],
                                      aggfunc='count', fill_value=0)
        
        
#         self.paras['plt_year_class_x'] = self.paras['df_year_class'].index.strftime('%Y')
        self.paras['plt_year_class_x'] = np.array(list(self.paras['df_year_class'].index))
        self.paras['plt_year_class_y'] = np.array(self.paras['df_year_class']).T
        self.paras['plt_year_y'] = np.array(self.paras['df_year_class']).sum(axis=1)

#         self.paras['plt_qrt_class_x'] = self.paras['df_qrt_class'].index.strftime('%YQ%q')
        self.paras['plt_qrt_class_x'] = np.array(list(self.paras['df_qrt_class'].index))
        self.paras['plt_qrt_class_y'] = np.array(self.paras['df_qrt_class']).T
        self.paras['plt_qrt_y'] = np.array(self.paras['df_qrt_class']).sum(axis=1)

#         self.paras['plt_mon_class_x'] = self.paras['df_mon_class'].index.strftime('%Y-%m')
        self.paras['plt_mon_class_x'] = np.array(list(self.paras['df_mon_class'].index))
        self.paras['plt_mon_class_y'] = np.array(self.paras['df_mon_class']).T
        self.paras['plt_mon_y'] = np.array(self.paras['df_mon_class']).sum(axis=1)
        

        
        
        
    def _plot_fig11(self, plt_x, plt_y):
        
        x_ord = OrdinalScale(domain=list(plt_x))
        y_sc = LinearScale(max=plt_y.max()*1.1)
        
        plot11 = Bars(x=plt_x, y=plt_y, scales={'x':x_ord, 'y':y_sc}, colors=['#3399ff'],
                      tooltip=bqp.Tooltip(fields=['x', 'y'], labels=['Date', 'Reads']))
        plot11.stroke = 'black'
        plot11.align = 'center'
        
        mark_text = Label(x=plt_x,
                      y=plt_y,
                      align='middle',
                      font_weight='normal',
                      y_offset=-10,
                      colors=['white'],
                      default_size=12,
                      scales={'x': x_ord, 'y': y_sc},
                      text=plt_y #[value for value in bar_label]
                         )
        
        xax11 = Axis(scale=x_ord, grid_lines='none', num_ticks=10)
        yax11 = Axis(scale=y_sc, tick_format=',d', grid_lines='none', orientation='vertical')
        
        #Axis(**kwargs)	orientation, side, label, tick_format, scale, num_ticks, 
        #tick_values, label_location, label_color, grid_lines, grid_color, color, label_offset, visible
        
        self.widgets['fig11'] = Figure(marks=[plot11, mark_text], axes=[xax11, yax11], padding_x=0.025, padding_y=0.025)
        self.widgets['fig11'].layout.width = '800px'
        self.widgets['fig11'].layout.height = '300px'
        self.widgets['fig11'].title = 'Readership data by Year'
        
        

    def _plot_fig12(self, plt_x, plt_y, df_year_class):
        
        x_ord = OrdinalScale()
        y_sc = LinearScale()
        
        #The 'marker' trait of a Lines instance must be any of 
        #['circle', 'cross', 'diamond', 'square', 'triangle-down', 'triangle-up', 'arrow', 'rectangle', 'ellipse'] or None
        plot12 = Lines(x=plt_x, y=plt_y, scales={'x':x_ord, 'y':y_sc}, 
                       tooltip=bqp.Tooltip(fields=['x', 'y'], labels=['Date', 'Reads']),
                      colors=CATEGORY10, marker='circle',
                      display_legend=True,
                      labels=['Class ' + s for s in df_year_class.columns])

        #Axes
        xax11 = Axis(scale=x_ord, grid_lines='none', num_ticks=10)
        yax11 = Axis(scale=y_sc, tick_format=',d', grid_lines='none', orientation='vertical')    
    
        #Axis(**kwargs)	orientation, side, label, tick_format, scale, num_ticks, 
        #tick_values, label_location, label_color, grid_lines, grid_color, color, label_offset, visible
        
        self.widgets['fig12'] = Figure(marks=[plot12], axes=[xax11, yax11], padding_x=0.025, padding_y=0.025)
        
        self.widgets['fig12'].layout.width = '800px'
        self.widgets['fig12'].layout.height = '300px'
    

    def _plot_update(self, *args): #only consider change frequency
        selected_freq = self.widgets['dropdown'].value

        # update the y attribute of the mark by selecting 
        # the column from the price data frame
        try:
            if selected_freq == 'Year':
                self.widgets['fig11'].axes[0].scale.domain = list(self.paras['plt_year_class_x'])
                self.widgets['fig11'].axes[1].scale.max=self.paras['plt_year_y'].max()*1.1
                self.widgets['fig11'].marks[1].x = self.paras['plt_year_class_x']
                self.widgets['fig11'].marks[1].y = self.paras['plt_year_y']
                self.widgets['fig11'].marks[1].text = self.paras['plt_year_y']
                self.widgets['fig11'].marks[0].x = self.paras['plt_year_class_x']
                self.widgets['fig11'].marks[0].y = self.paras['plt_year_y']
                self.widgets['fig12'].marks[0].x = self.paras['plt_year_class_x']
                if len(self.paras['plt_year_class_x'])>1:
                    self.widgets['fig12'].marks[0].y = self.paras['plt_year_class_y']
                else:
                    self.widgets['fig12'].marks[0].y = self.paras['plt_year_class_y'][0]
            elif selected_freq == 'Quarter':
                self.widgets['fig11'].axes[0].scale.domain = list(self.paras['plt_qrt_class_x'])
                self.widgets['fig11'].axes[1].scale.max=self.paras['plt_qrt_y'].max()*1.1
                self.widgets['fig11'].marks[1].x = self.paras['plt_qrt_class_x']
                self.widgets['fig11'].marks[1].y = self.paras['plt_qrt_y']
                self.widgets['fig11'].marks[1].text = self.paras['plt_qrt_y']
                self.widgets['fig11'].marks[0].x = self.paras['plt_qrt_class_x']
                self.widgets['fig11'].marks[0].y = self.paras['plt_qrt_y']
                self.widgets['fig12'].marks[0].x = self.paras['plt_qrt_class_x']
                self.widgets['fig12'].marks[0].y = self.paras['plt_qrt_class_y']
            elif selected_freq == 'Month':
                self.widgets['fig11'].axes[0].scale.domain = list(self.paras['plt_mon_class_x'])
                self.widgets['fig11'].axes[1].scale.max=self.paras['plt_mon_y'].max()*1.1
                self.widgets['fig11'].marks[1].x = self.paras['plt_mon_class_x']
                self.widgets['fig11'].marks[1].y = self.paras['plt_mon_y']
                self.widgets['fig11'].marks[1].text = self.paras['plt_mon_y']
                self.widgets['fig11'].marks[0].x = self.paras['plt_mon_class_x']
                self.widgets['fig11'].marks[0].y = self.paras['plt_mon_y']
                self.widgets['fig12'].marks[0].x = self.paras['plt_mon_class_x']
                self.widgets['fig12'].marks[0].y = self.paras['plt_mon_class_y']
        except:
            pass
        finally:
        # update the title of the figure
            if selected_freq == 'Year':
                self.widgets['fig12'].marks[0].labels = ['Class ' + s for s in self.paras['df_year_class'].columns]
            elif selected_freq == 'Quarter':
                self.widgets['fig12'].marks[0].labels = ['Class ' + s for s in self.paras['df_qrt_class'].columns]
            elif selected_freq == 'Month':
                self.widgets['fig12'].marks[0].labels = ['Class ' + s for s in self.paras['df_mon_class'].columns]
            self.widgets['fig11'].title = 'Readership data by {}'.format(selected_freq)
#             self.widgets['fig11'].marks[1].align = "middle"
        
        
    def _plot_fig1_update(self, df): #consider change year, class
             
        self._data_process(df)
        self._plot_update()
             
        
    def show(self):
        return self.widgets['tab1']
        
        