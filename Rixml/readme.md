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


## How our Rixml system works

**I will use a daily life example to help you understand.**

Think about how you send an object to a friend in another country, what you need to do:

1. pack the object into a parcel and fill required information on the delivery sheet.

<img src="/Images/sheet.png" width="500" height="300" />

2. submit your parcel to the delivery company.

<img src="/Images/delivering.jpg" width="500" height="300" />

3. parcel delivered to your friend.

<img src="/Images/delivered.jpg" width="500" height="300" />


Now you could think the Rixml contribution process as deliver the object (like above).

* The object to deliver is the research report;
* The delivery sheet is the Rixml (.xml) file;
* The delivery company is our SFTP server;
* The friend is Bloomberg terminal.

Here are the brief steps for Rixml contribution:
1. get the report file ready and create the according Rixml file.

<img src="/Images/rixml.PNG" width="500" height="300" />

2. Connect to research sftp host/server, submit the report file and Rixml file.

<img src="/Images/sftp.png" width="500" height="300" />

3. Rixml system parses the file and publish the report to Bloomberg terminal.

<img src="/Images/bbg.png" width="500" height="300" />

[Back to top](#rixml-introduction-internal-only)


## What is in Rixml

Rixml (.xml) file in our system is also called "control file", because it controls how our system publishes the report (to which channel) and what is about this report (for searching purpose).

Here's a Rixml sample file in a folded view:

![Rixml Tree](/Images/rixml_tree.PNG)

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
![Rixml Tree2](/Images/rixml_tree2.PNG)

You may check the "Sample" folder to find more sample rixml files in this repository. Also a tool is provided for you to quickly generate a rixml file that is acceptable by our rixml system (with all the important fields available), feel free to have a try.
For more details about the available fields, please refer to Rixml data dictionary.
Just be careful that **our system doesn't parse all fields provided in data dictionary so far. And there are some known issues for our rixml parser.** If you have any question, please check with related contribution CAMs or engineers.

[Back to top](#rixml-introduction-internal-only)


## Some more to know 

- **Why is Rixml recommended to broker?**
1. It is a widely adopted contribution standard. It has been implemented among all buldge brackets brokers (Goldman Sachs, Morgan Stanley, JP Morgan, Macquarie, Nomura, etc) and many other domestic brokers.
2. It gives brokers more flexibility about "controlling" their reports, e.g. who could access that specific report, which category a report belongs, what tags it has, etc.
3. It requires brokers to automate their publication action (minimize human error), and data we receive could be automatically processed as well.
4. It is secure (double authorization check), and it is fast (SFTP protocal).



- **General workflow to migrate a broker to Rixml contribution:**
1. Check with broker to see if they are willing to migrate to this method (also capability to develop their rixml contribution system);
2. Get in touch with their developer team (or IT team), introduce the rixml framework;
3. When they start to develop their system, contribution CAMs will create a SFTP login for this broker and raise DRQS to add this login to rixml parser (e.g. {DRQS 1084268})
4. Contribution CAMs create a test class/package for the broker, and broker starts to test their rixml contribution;
5. Troubleshoot and coordinate with broker till there's no issue;
6. Turn to PROD.

- **Rixml tag:**

Any report is uploaded via Rixml will be tagged with "RIXML" NI code in our system. You could easily identify it in "Story Maintenance" -> "assigned code" (higlighted in the screenshot below).

<img src="/Images/rixml_tag.PNG" width="800" height="500" />

It also means, you could use "rixml" as keyword to filter reports submitted via rixml in function {BRC} or {NH}, etc.



[Back to top](#rixml-introduction-internal-only)



>Created by West Wang, 2020 Oct
