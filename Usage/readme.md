# Data usage analysis
  
## Introduction
  This is an introduction of the app that I create to visualize and analyze data usage. Some information is hidden due to compliance concern.
  
**Navigator:**
* [Start the app](#start-the-app)
* [Prepare raw data](#prepare-raw-data)
* [Copy and paste the directory path](#copy-and-paste-the-directory-path)
* [The App](#the-app)
* [App design logic and features](#app-design-logic-and-features)

  
## Start the app

(information hidden)

[Back to top](#data-usage-analysis)


## Prepare raw data

(Information hidden)

Download the data.

[Back to top](#data-usage-analysis)

## Copy and paste the directory path

(Information hidden)

Import the data.

## The App

Three major sections (see screenshot below):
*	Filters: “Year”, “Month”, and “Class” filters are applied to all charts and tables. “Top Display” works for “Top Read Headlines”, “Top Analyst/Tickers”, and “Readers Profile” visuals.
*	Visual tabs: change views by clicking the tab.
*	Main view: view and other interactive tool section.

![Sections](/Screenshots/6.jpg)

### Reads Trend

Display total reads (bar chart) and reads by class (line chart) with options of different frequency (year, quarter, and month). “Year”, “Month”, and “Class” filters are applicable. You could also hover your mouse over to check the data point. Screenshots are below.

![Reads Trend](/Usage/Screenshots/7.PNG)

### Daily Trends

Select range to see reads during that period based on filters (“Year”, “Month”, “Class”) applied. 


![Daily Trends](/Usage/Screenshots/8.png)

### Top Reads Headlines

All filters are applicable for this view, especially “Top Display”. Hover mouse over the bar to check details of that headline. Click on the bar to filter details of the headline(s) in the below table. Click blank area in the chart to unselect. Note that there may be a delay once you click on the bar to filter details in the table if data size is large. A restriction of maximum 5000 records is applied to the table due to efficiency concern.

![Top Headlines](/Usage/Screenshots/9.jpg)

When top 30 filter is applied (one could scroll down in the app to see details in table):

![Top 30](/Usage/Screenshots/10.jpg)

### Top Analysts/Tickers

All filters are applicable for this view, especially “Top Display”. In the screenshot below, top 20 is selected.

![Analysts/Tickers](/Usage/Screenshots/11.jpg)

The numbers are counted by how many times the analysts/tickers appear in the imported raw data file from column “Author(s)” and “Primary Supplied Ticker(s)” in the new readership files. If contributor’s reports are not tagged properly, these charts may not be useful.

### Readers Profile

All filters are applicable for this view, especially “Top Display”. In the screenshot below, top 10 is selected. Please note that “Free content”, deleted users, and “Embargoed” records are not included in these charts.

![Readers Profile](/Usage/Screenshots/12.jpg)

### Reads Map

Display reads in world map view. “Year”, “Month”, and “Class” filters are applicable. Country in darker color means more reads are from that country. Click on the map to see customer level information in the table below. Click blank area to select all.

![Reads Map](/Usage/Screenshots/13.jpg)

Please note that some regions which are small in size are not visible in the map (e.g. Hong Kong), so you could not select them directly in the map but filter them by clicking the right-bottom of “Customer Country” header (see screenshot below). 

![Datagrid](/Usage/Screenshots/14.png)

[Back to top](#data-usage-analysis)

## App design logic and features

Summary of what have been taken care of and what are available:

- Import and process the data:
  (information hidden)

- Visualize the data so it’s more readable:
  - Show the readership trends by different frequency and class;
  - Show the most popular read reports with ability to dig into details;
  - Show the most popular read analysts and tickers (according to reports tagging);
  - Show the most frequent readers’ profile;
  - Show the readers allocation map;
  
- Interaction:
  - User could select certain year, month, and class to see how data look like, and these three filters apply to all visualization charts; and top maximum filter applies for headlines, analyst/tickers, and profiles charts;
  - Interval selection and calculation is allowed for daily trend charts;
  - User could select headline to see more details of the reads related to that story in table;
  - Map chart is allowed to select country to see more details in table.
  
  
*For anyone who is interested in the bqnt project, I have provided the source codes of visualization parts in "Scripts" folder, feel free to check.*

[Back to top](#data-usage-analysis)

>Created by West Wang
