import ipywidgets as widgets
from ipydatagrid import DataGrid, TextRenderer
import pandas as pd
import numpy as np
import time

from bqplot import (OrdinalScale, LinearScale, Bars, Lines, Label, Figure, Axis, CATEGORY10, Tooltip)
from bqplot import ColorScale, ColorAxis

class byStatus:
    
    def __init__(self, df_in, df_pb):
        
        self.df_in = df_in
        self.df_pb = df_pb
        
        self.widgets = dict()
        self.paras = dict()
        
        self._init_data_process(df_in, df_pb)
        self._data_process(df_in)
        
        self._plot_status()
        self._plot_other()
        self._plot_action()
        
        
        self.widgets['byStatus'] = widgets.VBox([
                                        widgets.HBox([
                                            widgets.VBox([
                                                widgets.Label(value=None, width='80px', height='300px'),
                                                widgets.Label(value="Status Filter"),
                                                self.widgets['filter']
                                                ]), 
                                            self.widgets['bar_fig']    
                                            ]),
                                        self.widgets['label'],
                                        widgets.HBox([
                                            widgets.Label(value="-----------------", width='80px', height='300px'),
                                            self.widgets['action_fig']
                                        ]),
                                        self.widgets['dg']
                                        ])
        
    
    def _init_data_process(self, df_in, df_pb):
        
        self.df = pd.concat([df_in[['Request ID', 'Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status', 'by_mon']],
                        df_pb[['Request ID', 'Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status', 'by_mon']]],
                      axis=0)
        
        
        self.paras['df_by_status'] = pd.pivot_table(self.df, values='Request ID', 
                               columns=['Status'], index=['by_mon'], 
                               aggfunc='count', fill_value=0
                              )
        self.paras['all_status'] = self.paras['df_by_status'].columns
        self.paras['sum_by_status'] = self.paras['df_by_status'].sum(axis=1)
        self.paras['df_by_status'] = (self.paras['df_by_status'].div(self.paras['sum_by_status'], axis=0)).round(5)
        
        self.paras['colorscheme'] = {'A':"#33cc33", 'MA':"#00e6e6", 'E':"#8c8c8c", 'R':"#ff0000", 'W':"#0066ff", 'PB':"#ffff1a"}
        self.paras['bar_colors'] = [self.paras['colorscheme'][i] for i in self.paras['all_status']]
        self.paras['legend_map'] = {'A': 'A: Approved via Request Tracker', 'E': 'E: Expired after 30 days',
                                     'MA': 'MA: Manual Approved via ENTA Function', 
                                     'R': 'R: Rejected via Request Tracker', 'W': 'W: Withdraw via Request Tracker',
                                     'PB': 'PB: Pending Broker Action'}
    
        
    def _data_process(self, df_in):
        
        df_in = df_in.assign(delta=(df_in['Closed']-df_in['Created']).dt.days)
        
        if 'bar_fig' in self.widgets:
            if self.widgets['bar_fig'].marks[0].selected is None:
                bar_selected = self.widgets['bar_fig'].marks[0].x
            else:
                bar_selected = self.widgets['bar_fig'].marks[0].x[self.widgets['bar_fig'].marks[0].selected]
                
            if bar_selected is None:
                bar_selected = self.widgets['bar_fig'].marks[0].x        
            self.paras['dg'] = self.df[self.df['by_mon'].isin(bar_selected)]\
                            [['Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status']]
            df_in = df_in[df_in['by_mon'].isin(bar_selected)]
        else:
            self.paras['dg'] = self.df[['Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status']]
            
        if 'filter' in self.widgets:
            self.paras['dg'] = self.paras['dg'][self.paras['dg']['Status'].isin(list(self.widgets['filter'].value))]
        
        self.paras['test'] = df_in
        
        self.paras['df_action'] = pd.pivot_table(df_in, 
                                                 index=['delta'], values='Request ID', 
                                                 aggfunc='count', fill_value=0)
        self.paras['df_action'] = self.paras['df_action'].reindex(
                                                pd.Int64Index(range(31)), fill_value=0)

        
        #average days actioned on individual request
        self.paras['user_req_avg'] = \
                self.paras['df_action']['Request ID'].mul(self.paras['df_action'].index).sum()\
                                        /self.paras['df_action'].sum()
        self.paras['user_req_avg'] = float(round(self.paras['user_req_avg'], 2))
        #average days actioned on cust request (req from the same cust on one day counts once)
        df_cust = df_in[['Package','Created','Customer','delta']]
        df_cust = df_cust.drop_duplicates(subset=['Package','Created','Customer','delta'], keep='first')
        self.paras['df_cust'] = pd.pivot_table(df_cust,
                                                index=['delta'], values='Customer',
                                                aggfunc='count', fill_value=0)
        self.paras['cust_req_avg'] = \
                self.paras['df_cust']['Customer'].mul(self.paras['df_cust'].index).sum()\
                                        /self.paras['df_cust'].sum()
        self.paras['cust_req_avg'] = float(round(self.paras['cust_req_avg'], 2))
        
        
        
        
    def _plot_status(self):
        
        x_ord = OrdinalScale()
        y_sc = LinearScale(max=1.65, min=-.1)

        self.widgets['bar'] = Bars(x=np.array(self.paras['df_by_status'].index), 
                   y=[self.paras['df_by_status'][i] for i in self.paras['all_status']],
                   scales={'x': x_ord, 'y': y_sc,}, 
                   interactions={'click': 'select','hover':'tooltip'},
                   unselected_style={'opacity': .5},
                   padding=0.3, 
                   colors=self.paras['bar_colors'],
                   display_legend=True, 
                   labels=[self.paras['legend_map'][i] for i in self.paras['all_status']],
                  tooltip=Tooltip(fields=['x', 'y'], labels=['Month', 'Action Percentage'])
                  )
        self.widgets['bar'].observe(self._on_bar_click, names='selected')
        
        bar_value = self.paras['df_by_status'].sum(axis=1)
        bar_text = [str(round(i*100,2))+"%" for i in (self.paras['df_by_status'].sum(axis=1))]
        
        self.widgets['bar_text'] = Label(x=np.array(self.paras['df_by_status'].index),
                      y=bar_value,
                      align='middle',
                      font_weight='normal',
                      y_offset=-10,
                      colors=['white'],
                      default_size=12,
                      scales={'x': x_ord, 'y': y_sc},
                      text=bar_text #[value for value in bar_label]
                         )
        

        ax_x = Axis(scale=x_ord, tick_rotate=-90, 
#                     label_offset='50px',
        #             label_location='start',
                    grid_lines='none',
                   offset={'value':-0.8})
        ax_y = Axis(scale=y_sc, orientation='vertical', tick_format='0.0%', grid_lines='dashed')

        self.widgets['bar_fig'] = Figure(marks=[self.widgets['bar'],self.widgets['bar_text']], axes=[ax_x, ax_y], legend_location='top')
        self.widgets['bar_fig'].title = "Entitlements Requests by Status"
        self.widgets['bar_fig'].layout.width = '800px'
        self.widgets['bar_fig'].layout.height = '500px'
