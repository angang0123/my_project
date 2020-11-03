import ipywidgets as widgets
import pandas as pd
import numpy as np
import datetime as dt

from bqplot import (OrdinalScale, LinearScale, Bars, Figure, Axis, CATEGORY10, Tooltip)
from bqplot import ColorScale, ColorAxis


class bySLA:
    
    def __init__(self, df_in, df_pb):
        
        self.df_in = df_in
        self.df_pb = df_pb
        
        self.widgets = dict()
        self.paras = dict()
        
        self._data_process(df_in, df_pb)
        self._plot()
        self._plot_other()
        
        self.widgets['bySLA'] = widgets.VBox([
                                        widgets.HBox([
                                            widgets.VBox([
                                                widgets.Label(value='SLA Benchmark (day)', width='80px', height='300px'),
                                                self.widgets['slider'],
                                                widgets.Label(value="Status Filter"),
                                                self.widgets['filter']
                                                ]), 
                                            self.widgets['bar_fig']    
                                            ]),
                                        self.widgets['label']
                                        ])
        
    
    def _data_process(self, df_in, df_pb, sla_day=5):
        
        df_in['SLA'] = np.where(
                                        (df_in['Closed']-df_in['Created']) <= dt.timedelta(sla_day-1), 
                                        "In SLA", "Out of SLA"
                                    )
        df_pb['SLA'] = np.where(
                                        (dt.datetime.today()-df_pb['Created']) <= dt.timedelta(sla_day-1),
                                        "Still Pending in SLA", "Out of SLA"
                                    )
        
        self.paras['SLA'] = pd.concat([
                                df_in[['Request ID', 'by_mon', 'SLA']], 
                                df_pb[['Request ID', 'by_mon', 'SLA']]
                                ], axis=0)
        
        self.paras['df_SLA'] = pd.pivot_table(self.paras['SLA'], values='Request ID',
                                            columns=['SLA'], index=['by_mon'],
                                             aggfunc='count', fill_value=0)
        
        
        self.paras['all_status'] = list(self.paras['df_SLA'].columns)
        self.paras['sum_by_sla'] = self.paras['df_SLA'].sum(axis=1)
        self.paras['df_by_sla'] = (self.paras['df_SLA'].div(self.paras['sum_by_sla'], axis=0)).round(4)
        
        self.paras['colorscheme'] = {'In SLA':"#33cc33", 'Still Pending in SLA':"#00e6e6", 'Out of SLA':"#8c8c8c"}
        self.paras['bar_colors'] = [self.paras['colorscheme'][i] for i in self.paras['all_status']]
        
        self.paras['out_of_sla'] = self.paras['df_SLA']['Out of SLA'].sum()
        self.paras['total_sla'] = self.paras['df_SLA'].sum().sum()
        self.paras['out_sla_rate'] = round(self.paras['out_of_sla']/self.paras['total_sla']*100, 2)
                  
    def _plot(self):
        
        x_ord = OrdinalScale()
        y_sc = LinearScale(max=1.2, min=-.1)

        self.widgets['bar'] = Bars(x=np.array(self.paras['df_by_sla'].index), 
                   y=[self.paras['df_by_sla'][i] for i in self.paras['all_status']],
                   scales={'x': x_ord, 'y': y_sc,}, 
                   padding=0.3, 
                   colors=self.paras['bar_colors'],
                   display_legend=True, 
                   labels=self.paras['all_status'],
                  tooltip=Tooltip(fields=['x', 'y'], labels=['Month', 'SLA Percentage'])
                  )

        ax_x = Axis(scale=x_ord, tick_rotate=-90, 
        #             label_offset='300ex',
        #             label_location='start',
                    grid_lines='none',
                   offset={'value':-0.8})
        ax_y = Axis(scale=y_sc, orientation='vertical', tick_format='0.0%', grid_lines='dashed')

        self.widgets['bar_fig'] = Figure(marks=[self.widgets['bar']], axes=[ax_x, ax_y], legend_location='top-right')
        self.widgets['bar_fig'].title = "Entitlements Requests by 5-day SLA"
        self.widgets['bar_fig'].layout.width = '800px'
        self.widgets['bar_fig'].layout.height = '500px'
    
    
    
    def _plot_update(self, *args):
        
        status_update = list(self.widgets['filter'].value)
        self.widgets['bar'].x = np.array(self.paras['df_by_sla'].index)
        self.widgets['bar'].y = [self.paras['df_by_sla'][i] for i in status_update]
        self.widgets['bar'].labels = status_update
        self.widgets['bar'].colors = [self.paras['colorscheme'][i] for i in status_update]
    
    
    def _plot_other(self):
              
        self.widgets['label'] = widgets.HTML(value=
        '<b style="color: #ff0000">{}%</b> of Terminal requests in \
        the imported period are out of Bloomberg SLA (not actioned within 5 days)'
            .format(self.paras['out_sla_rate'])
        )
        
        
        self.widgets['slider'] = widgets.IntSlider(
                                                    value=5,
                                                    min=1,
                                                    max=30,
                                                    step=1,
                                                    description='',
                                                    disabled=False,
                                                    continuous_update=False,
                                                    orientation='vertical',
                                                    readout=True,
                                                    readout_format='d'
                                                )
        
        self.widgets['filter'] = widgets.SelectMultiple(
                                                        options=list(self.paras['all_status']),
                                                        value=list(self.paras['all_status']),
                                                        #rows=10,
#                                                             description='Year',
                                                        disabled=False,
                                                        layout=widgets.Layout(
                                                            width='120px', height='80px'
                                                        )
                                                        )
        
        
        self.widgets['filter'].observe(self._plot_update, 'value')
        self.widgets['slider'].observe(self._sla_update, 'value')
        
        
    def _sla_update(self, *arg): #update because of sla slider change 
        
        self._data_process(self.df_in, self.df_pb, self.widgets['slider'].value)
        self._plot_update_all()
        
    
    def _full_update(self, df_in, df_pb): #update because df_in/df_pb change
        
        self._data_process(df_in, df_pb, self.widgets['slider'].value)
        
        self.widgets['bar'].x=np.array(self.paras['df_by_sla'].index) #new add
        
        self._plot_update_all()
        
        
    def _plot_update_all(self):
        
        self.widgets['bar'].y=[self.paras['df_by_sla'][i] for i in self.paras['all_status']]
        self.widgets['bar'].colors=self.paras['bar_colors']
        self.widgets['bar'].labels=self.paras['all_status']
        self.widgets['bar_fig'].title = "Entitlements Requests by {}-day SLA".format(self.widgets['slider'].value)
        
        self.widgets['filter'].options=list(self.paras['all_status'])
        self.widgets['filter'].value=list(self.paras['all_status'])
        
        self.widgets['label'].value = '<b style="color: #ff0000">{}%</b> of Terminal requests in \
        the imported period are out of Bloomberg SLA (not actioned within {} days)' \
            .format(self.paras['out_sla_rate'], self.widgets['slider'].value)        
        
        
    def show(self):
        return self.widgets['bySLA']
    