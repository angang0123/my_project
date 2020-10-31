from bqplot import (OrdinalScale, LinearScale, Bars, Figure, Axis, ColorScale, CATEGORY10, ColorScale)
import ipywidgets as widgets
from ipydatagrid import DataGrid, TextRenderer
from ipywidgets import AppLayout
import bqplot as bqp
import pandas as pd
import numpy as np

class Tab3:
    
    def __init__(self, df, top):
        
        self.df = df
        self.top = top
        self.max_dg = 5000
        self.widgets = dict()
        self.paras = dict()
        
        self._init_update()
        
     
    def _init_update(self):
        
        self._data_process(self.df, self.top)
        
        self.widgets['fig3'] = self.plot_fig3('headline', 
                                          self.paras['plt_title_x'], self.paras['plt_title_y'], '#ffcc00')
        self.plot3_addon()
#         self.widgets['fig3_label'] = widgets.Label(value='  *Click bar(s) to filter values. Click button to reset.')
        
        
        self.widgets['tab3'] = widgets.VBox([
                                            self.widgets['fig3'],
                                            widgets.Label("Maximum of {} recrods are listed below.".format(self.max_dg)),
                                            self.widgets['datagrid']
                                            ])
    
        
    def _data_process(self, df, top):
        
        try:
            self.paras['df_title'] = pd.pivot_table(df, values='Transaction Id',
                                      index=['Title'],
                                      aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            self.paras['df_title'] = pd.pivot_table(df, values='Transaction Id',
                                      index=['Title'],
                                      aggfunc='count', fill_value=0)
        finally:    
            self.paras['df_title'] = self.paras['df_title'].sort_values(by=['Transaction Id'], ascending=False)
               

        self.paras['plt_title_x'] = np.array(list(self.paras['df_title'].index))[:top][::-1]
        self.paras['plt_title_y'] = np.array(self.paras['df_title']['Transaction Id'].T)[:top][::-1]
        
        
    def plot_fig3(self, item, plt_x, plt_y, color_code):
        
        fig_title_tmpl = 'Top 10 reads {}'.format(item) # string template for title of the figure 
        
        x_ord = OrdinalScale()
        y_sc = LinearScale()
        

        plot = Bars(x=plt_x, y=plt_y, scales={'x':x_ord, 'y':y_sc}, colors=[color_code],
                    orientation='horizontal', padding=0.3,
                    interactions={'click': 'select',
                                 'hover':'tooltip'},
                    unselected_style={'opacity': .5},
                     tooltip=bqp.Tooltip(fields=['x', 'y'], labels=[item, 'Reads']))
        
        plot.selected = list(range(len(plt_x)))
        plot.align = 'center'
        
        xax = Axis(scale=x_ord, grid_lines='none', orientation='vertical')
        yax = Axis(scale=y_sc, tick_format=',d', grid_lines='none', min=0)
        
        plot.observe(self.on_bar_click, names='selected')

        fig = Figure(marks=[plot], axes=[xax, yax], padding_x=0.025, padding_y=0.025)
        fig.title = 'Top 10 reads {}'.format(item)
        fig.layout.width, fig.layout.height = '860px', '220px'
        fig.fig_margin = {'bottom':0, 'left':500, 'right':20, 'top':40}
        

        return fig
    
    
    def on_bar_click(self, evt=None):
        if evt is not None and evt['new'] is not None:
            selected = [self.widgets['fig3'].marks[0].x[i] for i in evt['new']]
            filter_df = self.df[['Title', 'UUID', 'User Name', 'Customer Name', 'Transaction Date']][self.df['Title'].isin(selected)]
            self.widgets['datagrid'].data = filter_df[:self.max_dg]
        else:
            self.widgets['datagrid'].data = self.df[['Title', 'UUID', 'User Name', 'Customer Name', 'Transaction Date']][:self.max_dg]
    
    
    
    def plot3_addon(self):
        
        self.widgets['datagrid'] = DataGrid(self.df[['Title', 'UUID', 'User Name', 'Customer Name', 'Transaction Date']][:self.max_dg], 
                                                base_column_size=50, layout={'height':'300px'},
                                     column_widths={'Title':280, 'UUID':60, 'User Name':80, 'Customer Name':180, 'Transaction Date':90},
                                     renderers={'Transaction Date': TextRenderer(format='%Y/%m/%d', format_type='time')})
        

          
    
    def _plot_update(self, df):
        
        self.widgets['fig3'].marks[0].x = self.paras['plt_title_x']
        self.widgets['fig3'].marks[0].y = self.paras['plt_title_y']
        self.widgets['fig3'].marks[0].selected = list(range(len(self.paras['plt_title_x'])))
        
        self.widgets['datagrid'].data = df[['Title', 'UUID', 'User Name', 'Customer Name', 'Transaction Date']][:self.max_dg]
        
        
    def _plot_fig3_update(self, df): 
        
        self._data_process(df, self.top)
        self._plot_update(df)
        
    
    
    def _top_update(self, top):
        
        self.top = top

        self.paras['plt_title_x'] = np.array(list(self.paras['df_title'].index))[:top][::-1]
        self.paras['plt_title_y'] = np.array(self.paras['df_title']['Transaction Id'].T)[:top][::-1]
        
        self.widgets['fig3'].marks[0].x = self.paras['plt_title_x']
        self.widgets['fig3'].marks[0].y = self.paras['plt_title_y']
        self.widgets['fig3'].marks[0].selected = list(range(len(self.paras['plt_title_x'])))
        
        self.widgets['fig3'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig3'].title = 'Top {} reads headline'.format(top)
        
        
    
    def show(self):
        return self.widgets['tab3']
    