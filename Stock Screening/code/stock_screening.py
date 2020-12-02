import pandas as pd
import numpy as np
from ipywidgets import Dropdown, FloatRangeSlider, DatePicker, SelectMultiple, Button, VBox, HBox, Layout, Label, Textarea
from ipydatagrid import DataGrid, TextRenderer
import datetime as dt

from bqplot import (OrdinalScale, LinearScale, Hist, Figure, Axis, CATEGORY10, Tooltip, Bars)
from bqplot import ColorScale, ColorAxis
from bqplot.interacts import BrushIntervalSelector

from IPython.display import display


class visualization:
    def __init__(self, df, num_params):

        self.df = df
        self.slided_df = df
        self.colors = ['#ff0000', '#00e6b8', '#ff9900', '#cce6ff', '#ff00aa', '#8600b3']
        self.num_chart = num_params

        self.fig = {}
        self.bin = {}
        self.slider = {}
        self.widgets = {}
        self.plot_init_chart()

    def plot_init_chart(self):

        for i in range(self.num_chart):
            x_ls = LinearScale()
            y_ls = LinearScale(min=0)

            plot = Hist(sample=[0], scales={'sample': x_ls, 'count': y_ls}, colors=[self.colors[i]], stroke='black',
                        bins=10,
                        interactions={'click': 'select', 'hover': 'tooltip'},
                        unselected_style={'opacity': .5},
                        tooltip=Tooltip(fields=['count'], labels=['Count'])
                        )

            plot.observe(self._bar_click)

            xax = Axis(scale=x_ls, grid_lines='none')
            yax = Axis(scale=y_ls, tick_format=',d', grid_lines='none', orientation='vertical')

            fig = Figure(marks=[plot], axes=[xax, yax]
                         , padding_x=0., padding_y=0.
                         )

            fig.title = 'Histogram: {}'.format(i)

            fig.layout.width, fig.layout.height = '400px', '220px'
            fig.fig_margin = {'bottom': 40, 'left': 60, 'right': 20, 'top': 40}

            self.fig[i] = fig

            bin_picker = Dropdown(options=[10, 20, 50, 100], description='bar number',
                                  style={'description_width': 'initial'}, value=10
                                  , layout=Layout(width='150px'))
            bin_picker.observe(self._bin_change, 'value')
            self.bin[i] = bin_picker

            range_slider = FloatRangeSlider(
                value=[0, 0],
                min=0,
                max=0,
                step=0.1,
                description='Range:',
                disabled=False,
                continuous_update=False,
                orientation='horizontal',
                #                                             readout=True,
                #                                             readout_format='.2f',
                layout=Layout(width='400px')
            )
            range_slider.observe(self._slider_filter_update, 'value')
            self.slider[i] = range_slider

            self.widgets[i] = VBox([bin_picker, range_slider, fig])

            self.datagrid = DataGrid(self.df, base_column_size=80, layout={'height': '300px'},
                                     column_widths={'ID': 120, 'Company Name': 180, 'GICS Sector': 120},
                                     renderers={
                                         'DATE': TextRenderer(format='%Y/%m/%d', format_type='time'),
                                         'AS_OF_DATE': TextRenderer(format='%Y/%m/%d', format_type='time'),
                                         'Market Cap': TextRenderer(format=',.2f'),
                                         # IS
                                         'Revenue': TextRenderer(format=',.2f'),
                                         'Net Income': TextRenderer(format=',.2f'),
                                         # IS ratio
                                         'Gross Margin': TextRenderer(format='.2f'),
                                         'Operating Margin': TextRenderer(format='.2f'),
                                         'NI Margin': TextRenderer(format='.2f'),
                                         # BS
                                         'Cash & Equiv': TextRenderer(format=',.2f'),
                                         'CA': TextRenderer(format=',.2f'),
                                         # BS ratio

                                         # exchange
                                         'Price': TextRenderer(format='.2f'),
                                         'Volume': TextRenderer(format='.2d'),
                                         # other ratios
                                         'PE Ratio': TextRenderer(format='.2f'),
                                         'ROE': TextRenderer(format='.2f'),
                                         'ROA': TextRenderer(format='.2f'),
                                         'EPS': TextRenderer(format='.2f'),
                                         'Dvd Payout Ratio': TextRenderer(format='.2f')
                                     }
                                     )

        self.widgets['vs'] = VBox([
            HBox([self.widgets[0], self.widgets[1], self.widgets[2]]),
            HBox([self.widgets[3], self.widgets[4], self.widgets[5]]),
            self.datagrid
        ])

    def _bin_change(self, *arg):

        for i in range(self.num_chart):
            if self.bin[i].value != self.fig[i].marks[0].bins:
                self.fig[i].marks[0].bins = self.bin[i].value
                self.slider[i].step = (self.slider[i].max - self.slider[i].min) / (self.bin[i].value + 1)

    def _bar_click(self, evt=None):

        dg_index = list(range(len(self.slided_df.index)))

        for i in range(self.num_chart):
            if (np.nansum(self.fig[i].marks[0].sample) > 0) and (
                    self.fig[i].marks[0].selected is not None):  # not empty
                dg_index = list(set(dg_index).intersection(list(self.fig[i].marks[0].selected)))

        self.datagrid.transform([{'type': 'filter',
                                  'columnIndex': 0,
                                  'operator': 'in',
                                  'value': list(self.slided_df.iloc[dg_index].index)}])

    def _chart_update(self, df):

        global select_params

        for i in range(len(select_params.value)):
            param = list(select_params.value)[i]
            self.fig[i].title = 'Parameters: {}'.format(param)
            self.fig[i].marks[0].sample = df[param]
            self.fig[i].marks[0].selected = None

        self.datagrid.data = df

    def _slider_chart_update(self, df):

        global select_params

        self.df = df
        self.slided_df = df

        for i in range(len(select_params.value)):
            param = list(select_params.value)[i]
            self.slider[i].unobserve(self._slider_filter_update, 'value')
            if np.nanmax(df[param]) >= self.slider[i].min:
                self.slider[i].max = np.nanmax(df[param]) + 1
                self.slider[i].min = np.nanmin(df[param]) - 1
            elif np.nanmin(df[param]) <= self.slider[i].max:
                self.slider[i].min = np.nanmin(df[param]) - 1
                self.slider[i].max = np.nanmax(df[param]) + 1
            self.slider[i].value = [self.slider[i].min, self.slider[i].max]
            self.slider[i].step = (self.slider[i].max - self.slider[i].min) / (self.bin[i].value + 1)
            self.slider[i].observe(self._slider_filter_update, 'value')

        self._chart_update(df)

    def _slider_filter_update(self, evt=None):

        slider_idx = self.df.index != False

        for i in range(len(select_params.value)):
            param = list(select_params.value)[i]
            slider_idx = slider_idx & (
                        (self.slider[i].value[0] <= self.df[param]) & (self.df[param] <= self.slider[i].value[1]) |
                        self.df[param].isna())

        self.slided_df = self.df[slider_idx]
        self._chart_update(self.slided_df)