#         self.widgets['bar_fig'].fig_margin = {'bottom':0,'top':0}
        
    
    def _plot_action(self):
        
        x_ord = LinearScale(min=0, max=30)
        y_sc = LinearScale(min=0)
        
        self.widgets['action'] = Bars(x=np.array(self.paras['df_action'].index), 
                   y=np.array(self.paras['df_action']).T,
                   scales={'x': x_ord, 'y': y_sc,}, 
                   padding=0.3,
                   colors=['#00e68a'],
                   tooltip=Tooltip(fields=['x', 'y'], labels=['On day', '#Req Handled'])
                  )
        
        self.widgets['cust_line'] = Lines(x=[self.paras['cust_req_avg'],self.paras['cust_req_avg']],
                                  y=[0,max(self.paras['df_action']['Request ID'])],
                  scales={'x': x_ord, 'y': y_sc,}, 
                  stroke_width=3,colors=['#e6e600'],line_style='dashed'
                  ,display_legend=True
                  ,labels=['Customer req {} days on average'.format(self.paras['cust_req_avg'])]
                                         )
        
        self.widgets['user_line'] = Lines(x=[self.paras['user_req_avg'],self.paras['user_req_avg']],
                                  y=[0,max(self.paras['df_action']['Request ID'])],
                  scales={'x': x_ord, 'y': y_sc,}, 
                  stroke_width=3,colors=['#e67300'],line_style='dotted'
                  ,display_legend=True
                  ,labels=['Individual req {} days on average'.format(self.paras['user_req_avg'])]
                                         )
        
        ax_x = Axis(scale=x_ord, label="Days before action",
#                     label_offset='5ex',
        #             label_location='start',
                    grid_lines='none',
                   offset={'value':-0.8})
        ax_y = Axis(scale=y_sc, orientation='vertical', tick_format=',d', grid_lines='dashed')

        self.widgets['action_fig'] = Figure(
                        marks=[self.widgets['action'], self.widgets['cust_line'], self.widgets['user_line']],
                        legend_location='top-right',
                        axes=[ax_x, ax_y])
        self.widgets['action_fig'].layout.width = '800px'
        self.widgets['action_fig'].layout.height = '250px'
    
        
    def _on_bar_click(self, evt):
        
        status_update = list(self.widgets['filter'].value)
            
        df_in = self.df_in[self.df_in['Status'].isin(status_update)]
            
        self._data_process(df_in)

        self.widgets['action'].y = np.array(self.paras['df_action']).T

        self.widgets['cust_line'].x = [self.paras['cust_req_avg'],self.paras['cust_req_avg']]
        self.widgets['cust_line'].y = [0,max(self.paras['df_action']['Request ID'])]
        self.widgets['cust_line'].labels=['Customer req {} days on average'.format(
                                                                self.paras['cust_req_avg'])]
        
        self.widgets['user_line'].x = [self.paras['user_req_avg'],self.paras['user_req_avg']]
        self.widgets['user_line'].y = [0,max(self.paras['df_action']['Request ID'])]
        self.widgets['user_line'].labels=['Individual req {} days on average'.format(
                                                                self.paras['user_req_avg'])]
        
        self.widgets['dg'].data = self.paras['dg']

        
        
    def _filter_update(self, *args): #change filter
        
        status_update = list(self.widgets['filter'].value)
        #select status -> filter action data
        if status_update == ["PB"]:
            pass
        else:
            df_in = self.df_in[self.df_in['Status'].isin(status_update)]
            self._data_process(df_in)
        
        self._plot_update(status_update)
        
        
    def _plot_update(self, status_update):
        
        self.widgets['bar'].y = [self.paras['df_by_status'][i] for i in status_update]
        self.widgets['bar'].labels = [self.paras['legend_map'][i] for i in status_update]
        self.widgets['bar'].colors = [self.paras['colorscheme'][i] for i in status_update]
        
        bar_value = self.paras['df_by_status'][status_update].sum(axis=1)
        bar_text = [str(round(i*100,2))+"%" for i in bar_value]
        self.widgets['bar_text'].y = bar_value
        self.widgets['bar_text'].text = bar_text
        
        if status_update == ["PB"]:
            self.widgets['action'].y = np.array([0]*31)
            self.widgets['cust_line'].x = [30, 30]
            self.widgets['cust_line'].y = [0,10]
            self.widgets['cust_line'].labels=['Pending to act']
            
            self.widgets['user_line'].x = [30, 30]
            self.widgets['user_line'].y = [0,10]
            self.widgets['user_line'].labels=['Pending to act']
        else: 
                
            self.widgets['action'].y = np.array(self.paras['df_action']).T

            self.widgets['cust_line'].x = [self.paras['cust_req_avg'],self.paras['cust_req_avg']]
            self.widgets['cust_line'].y = [0,max(self.paras['df_action']['Request ID'])]
            self.widgets['cust_line'].labels=['Customer req {} days on average'.format(
                                                                    self.paras['cust_req_avg'])]

            self.widgets['user_line'].x = [self.paras['user_req_avg'],self.paras['user_req_avg']]
            self.widgets['user_line'].y = [0,max(self.paras['df_action']['Request ID'])]
            self.widgets['user_line'].labels=['Individual req {} days on average'.format(
                                                                    self.paras['user_req_avg'])]
            
        self.widgets['dg'].data = self.paras['dg'][self.paras['dg']['Status'].isin(status_update)]
