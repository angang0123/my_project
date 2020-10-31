from bqplot import CATEGORY10, ColorScale
from bqplot import Mercator, Tooltip

import ipywidgets as widgets
import bqplot as bqp
from ipydatagrid import DataGrid, TextRenderer
import bqplot.pyplot as plt
import pandas as pd

class Tab6:
    
    def __init__(self, df):
        
        self.df = df
        self.widgets = dict()   #dropdown and figs
        self.paras = dict()   #X and Y
        
        self._init_update()
        
        
    def _init_update(self):
        
        self.paras['country_map'] = pd.read_csv("IdMapping.csv", header=0, usecols=['Country Name', 'id'])
        self.paras['country_id'] = dict(zip(self.paras['country_map']['id'], self.paras['country_map']['Country Name']))
        self.paras['country_map'].set_index(['Country Name'], inplace=True)
#         self.paras['country_id'] = pd.read_csv("IdMapping.csv", header=0, usecols=['Country Name', 'id'])
#         self.paras['country_id'].set_index(['id'], inplace=True)
        
        self.paras['country_index'] = self.paras['country_map'].index
        
        self._data_process(self.df)
        
        self._plot_fig6(self.paras['plt_map'])
  
        self.widgets['mapdatagrid'] = DataGrid(self.paras['df_mapgrid'], 
                                                base_column_size=50, layout={'height':'300px'},
                                     column_widths={'Customer Country':180, 'Customer Name':300, 'Total Reads':100}
#                                      ,renderers={'Transaction Date': TextRenderer(format='%Y/%m/%d', format_type='time')}
                                              )
                
        self.widgets['tab6'] = widgets.VBox([
                                            self.widgets['fig6'],
                                            self.widgets['mapdatagrid']
                                            ])
        
     
    def _data_process(self, df):
        
        try:
            df_map_country = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Country'],
                          aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            df_map_country = pd.pivot_table(df, values='Transaction Id', 
                           index=['Customer Country'],
                          aggfunc='count', fill_value=0)
                          
        self.paras['plt_map'] = {}
        self.paras['unplt_map'] = {}
        
        
        temp_dict = df_map_country.to_dict()['Transaction Id']
        
        for key in temp_dict:
            if (key in self.paras['country_index']) and not pd.isna(self.paras['country_map'].loc[key]['id']):
                self.paras['plt_map'][int(self.paras['country_map'].loc[key]['id'])] = temp_dict[key]
            else:
                self.paras['unplt_map'][key] = temp_dict[key]
                
                
        try:
            df_mapgrid = pd.pivot_table(df, values='Transaction Id',
                                      index=['Customer Country', 'Customer Name'],
                                      aggfunc='count', fill_value=0).to_frame()
        except AttributeError:
            df_mapgrid = pd.pivot_table(df, values='Transaction Id',
                                      index=['Customer Country', 'Customer Name'],
                                      aggfunc='count', fill_value=0)
        finally:    
            df_mapgrid = df_mapgrid.sort_values(by=['Transaction Id'], ascending=False)
            if '****** DELETE' in df_mapgrid.index:
                df_mapgrid = df_mapgrid.drop('****** DELETE')
            if 'Embargoed' in df_mapgrid.index:
                df_mapgrid = df_mapgrid.drop('Embargoed')
            df_mapgrid = df_mapgrid.reset_index()
            df_mapgrid.columns = ['Customer Country', 'Customer Name', 'Total Reads']
            
        self.paras['df_mapgrid'] = df_mapgrid
        
        
        
    def _plot_fig6(self, data_map):
    
        self.widgets['fig6']  = plt.figure(title='Choropleth Map of Readership')
        try:
            plt.scales(scales={'projection':Mercator()
                               , 'color': ColorScale(scheme='GnBu', min=0, max=max(data_map.values()))
                              })
            def_tt = Tooltip(fields=['name'])
            self.widgets['plt_map'] = plt.geo(map_data='WorldMap',
                              color=data_map,
                              tooltip=def_tt,
                              interactions={'click':'select', 'hover':'tooltip'},
                              colors={'default_color': 'White'},
                              axes_options={'color':{'orientation':'vertical', 'side':'right'}}
                                )
        except:
            plt.scales(scales={'projection':Mercator()})
            def_tt = Tooltip(fields=['name'])
            self.widgets['plt_map'] = plt.geo(map_data='WorldMap',
                              tooltip=def_tt,
                              interactions={'click':'select', 'hover':'tooltip'},
                              colors={'default_color': 'White'},
                              axes_options={'color':{'orientation':'vertical', 'side':'right'}}
                                )
        finally:
            self.widgets['plt_map'].observe(self._map_click, names='selected')
        

        self.widgets['fig6'].layout.width = '800px'
        self.widgets['fig6'].layout.height = '440px'
        self.widgets['fig6'].fig_margin = {'bottom':40, 'left':40, 'right':100, 'top':40}
        
#         self.widgets['fig5']
    
    def _map_click(self, change):
        if change is not None and change['new'] is not None and len(change['new']!=0):
            selected = [self.paras['country_id'][i] for i in change['new']]
            self.widgets['mapdatagrid'].data = self.paras['df_mapgrid'][self.paras['df_mapgrid']['Customer Country'].isin(selected)]
        else:
            self.widgets['mapdatagrid'].data = self.paras['df_mapgrid']
    
    
    def _plot_update(self, *args):
        
#         self.widgets['plt_map'].selected = []
        self.widgets['plt_map'].color = self.paras['plt_map']
        self.widgets['plt_map'].scales['color'].max = max(self.paras['plt_map'].values())
        self.widgets['mapdatagrid'].data = self.paras['df_mapgrid']
        

    def _plot_fig6_update(self, df): 
        
        self.df = df
        self._data_process(df)
        self._plot_update()   
        
        
    def show(self):
        return self.widgets['tab6']