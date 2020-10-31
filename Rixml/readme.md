# A brief introduction of Rixml

This tutorial will walk you through the basic concepts of Rixml and how Rixml works. Useful references are also provided for further learning. Some information is hidden due to compliance concern.

**Contents (click to quickly move to the section):**

* [What is Rixml](#what-is-rixml)
* [How our Rixml system works](#how-our-rixml-system-works)
* [What is in Rixml](#what-is-in-rixml)
* [Some more to know](#some-more-to-know)


## What is Rixml

1. Rixml stands for **R**esearch **I**nformation e**X**change **M**arkup **L**anguage. It is a subset of markup language. (What is [Markup Language](https://en.wikipedia.org/wiki/Markup_language)?). It is usually with a file extension ".xml".

2. It was created due to the increase demand of research distribution, both buy-side and sell-side firms want to organize it in a more efficient way.

3. It is an industrial standard now. More information is available on [https://www.rixml.org/](https://www.rixml.org/)


[Back to top](#a-brief-introduction-of-rixml)


## How xx Rixml system works

**I will use a daily life example to help you understand.**

Think about how you send an object to a friend in another country, what you need to do:

1. pack the object into a parcel and fill required information on the delivery sheet.

<img src="/Rixml/images/sheet.png" width="500" height="300" />

2. submit your parcel to the delivery company.

<img src="/Rixml/images/delivering.jpg" width="500" height="300" />

3. parcel delivered to your friend.

<img src="/Rixml/images/delivered.jpg" width="500" height="300" />


Now you could think the Rixml contribution process as deliver the object (like above).

* The object to deliver is the research report;
* The delivery sheet is the Rixml (.xml) file;
* The delivery company is our SFTP server;
* The friend is xxx terminal.

Here are the brief steps for Rixml contribution:
1. get the report file ready and create the according Rixml file.

<img src="/Rixml/images/rixml-hide.jpg" width="500" height="300" />

2. Connect to research sftp host/server, submit the report file and Rixml file.

<img src="/Rixml/images/sftp.png" width="500" height="300" />

3. Rixml system parses the file and publish the report to xxx terminal.

<img src="/Rixml/images/bbg.png" width="500" height="300" />

[Back to top](#a-brief-introduction-of-rixml)


## What is in Rixml

Rixml (.xml) file in xxx system is also called "control file", because it controls how our system publishes the report (to which channel) and what is about this report (for searching purpose).

Here's a Rixml sample file in a folded view:

![Rixml Tree](/Rixml/images/rixml_tree.PNG)

Most of the information is included in the "Product" node. And it has four children node:
- StatusInfo
- Source
- Content
- Context

This is a fixed structure suggested by Rixml organization. (more details are available at [Rixml Research Standard Data Dictionary v2.5](https://www.rixml.org/images/docs/RIXML-DataDictionary-2_5.pdf)

Whoever adopts Rixml must put the corresponding information in the right section. Here are some brief facts about what are included in each section:

* **StatusInfo**: contribution action (publish or withdraw report);
* **Source**: broker information (who is sending this file), author information (who is writing this report);
* **Content**: headline of the report (displayed on terminal), summary (displayed on terminal), report file name (for parser to match the upload);
* **Context**: ticker information (symbol, target price, currency, ratings), research type (fundamental, technical, etc), asset class information, country information, sector information, etc...

Here's a sample Rixml file structure in a tree graph overview:

![Rixml Tree2](/Rixml/images/rixml_tree2.PNG)

You may check the ["Sample"](/Rixml/Samples) folder to find more sample rixml files in this repository. Also a tool is provided for you to quickly generate a rixml file that is acceptable by our rixml system (with all the important fields available), feel free to have a try.
(information hiden)

[Back to top](#a-brief-introduction-of-rixml)


## Some more to know 

- **Why is Rixml recommended to broker?**
1. It is a widely adopted contribution standard. It has been implemented among all buldge brackets brokers (Goldman Sachs, Morgan Stanley, JP Morgan, Macquarie, Nomura, etc) and many other domestic brokers.
2. It gives brokers more flexibility about "controlling" their reports, e.g. who could access that specific report, which category a report belongs, what tags it has, etc.
3. It requires brokers to automate their publication action (minimize human error), and data we receive could be automatically processed as well.
4. It is secure (double authorization check), and it is fast (SFTP protocal).

(information hiden)


[Back to top](#a-brief-introduction-of-rixml)



>Created by West Wang
