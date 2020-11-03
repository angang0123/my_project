import ipywidgets as widgets
from ipydatagrid import DataGrid, TextRenderer
import pandas as pd
import numpy as np
import datetime as dt

from bqplot import (OrdinalScale, LinearScale, Bars, Label, Figure, Axis, CATEGORY10, Tooltip)
from bqplot import ColorScale, ColorAxis


class byPKG:
    
    def __init__(self, df_in, df_pb):
        
        self.df_in = df_in
        self.df_pb = df_pb
        
        self.widgets = dict()
        self.paras = dict()
        
        self._data_process(df_in, df_pb)
        self.widgets['user_plot'], self.widgets['user_fig'] = self._plot("User")
        self.widgets['cust_plot'], self.widgets['cust_fig'] = self._plot("Cust")

        
        self._plot_other()

        self.widgets['byPKG'] = widgets.VBox([
                                            self.widgets['user_fig'],
                                            self.widgets['cust_fig'],
                                            self.widgets['dg']
        ])
        
    
    def _data_process(self, df_in, df_pb):
        
        self.paras['pkg_user'] = pd.concat([
                                df_in[['Package', 'by_mon', 'Requester', 'Requester Email', 'UUID', 'Request ID']], 
                                df_pb[['Package', 'by_mon', 'Requester', 'Requester Email', 'UUID', 'Request ID']]
                                ], axis=0)
        self.paras['pkg_user'] = self.paras['pkg_user'].drop_duplicates(keep='first')
        
        self.paras['dg'] = pd.concat([
                                df_in[['Package', 'by_mon', 'Created', 'Customer', 'Ctry', 'Request ID']], 
                                df_pb[['Package', 'by_mon', 'Created', 'Customer', 'Ctry', 'Request ID']]
                                ], axis=0)
        self.paras['dg']['Created'] = self.paras['dg']['Created'].dt.strftime("%Y-%m-%d")
        self.paras['pkg_cust'] = self.paras['dg'].drop_duplicates(
                                    subset=['Package', 'Created', 'Customer', 'Ctry', 'by_mon'], keep='first'
                                    )
        
        
        self.paras['df_pkg_user'] = pd.pivot_table(self.paras['pkg_user'], values='Request ID',
                                            columns=['Package'], index=['by_mon'],
                                             aggfunc='count', fill_value=0)
        self.paras['df_pkg_cust'] = pd.pivot_table(self.paras['pkg_cust'], values='Request ID',
                                            columns=['Package'], index=['by_mon'],
                                             aggfunc='count', fill_value=0)
        self.paras['df_dg'] = pd.pivot_table(self.paras['dg'], values='Request ID',
                                            index=['Created', 'by_mon', 'Package', 'Customer'],
                                             aggfunc='count')
        self.paras['df_dg'].columns = ["Total Req"]
        self.paras['df_dg'].reset_index(inplace=True)
        
        
        self.paras['all_pkg'] = list(self.paras['df_pkg_user'].columns)
          
                  
    def _plot(self, user_cust):
        
        x_ord = OrdinalScale()
        
        if user_cust=="User":
            plot_x = np.array(self.paras['df_pkg_user'].index)
            if len(self.paras['all_pkg'])==1:
                plot_y = self.paras['df_pkg_user'].T
                plot_colors = ['#1f77b4']
            else:
                plot_y = [self.paras['df_pkg_user'][i] for i in self.paras['all_pkg']]
                plot_colors = CATEGORY10
            y_sc = LinearScale(max=self.paras['df_pkg_user'].sum(axis=1).max()*1.1)
            
        elif user_cust=="Cust":
            plot_x = np.array(self.paras['df_pkg_cust'].index)
            if len(self.paras['all_pkg'])==1:
                plot_y = self.paras['df_pkg_cust'].T
                plot_colors = ['#1f77b4']
            else:
                plot_y = [self.paras['df_pkg_cust'][i] for i in self.paras['all_pkg']]
                plot_colors = CATEGORY10 
            y_sc = LinearScale(max=self.paras['df_pkg_cust'].sum(axis=1).max()*1.1) 
       
        
        
        if user_cust=="User":
            bar = Bars(x=plot_x, 
                       y=plot_y,
                       scales={'x': x_ord, 'y': y_sc,}, 
                       padding=0.3, 
                       colors=plot_colors,
                       display_legend=True, 
                       labels=self.paras['all_pkg'],
                      tooltip=Tooltip(fields=['x', 'y'], labels=['Month', 'Number of requests by user'])
                      )
            bar_label = self.paras['df_pkg_user'].sum(axis=1)
        elif user_cust=="Cust":
            bar = Bars(x=plot_x, 
                   y=plot_y,
                   scales={'x': x_ord, 'y': y_sc,}, 
                   padding=0.3, 
                   interactions={'click': 'select',
                             'hover':'tooltip'},
                   unselected_style={'opacity': .5},
                   colors=plot_colors,
                   display_legend=False, 
#                    labels=self.paras['all_pkg'],
                  tooltip=Tooltip(fields=['x', 'y'], labels=['Month', 'Number of requests by user'])
                  )
            bar_label = self.paras['df_pkg_cust'].sum(axis=1)
            bar.observe(self.on_bar_click, names='selected')
            

        mark_text = Label(x=plot_x,
                      y=bar_label,
                      align='middle',
                      font_weight='normal',
                      y_offset=-10,
                      colors=['white'],
                      default_size=12,
                      scales={'x': x_ord, 'y': y_sc},
                      text=bar_label #[value for value in bar_label]
                         )
            

        ax_x = Axis(scale=x_ord, tick_rotate=-45, 
        #             label_offset='300ex',
        #             label_location='start',
                    grid_lines='none',
                   offset={'value':-0.8})
        ax_y = Axis(scale=y_sc, orientation='vertical', tick_format=',d', grid_lines='dashed')

        fig = Figure(marks=[bar, mark_text], axes=[ax_x, ax_y], legend_location='top')
        fig.title = "{} Entitlements Requests".format(user_cust)
        fig.layout.width = '800px'
        fig.layout.height = '300px'
        
        return bar, fig
    
    def on_bar_click(self, evt=None):
        if evt is not None and evt['new'] is not None:
            selected = [self.widgets['cust_fig'].marks[0].x[i] for i in evt['new']]
            filter_df = \
                self.paras['df_dg'][self.paras['df_dg']['by_mon'].isin(selected)]
            self.widgets['dg'].data = filter_df[['Package', 'Customer', 'Created', 'Total Req']]
        else:
            self.widgets['dg'].data = self.paras['df_dg'][['Package', 'Customer', 'Created', 'Total Req']]

    
    def _full_update(self, df_in, df_pb):
        
        self._data_process(df_in, df_pb)
        
        user_label = self.paras['df_pkg_user'].sum(axis=1)
        cust_labe = self.paras['df_pkg_cust'].sum(axis=1)
        
        self.widgets['user_plot'].x = np.array(self.paras['df_pkg_user'].index)
        self.widgets['user_fig'].marks[1].x = np.array(self.paras['df_pkg_user'].index)
        
        if len(self.paras['all_pkg'])==1:
            self.widgets['user_plot'].y = self.paras['df_pkg_user'].T
            self.widgets['user_plot'].colors=['#1f77b4']
        else:
            self.widgets['user_plot'].y = [self.paras['df_pkg_user'][i] for i in self.paras['all_pkg']]
            self.widgets['user_plot'].colors=CATEGORY10
            
        self.widgets['user_plot'].labels = self.paras['all_pkg']
        
        
        self.widgets['cust_plot'].x = np.array(self.paras['df_pkg_cust'].index)
        self.widgets['cust_fig'].marks[1].x = np.array(self.paras['df_pkg_cust'].index)
        
        if len(self.paras['all_pkg'])==1:
            self.widgets['cust_plot'].y = self.paras['df_pkg_cust'].T
            self.widgets['cust_plot'].colors=['#1f77b4']
        else:
            self.widgets['cust_plot'].y = [self.paras['df_pkg_cust'][i] for i in self.paras['all_pkg']]
            self.widgets['cust_plot'].colors=CATEGORY10
            
        self.widgets['user_fig'].axes[1].scale.max=user_label.max()*1.1
        self.widgets['user_fig'].marks[1].y = user_label
        self.widgets['user_fig'].marks[1].text = user_label
        
        self.widgets['cust_fig'].axes[1].scale.max=cust_labe.max()*1.1
        self.widgets['cust_fig'].marks[1].y = cust_labe
        self.widgets['cust_fig'].marks[1].text = cust_labe
        
        
        
        self.widgets['dg'].data = self.paras['df_dg'][['Package', 'Customer', 'Created', 'Total Req']]
        
        

    def _plot_other(self):
        
        self.widgets['dg'] = DataGrid(self.paras['df_dg'][['Package', 'Customer', 'Created', 'Total Req']], 
                                                base_column_size=50, layout={'height':'200px'},
                                     column_widths={'Package':200, 'Customer':300, 
                                                   'Created':70, 'Total Req':100},
                                     renderers={'Created': TextRenderer(format='%Y/%m/%d', format_type='time')})
        
    
    def show(self):
        return self.widgets['byPKG']
    