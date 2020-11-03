# Examples of path generation

**This information is extracted from entitlement API documentation for easier reference:**

Navigator:
* [Path of ticket request](#path-of-ticket-request)
* [Path of package request](#path-of-package-request)


## Path of ticket request:

**1. GET request:**

**Related parameters:**

Name | Description | Data Type
-----|------------|-----------
brokerID | unique identifier of broker | integer
uuids | get associated entitlement status for a list of users, specified by a comma-separated list of uuids. if uuid is unavailable, use e-mail instead. the status of a user will be "entitled", "pending", or "not entitled". | string
emails | get associated entitlement status for a list of users, specified by a comma-separated list of emails. the status of a user will be "entitled", "pending", or "not entitled". | string


* **GET /tickets:**	access tickets related to the entitlements owned by a broker
* Examples:
    * curl -X GET https://api.bloomberg.com/ctrb/v1/tickets?brokerId=1&status=pending,approved&startDate=2017-01-01

* **GET /tickets/{ticketId}:**	access a specific entitlement request ticket
* Examples:
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/tickets/8315?brokerId=1"


**2. PATCH request:**

**Related parameters:**

Name | Description | Data Type
-----|------------|-----------
brokerID | unique identifier of broker | integer
request body | a list of user identification and the entitlement status that user should be be updated to | json


* **PATCH /tickets:**	allows brokers to approve or reject entitlement request tickets in bulk
* Examples:
    * curl --header "Content-Type:application/json" --request PATCH --data '{"updates": [{"ticketId": 8314, "status": "approved"}]}' https://api.bloomberg.com/ctrb/v1/tickets?brokerId=1

* **PATCH /tickets/{ticketId}	:**	allows brokers to accept or reject a specific entitlement request
* Examples:
    * curl --header "Content-Type:application/json" --request PATCH --data '{"status": "approved"}' https://api.bloomberg.com/ctrb/v1/tickets/8315?brokerId=1


## Path of package request:

**1. GET request:**

**Related parameters:**

Name | Description | Data Type
-----|------------|-----------
brokerID | unique identifier of broker | integer
status | a comma-separated list of keywords to filter the response. valid values are "pending", "approved", and "rejected". if omitted, default to "pending" | string[] , x ∈ { pending , approved , rejected }
startDate | to specify a time range. defaults to 30 days prior. formatted YYYY-MM-DD | string
endDate | to specify a time range. defaults to present. formatted YYYY-MM-DD | string

* **GET /packages/{packageId}/users/{userId}:**	get information on a user within a package
* Examples:
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/123/users/123456?brokerId=1"
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/123/users/johndoe@gmail.com?brokerId=1"
    
* **GET /packages/{packageId}/users:**	allows brokers to see users of research packages
* Examples:
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/123/users?brokerId=1"
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/123/users?brokerId=1&uuids=123456&emails=doejohn@corp.com"
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/123/users?brokerId=1&uuids=123456"

* **GET /packages/users:**	get information on entitlement status of all visible packages for specified user/users
* Examples:
    * curl -X GET "https://api.bloomberg.com/ctrb/v1/packages/users?brokerId=1&uuids=123456&emails=doejohn@corp.com"


**2. PATCH request:**

**Related parameters:**

Name | Description | Data Type
-----|------------|-----------
brokerID | unique identifier of broker | integer
request body | a list of user identification and the entitlement status that user should be be updated to | json

* **PATCH /packages/{packageId}/users:**	allows brokers to update the statuses of entitlements in bulk
* Examples:
    * Use e-mail: curl --header "Content-Type:application/json" --request PATCH --data '{"updates": [{"email": "johndoe@gmail.com", "status": "entitled"}]}' "https://api.bloomberg.com/ctrb/v1/packages/123/users?brokerId=1"
    * Use uuid: curl --header "Content-Type:application/json" --request PATCH --data '{"updates": [{"uuid": 123456, "status": "entitled"}]}' "https://api.bloomberg.com/ctrb/v1/packages/123/users?brokerId=1"

* **PATCH /packages/{packageId}/users/{userId}:**	update a user's entitlement status
* Examples:
    * curl --header "Content-Type:application/json" --request PATCH --data '{"status": "entitled"}' https://api.bloomberg.com/ctrb/v1/packages/123/users/123456?brokerId=1
    * curl --header "Content-Type:application/json" --request PATCH --data '{"status": "entitled"}' https://api.bloomberg.com/ctrb/v1/packages/123/users/johndoe@gmail.com?brokerId=1

* **PATCH /packages/users:**	allows brokers to update the statuses of entitlements of multiple packages
* Examples:
    * Use e-mail: curl --header "Content-Type:application/json" --request PATCH --data '{"updates": [{"packageIds": [2233], "email": "johndoe@gmail.com", "status": "entitled"}]}' "https://api.bloomberg.com/ctrb/v1/packages/users?brokerId=1"
    * Use uuid: curl --header "Content-Type:application/json" --request PATCH --data '{"updates": [{"packageIds": [77668, 5678], "uuid": 123456, "status": "entitled"}]}' "https://api.bloomberg.com/ctrb/v1/packages/users?brokerId=1"