#         self.df[self.df['Status'].isin(status_update)][['Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status']]


        
    def _plot_other(self):
        
        self.paras['expire_req'] = (self.df_in['Status']=='E').sum()
        self.paras['total_req'] = self.df_in['Status'].count() + self.df_pb['Status'].count()
        self.paras['expire_rate'] = round(self.paras['expire_req']/self.paras['total_req']*100, 2)
        
        self.widgets['label'] = widgets.HTML(value=
        '<b style="color: #ff0000">{}%</b> of Terminal requests in \
        the imported period have expired (not approved or rejected within 30 days)'.format(self.paras['expire_rate'])
        )
        
        self.widgets['filter'] = widgets.SelectMultiple(
                                                        options=list(self.paras['all_status']),
                                                        value=list(self.paras['all_status']),
                                                        #rows=10,
#                                                             description='Year',
                                                        disabled=False,
                                                        layout=widgets.Layout(
                                                            width='80px', height='110px'
                                                        )
                                                        )
        self.widgets['filter'].observe(self._filter_update, 'value')
        
        
        
        self.widgets['dg'] = DataGrid(self.paras['dg'], 
                                                base_column_size=50, layout={'height':'200px'},
                                     column_widths={'Package':150, 'Requester':200, 'Customer':200, 'Ctry':70, 
                                                   'Created':70, 'Status':70},
                                     renderers={'Created': TextRenderer(format='%Y/%m/%d', format_type='time')})
        
        
    def _full_update(self, df_in, df_pb):
        
        self.df_in = df_in
        self.df_pb = df_pb
        
        self.df = pd.concat([df_in[['Request ID', 'Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status', 'by_mon']],
                        df_pb[['Request ID', 'Package', 'Requester', 'Customer', 'Ctry', 'Created', 'Status', 'by_mon']]],
                      axis=0)
        
        self.paras['df_by_status'] = pd.pivot_table(self.df, values='Request ID', 
                               columns=['Status'], index=['by_mon'], 
                               aggfunc='count', fill_value=0
                              )
        self.paras['all_status'] = self.paras['df_by_status'].columns
        self.paras['sum_by_status'] = self.paras['df_by_status'].sum(axis=1)
        self.paras['df_by_status'] = (self.paras['df_by_status'].div(self.paras['sum_by_status'], axis=0)).round(5)
        
        self.widgets['filter'].unobserve(self._filter_update, 'value')       
        self.widgets['filter'].options = list(self.paras['all_status'])
        self.widgets['filter'].value = list(self.paras['all_status'])
        self.widgets['filter'].observe(self._filter_update, 'value')
             
        
        self._data_process(df_in)
        
        self.widgets['bar'].x = np.array(self.paras['df_by_status'].index) #new add
        self.widgets['bar_text'].x = np.array(self.paras['df_by_status'].index) #new add
        self.widgets['action'].x = np.array(self.paras['df_action'].index) #new add
        
        self._plot_update(list(self.paras['all_status']))
        
        self.paras['expire_req'] = (df_in['Status']=='E').sum()
        self.paras['total_req'] = df_in['Status'].count() + df_pb['Status'].count()
        self.paras['expire_rate'] = round(self.paras['expire_req']/self.paras['total_req']*100, 2)
        
        self.widgets['label'].value = '<b style="color: #ff0000">{}%</b> of Terminal requests in \
                                        the imported period have expired (not approved or rejected within 30 days)'.format(self.paras['expire_rate'])   
        
        
    def show(self):
        return self.widgets['byStatus']