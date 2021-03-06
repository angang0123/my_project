# Entitlement Analysis Tool

Want to know how contributor performs on their entitlement requests? How did they perform historically? Is there a difference between packages? How do they perform in regard of entitlement SLA?

There's a tool will help you with all these and more than that. It could help you explore more information that hidden behind the static request data from ENTA requests. It provides you some dimensions to view the data deeper and also gives you the ability to dig more based on your expertise.

This tutorial will walk you through the functionalities of this tool.

![SLA Evolves](https://github.com/angang0123/my_project/blob/main/Entitlement%20Analysis%20Tool/images/sla_evolves.gif)

It contains the following sections:
* [How to get the source data](#how-to-get-source-data);
* [How to run the app](#how-to-run-the-app);
* [What are the functionalities](#what-are-the-functionalities):
  * Requests analysis based on action status in time series;
  * Requests analysis based on packages in time series;
  * Entitlement SLA baseline reference.
 * [Source code](#source-code)
  
  
[Back to top](#entitlement-analysis-tool)

## How to get the source data

(information hidden)


[Back to top](#entitlement-analysis-tool)


## How to run the app

(information hidden)

[Back to top](#entitlement-analysis-tool)


##  What are the functionalities

On the top level, there are four parts of the app:

* [Package filter](#package-filter): it applies to the whole app, it is used to select which package(s) that you would like to analyze;
* [Status Analysis tab](#status-analysis-tab): it helps analyze how this contributor/admin performs for different types of entitlement actions status in time series;
* [Requests Details tab](#requests-details-tab): it helps how the requests look like on user/customer level by package in time series;
* [SLA Analysis tab](#sla-analysis-tab): it provides an insight of how the SLA may evolve by changing the SLA threshold.

### Package Filter:

This filter will control all the data you are going to analyze via this app. Click on the package you would like to explore by clicking on the name of the item, or select multiple package(s) by holding "ctrl" key on your keyboard and select. In addition, you could use "ctrl" + "A" to select all packages.

<img src="/Entitlement%20Analysis%20Tool/images/package_filter.jpg" width="210" height="236"/>

### Status Analysis tab

First of all, the "Status Filter" will further select the action status data you would like to research. There are 6 possible options:

* A: Approved
* E: Expired
* MA: Manual Approved (contributor/admin entitle that user via ENTA function directly instead of approving/rejecting his/her request)
* PB: Pending Broker Action
* R: Rejected
* W: Withdraw (the requestor doesn't want to request and withdraw the request
    

The first graph will display what percentage of each action status in each month per the status selected. When hover mouse on the bar, it will display detail of that specific data set.

![Status1](/Entitlement%20Analysis%20Tool/images/status1.PNG)

In addition, you could click on the bar to select one or a few months (highlighted in the graph) to further analyze coming after.

On the bottom of above screenshot, it shows what percentage of requests is "Expired" for the time period imported (bar month selector doesn't impact it).

![Status2](/Entitlement%20Analysis%20Tool/images/status2.jpg) 

This bar chart shows you how the distribution of action days for the status and mont(s) you selected to analyze (also package you select).

For example, you may select "A" from status and "2020-08" from the first graph, then you will see how many requests are approved on day 1, how many on day 2, ... day 30 for this broker/admin.

The two vertical lines show how many days on average (time weighted) this contributor/admin act on individual request or request from one customer.

The last table provides detail information for all requests based on the filters you applied above. 


### Requests Details tab

This tab shows you how many requests are coming in each month for this contributor/admin.

User entitlement request is calculated as count of each individual request each month. Customer entitlement request is calculated as count of request from one customer (only count one each day when they are multiple individual requests from one specific customer) each month.

![request_details](/Entitlement%20Analysis%20Tool/images/request_details.jpg)

The bar chart of customer entitlement request is clickable to select month. And you will see the filtered detailed information for those requests in the below table. 


### SLA Analysis tab

This chart will give you some idea of how this contributor/admin could possibly meet our SLA given a specific SLA threshold. You may scroll the bar to change the threshold.

![sla](/Entitlement%20Analysis%20Tool/images/sla.PNG)


[Back to top](#entitlement-analysis-tool)


## Source code

For those who are interested in the code. I have uploaded the codes for the major functionalities in the ["code"](https://github.com/angang0123/my_project/tree/main/Entitlement%20Analysis%20Tool/code) folder. Feel free to check.

[Back to top](#entitlement-analysis-tool)



>Created by West Wang
