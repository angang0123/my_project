# User Creation for Enterprise Console

## Create new login

The first step is to create logins for the client’s engineers for them to access the Enterprise Console.

If clients already have an existing Bloomberg login, that login can be enabled to view the console. Refer to next section for more details.

In most instances, engineers don’t already have access to Bloomberg, and therefore need new logins to be created.

In order to create a login, the following information need to collect from the clients:
  * First Name
  * Last Name
  * Email
  * Phone Number
  
Once you have compiled this information, you will need to run {NTLM<GO>} and hit the launch EC-LM red button on the top (highlighted in yellow below in the screenshot).
  
![NTLM](/Entitlement%20API/images/NTLM.png)

This will open up a browser and you will be prompted to login via your terminal login. Once you are logged in you could either create an individual account or create multiple ones in bulk:

####  1. Create single login

Select the 'create user' tab, input information (first name, last name, Email, phone number, customer number, source), and click on "CREATE" button. And click "YES" to submit the request to CIS team.

![Create User](/Entitlement%20API/images/Create%20New%20User.PNG)

#### 2. Create multiple logins

Select "Bulk Operations File Upload" tab, 

![Bulk Creation](/Entitlement%20API/images/Mass%20upload.PNG)

download the template if you don't have it (by clicking on "DOWNLOAD FILE TEMPLATE").

![Bulk Template](/Entitlement%20API/images/Mass%20upload%20template.PNG)

Fill the template (*what to fill?*), click "CHOOSE FILE" and select the template you finished, click "UPLOAD FILE" to submit.


## Confirm Users

After the users are created (*any notice?*), got o "Confirm Users" tab, submit the emails or UUIDs (separated by newline or comma if more than one user).

![User Confirm](/Entitlement%20API/images/User%20Confirm.PNG)


## Invite Users

After user creation is confirmed, you will need to invite the users, by entering either UUID or email (separated by newline or comma if more than one user). This will send an email to the corresponding users that will prompt them to create a login in the Bloomberg Enterprise console system.


## Permission Users

After the logins have been created, they will need to be permissioned to the Rest API applications. 
