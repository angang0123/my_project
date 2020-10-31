from bqplot import (OrdinalScale, LinearScale, Bars, Figure, Axis, ColorScale, CATEGORY10, ColorScale)
import ipywidgets as widgets
import bqwidgets as bqw
from ipywidgets import AppLayout
import bqplot as bqp
import pandas as pd
import numpy as np

class Tab4:
    
    def __init__(self, df, top):
        
        self.df = df
        self.top = top
        self.widgets = dict()
        self.paras = dict()
        
        self._init_update()
        
     
    def _init_update(self):
        
        self._data_process(self.df, self.top)
        
        self.widgets['fig41'] = self.plot_fig4('analyst', 
                                          self.paras['plt_analyst_x'], self.paras['plt_analyst_y'], '#e60000')
                 
        self.widgets['fig42'] = self.plot_fig4('ticker', 
                                          self.paras['plt_ticker_x'], self.paras['plt_ticker_y'], '#00cc00')
        
        
        
        self.widgets['tab4'] = AppLayout(header=None,
                                          left_sidebar=self.widgets['fig41'],
                                          center=None,
                                          right_sidebar=self.widgets['fig42'],
                                          footer=None
                                              )
        
    def _data_process(self, df, top):
        
        self.paras['dic_analyst'] = {}
        if 'Author(s)' in df.columns:
            for s in df['Author(s)']:
                if type(s) == type('test'):
                    line = s.split(sep=', ')
                    for t in line:
                        if t in self.paras['dic_analyst']:
                            self.paras['dic_analyst'][t] += 1
                        else:
                            self.paras['dic_analyst'][t] = 1
            self.paras['df_analyst'] = pd.DataFrame(
                                list(self.paras['dic_analyst'].values()),index=list(self.paras['dic_analyst'].keys()),columns=['count'])
            self.paras['df_analyst'] = self.paras['df_analyst'].sort_values(by='count', ascending=False)
        else:
            self.paras['df_analyst'] = pd.DataFrame()
        
        self.paras['dic_ticker'] = {}
        if 'Primary Supplied Ticker(s)' in df.columns:
            for s in df['Primary Supplied Ticker(s)']:
                if type(s) == type('test'):
                    line = s.split(sep=', ')
                    for t in line:
                        if ('@' in t):
                            if t in self.paras['dic_ticker']:
                                self.paras['dic_ticker'][t] += 1
                            else:
                                self.paras['dic_ticker'][t] = 1
            self.paras['df_ticker'] = pd.DataFrame(
                                list(self.paras['dic_ticker'].values()),index=list(self.paras['dic_ticker'].keys()),columns=['count'])
            self.paras['df_ticker'] = self.paras['df_ticker'].sort_values(by='count', ascending=False)
        else:
            self.paras['df_ticker'] = pd.DataFrame()
        
        
        if len(self.paras['df_analyst'])>0:
            self.paras['plt_analyst_x'] = np.array(list(self.paras['df_analyst'].index))[:top][::-1]
            self.paras['plt_analyst_y'] = np.array(self.paras['df_analyst']['count'])[:top][::-1]
        else:
            self.paras['plt_analyst_x'] = ['N/A']
            self.paras['plt_analyst_y'] = [0]
        
        if len(self.paras['df_ticker'])>0:
            self.paras['plt_ticker_x'] = np.array(list(self.paras['df_ticker'].index))[:top][::-1]
            self.paras['plt_ticker_y'] = np.array(self.paras['df_ticker']['count'])[:top][::-1]
        else:
            self.paras['plt_ticker_x'] = ['N/A']
            self.paras['plt_ticker_y'] = [0]

               
        self.paras['tickers'] = self.paras['dic_ticker'].keys()
        

        
    def plot_fig4(self, item, plt_x, plt_y, color_code):
        #will set title fig differently
        #fig will be distincted by color_code
        
        fig_title_tmpl = 'Top 10 reads {}'.format(item) # string template for title of the figure 
        
        x_ord = OrdinalScale()
        y_sc = LinearScale()

        plot = Bars(x=plt_x, y=plt_y, scales={'x':x_ord, 'y':y_sc}, colors=[color_code],
                    orientation='horizontal', padding=0.3,
                     tooltip=bqp.Tooltip(fields=['x', 'y'], labels=[item, 'Reads']))
                    
        plot.align = 'center'
        
        xax = Axis(scale=x_ord, grid_lines='none', orientation='vertical')
        yax = Axis(scale=y_sc, tick_format=',d', grid_lines='none', min=0)

        fig = Figure(marks=[plot], axes=[xax, yax], padding_x=0.025, padding_y=0.025)
        fig.title = 'Top 10 reads {}'.format(item)
        
        fig.layout.width, fig.layout.height = '400px', '220px'
        fig.fig_margin = {'bottom':40, 'left':100, 'right':20, 'top':40}
               

        return fig
    
    
    def _plot_update(self, *args):
        
        self.widgets['fig41'].marks[0].x = self.paras['plt_analyst_x']
        self.widgets['fig41'].marks[0].y = self.paras['plt_analyst_y']
        
        self.widgets['fig42'].marks[0].x = self.paras['plt_ticker_x']
        self.widgets['fig42'].marks[0].y = self.paras['plt_ticker_y']
        
        
        
    def _plot_fig4_update(self, df): 
        
        self._data_process(df, self.top)
        self._plot_update()
        
        
    def _top_update(self, top):
        
        self.top = top
        
        if len(self.paras['df_analyst'])>0:
            self.paras['plt_analyst_x'] = np.array(list(self.paras['df_analyst'].index))[:top][::-1]
            self.paras['plt_analyst_y'] = np.array(self.paras['df_analyst']['count'])[:top][::-1]
        else:
            self.paras['plt_analyst_x'] = ['N/A']
            self.paras['plt_analyst_y'] = [0]
        
        if len(self.paras['df_ticker'])>0:
            self.paras['plt_ticker_x'] = np.array(list(self.paras['df_ticker'].index))[:top][::-1]
            self.paras['plt_ticker_y'] = np.array(self.paras['df_ticker']['count'])[:top][::-1]
        else:
            self.paras['plt_ticker_x'] = ['N/A']
            self.paras['plt_ticker_y'] = [0]
            
        self._plot_update()
        
        self.widgets['fig41'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig41'].title = 'Top {} reads analyst'.format(top)
        self.widgets['fig42'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig42'].title = 'Top {} reads ticker'.format(top)
            
        
    
    def show(self):
        return self.widgets['tab4']
    