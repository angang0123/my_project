from bqplot import (OrdinalScale, LinearScale, Bars, Figure, Axis, ColorScale, CATEGORY10, ColorScale)
import ipywidgets as widgets
from ipywidgets import TwoByTwoLayout
import bqplot as bqp
import pandas as pd
import numpy as np

class Tab5:
    
    def __init__(self, df, top):
        
        self.df = df
        self.top = top
        self.widgets = dict()
        self.paras = dict()
        
        self._init_update()
        
        
        
    def _init_update(self):
        
        self._data_process(self.df, self.top)
        
        self.widgets['fig51'] = self.plot_fig5('country', 
                                          self.paras['plt_country_x'], self.paras['plt_country_y'], '#ff00aa')
        
        self.widgets['fig52'] = self.plot_fig5('city', 
                                          self.paras['plt_city_x'], self.paras['plt_city_y'], '#00e6b8')
        
        self.widgets['fig53'] = self.plot_fig5('user', 
                                          self.paras['plt_user_x'], self.paras['plt_user_y'], '#ff9900')
        
        self.widgets['fig54'] = self.plot_fig5('company', 
                                          self.paras['plt_company_x'], self.paras['plt_company_y'], '#cce6ff')

        self.widgets['fig5note'] = widgets.Label(value="Note: 'Free content', deleted user, 'Embargoed' are not included in the chart")
        
        
        self.widgets['tab5'] = widgets.VBox(
                                            [TwoByTwoLayout(top_left=self.widgets['fig51'],
                                               top_right=self.widgets['fig52'],
                                               bottom_left=self.widgets['fig53'],
                                               bottom_right=self.widgets['fig54']),
                                             self.widgets['fig5note']]
                                            )
        
        
    def _data_process(self, df, top):
        
        try:
            self.paras['df_bar_country'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Country'],
                          aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            self.paras['df_bar_country'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Country'],
                          aggfunc='count', fill_value=0)
        finally:
            self.paras['df_bar_country'] = self.paras['df_bar_country'].sort_values(by=['Transaction Id'], ascending=False)
            if 'N/A - Free Content' in self.paras['df_bar_country'].index:
                self.paras['df_bar_country'] = self.paras['df_bar_country'].drop('N/A - Free Content')
            if '****** DELETE' in self.paras['df_bar_country'].index:
                self.paras['df_bar_country'] = self.paras['df_bar_country'].drop('****** DELETE')
            if 'Embargoed' in self.paras['df_bar_country'].index:
                self.paras['df_bar_country'] = self.paras['df_bar_country'].drop('Embargoed')
            
        try:
            self.paras['df_bar_city'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer City'],
                          aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            self.paras['df_bar_city'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer City'],
                          aggfunc='count', fill_value=0)
        finally:
            self.paras['df_bar_city'] = self.paras['df_bar_city'].sort_values(by=['Transaction Id'], ascending=False)
            if 'N/A - Free Content' in self.paras['df_bar_city'].index:
                self.paras['df_bar_city'] = self.paras['df_bar_city'].drop('N/A - Free Content')
            if '****** DELETE' in self.paras['df_bar_city'].index:
                self.paras['df_bar_city'] = self.paras['df_bar_city'].drop('****** DELETE')
            if 'Embargoed' in self.paras['df_bar_city'].index:
                self.paras['df_bar_city'] = self.paras['df_bar_city'].drop('Embargoed')
            
        try:
            self.paras['df_bar_user'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['User Name'],
                          aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            self.paras['df_bar_user'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['User Name'],
                          aggfunc='count', fill_value=0)
        finally:
            if len(self.paras['df_bar_user'])>0:
                self.paras['df_bar_user'] = self.paras['df_bar_user'].sort_values(by=['Transaction Id'], ascending=False)
                if 'N/A - Free Content' in self.paras['df_bar_user'].index:
                    self.paras['df_bar_user'] = self.paras['df_bar_user'].drop('N/A - Free Content')
                if '****** DELETE' in self.paras['df_bar_user'].index:
                    self.paras['df_bar_user'] = self.paras['df_bar_user'].drop('****** DELETE')
                if 'Embargoed' in self.paras['df_bar_user'].index:
                    self.paras['df_bar_user'] = self.paras['df_bar_user'].drop('Embargoed')    

        try:
            self.paras['df_bar_company'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Name'],
                          aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            self.paras['df_bar_company'] = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Name'],
                          aggfunc='count', fill_value=0)
        finally:
            self.paras['df_bar_company'] = self.paras['df_bar_company'].sort_values(by=['Transaction Id'], ascending=False)
            if 'N/A - Free Content' in self.paras['df_bar_company'].index:
                self.paras['df_bar_company'] = self.paras['df_bar_company'].drop('N/A - Free Content')
            if '****** DELETE' in self.paras['df_bar_company'].index:
                self.paras['df_bar_company'] = self.paras['df_bar_company'].drop('****** DELETE')
            if 'Embargoed' in self.paras['df_bar_company'].index:
                self.paras['df_bar_company'] = self.paras['df_bar_company'].drop('Embargoed')
        
        
        self.paras['plt_country_x'] = np.array(list(self.paras['df_bar_country'].index))[:top][::-1]
        self.paras['plt_country_y'] = np.array(self.paras['df_bar_country'])[:top][::-1].T

        self.paras['plt_city_x'] = np.array(list(self.paras['df_bar_city'].index))[:top][::-1]
        self.paras['plt_city_y'] = np.array(self.paras['df_bar_city'])[:top][::-1].T
        
        if len(self.paras['df_bar_user'])>0:
            self.paras['plt_user_x'] = np.array(list(self.paras['df_bar_user'].index))[:top][::-1]
            self.paras['plt_user_y'] = np.array(self.paras['df_bar_user'])[:top][::-1].T
        else:
            self.paras['plt_user_x'] = ['N/A']
            self.paras['plt_user_y'] = [0]
            
        self.paras['plt_company_x'] = np.array(list(self.paras['df_bar_company'].index))[:top][::-1]
        self.paras['plt_company_y'] = np.array(self.paras['df_bar_company'])[:top][::-1].T

        
        
    def plot_fig5(self, item, plt_x, plt_y, color_code):
        
#         fig_title_tmpl = 'Top 10 reads {}'.format(item) # string template for title of the figure 
        
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
        fig.layout.width = '400px'
        fig.layout.height = '220px'
        fig.fig_margin = {'bottom':40, 'left':100, 'right':20, 'top':40}

        return fig
    
    
    def _plot_update(self, *args):
        
        self.widgets['fig51'].marks[0].x = self.paras['plt_country_x']
        self.widgets['fig51'].marks[0].y = self.paras['plt_country_y']
        
        self.widgets['fig52'].marks[0].x = self.paras['plt_city_x']
        self.widgets['fig52'].marks[0].y = self.paras['plt_city_y']
        
        self.widgets['fig53'].marks[0].x = self.paras['plt_user_x']
        self.widgets['fig53'].marks[0].y = self.paras['plt_user_y']
        
        self.widgets['fig54'].marks[0].x = self.paras['plt_company_x']
        self.widgets['fig54'].marks[0].y = self.paras['plt_company_y']
        
        
    def _plot_fig5_update(self, df): 
        
        self._data_process(df, self.top)
        self._plot_update()
        
        
    def _top_update(self, top):
        
        self.top = top
        
        self.paras['plt_country_x'] = np.array(list(self.paras['df_bar_country'].index))[:top][::-1]
        self.paras['plt_country_y'] = np.array(self.paras['df_bar_country'])[:top][::-1].T

        self.paras['plt_city_x'] = np.array(list(self.paras['df_bar_city'].index))[:top][::-1]
        self.paras['plt_city_y'] = np.array(self.paras['df_bar_city'])[:top][::-1].T
        
        if len(self.paras['df_bar_user'])>0:
            self.paras['plt_user_x'] = np.array(list(self.paras['df_bar_user'].index))[:top][::-1]
            self.paras['plt_user_y'] = np.array(self.paras['df_bar_user'])[:top][::-1].T
        else:
            self.paras['plt_user_x'] = ['N/A']
            self.paras['plt_user_y'] = [0]
            
        self.paras['plt_company_x'] = np.array(list(self.paras['df_bar_company'].index))[:top][::-1]
        self.paras['plt_company_y'] = np.array(self.paras['df_bar_company'])[:top][::-1].T
        
        self._plot_update()
        
        
        self.widgets['fig51'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig51'].title = 'Top {} reads country'.format(top)
        self.widgets['fig52'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig52'].title = 'Top {} reads city'.format(top)
        self.widgets['fig53'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig53'].title = 'Top {} reads user'.format(top)
        self.widgets['fig54'].layout.height = str(220*int(top/10))+'px'
        self.widgets['fig54'].title = 'Top {} reads company'.format(top)
        
        
        
    def show(self):
        return self.widgets['tab5']