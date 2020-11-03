# Research Entitlement API Implementation (Internal)

This tutorial is for research contribution CAMs to get to know entitlement API, and help their conversation with contributors who may be interested in adopting entitlement API. I will try to explain all concepts and list detailed instructions in plain words. To keep this tutorial as simple and clean as possible, external links will be used. Please use navigators to switch among sections/pages.

Suggeted steps:
* [Understand and pitch entitlement API](#understand-and-pitch-entitlement-api)
* [Communicate and discuss with contributors](#communicate-and-discuss-with-contributors)
* [Help contributor access enterprise console](#help-contributor-access-enterprise-console)
* [Set up connection and develope entitlement API](#set-up-connection-and-develope-entitlement-api)
* [Test API and go on "live"](#test-api-and-go-on-live)



## Understand and pitch entitlement API

Why should contributors use entitlement API?

(information hidden)

[Back to top](#research-entitlement-api-implementation-internal)


## Communicate and discuss with contributors

(information hidden)

### Why do we need to do this

(information hidden)

### What need to be discussed

(information hidden)
   
   It's good to ask contributor to fill the decision tree below (click it to see a bigger picture):

  ![Ticket API Workflow](/Entitlement%20API/images/api_workflow_ticket.png)



[Back to top](#research-entitlement-api-implementation-internal)


## Help contributor access enterprise console

(information hidden)



## Set up connection and develop entitlement API

This step is more for client to do on their end, if contributor is knowledgable enough, there is little for CAMs to get involved and we could skip this step. But still, a simple guidance is provided below:

Contributor needs to do the following:
* Set up connection to our API system;
* Develope entitlement API based on their entitlement workflow (sample code is provided).


### Set up connection (by contributor)

(information hidden)

-------------------------------------------------------------------------------------------------------------------


### Develop Entitlement API

**VERY IMPORTANT!!** As mentioned earlier, this process will determine how much we could improve for their entitlement workflow and our entitlement SLA!

Contributor could check the API documentation from last step for technical details. I will briefly introduce what contributor needs to do to develope entitlement API: (if you are not interested in the technical details, you may skip the following part and go to the next section directly by clicking [here](#set-up-test-package-and-test-api).

**Contributor will send a request to our entitlement system and receive a response.** And this communication is done via entitlement API (like a formatted letter).

So they need to write the request in the required format, and interpret the response in case any addition action is required from them.

The request is in fact HTTP request. And typical request looks like this:

<img src="/Entitlement%20API/images/whole_url.PNG" width="600" height="350" />

It composes of three parts (as a string):
  * Host (marked with red rectangle): it indicates whether this request is sent to BETA environment or PROD environment;
  * Path (marked with blue rectangle): what type of request it is (more details are in next section);
  * JWT (marked with green rectangle): token for this request.

#### Host

Host domain:

  * UAT: https://beta.api.bloomberg.com
  * PROD: https://api.bloomberg.com

#### Path

**This is the MOST tricky part among the three**, if we help contributor understand how this is generated, it will greatly reduce the time they migrate to entitlement API. And this may be the part that troubleshooting is needed. If CAMs learn how it works and explain to contributor directly, it will take off much pressure from engineer team.

There are two types of requests in general, and their operations are listed below:

(information hidden)
 

Here's a quick reference for different examples of "path" generation that I compiled for you. You may share it to contributor as well. [Examples of path generation](https://github.com/angang0123/my_project/Entitlement/blob/master/Entitlement%20API/path.md)

Here are something to notice:
(information hidden)


#### JWT

**What is a JWT?** JWT stands for JSON web token. This is a key (similar to SSH-Key in SFTP) that contributor needs to generate on their end to send us authorized API request.

This part looks complicated, but in fact it is not. It contains a lot of information which we have already coverred in previous sections. What we need to do is telling contributor to fill all those fields accordingly:

It has three portions:
  * **Credentials**
  * **JWT Header**
  * **JWT Payload**
  
You may refer to the API documentation for details, it already contains all necessary inforation. Just one tip from me, the "path" field in JWT Payload is the same as that from "Path" section (but it does **NOT** include parameters!).

### *Code reference (Python version)

You could find the python code to achieve entitlement API in the [code folder](https://github.com/angang0123/my_project/Entitlement/tree/master/Entitlement%20API/code). 
(information hidden)

## Test API and go on "live"

(information hidden)


[Back to top](#research-entitlement-api-implementation-internal)


> Created by West
