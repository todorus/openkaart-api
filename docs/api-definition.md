**This is a draft version and it is subject to change**

# Overview

## Structure
The API follows a tree like structure, which is mirrored in the url. The final part of the url denotes what type of object will be returned. Its former parts are used as a filter, instructing the API to what other object the results must be related.

For example, all the Organizations that are active within a Region can be found at the endpoint:
```
GET /regions/1234/organizations
```

The final part of the url "/organizations" tells the API that we are interested in Organization objects. The former part "/regions/1234" tells the API that the Organizations that are returned, must be related to the Region with uuid "1234".

The total tree is as follows:
* Users
* Regions
  * Organizations
    * Locations
    * Services
  * Services
    * Organizations
* Organizations
  * Locations
  * Services
  * Regions
* Services
  * Regions
  * Organizations

Do note that this does not reflect the structure of the data, but rather the ways in which it can be queried. Some endpoints may also offer additional filters, like querying by part of the name. Be sure to check the endpoints definition before assuming anything.

# Endpoint definitions

## Users
```
{
  username: string
}
```

* username: The username that the user can be logged into. Must be unique.

### POST /users/login
_Allows a client to login, using a username passward combination. The api will
respond with a JWT when authentication is succesful._

_If the username/password is incorrect then the api will return a 401 status and
an empty body_

**request**
```
{
  username: string,
  password: string (12 bcrypt cycles, base64 encoded)
}
```
**response**
```
JWT: string
{
  username: string
}
```


## Regions
```
{
  uuid, string,
  code: integer,
  name: string,
  type, string,
  geometry: geojson
}
```
* uuid: unique identifier
* code: A code that is unique for that type. For example, a municipality code, or postal code.
* name: The name of the Region
* type: The region type
  * Zip
  * PostalArea
  * Place
  * Municipality
  * Province
  * Care
* geometry: A geojson object describing the area(s) the Region covers. No properties
are set, just the geometry is supplied

### GET /regions
_List all the regions which satisfy the filter conditions. If no filter options
are supplied, all the Regions are returned._

**request**

urlparameters
* q: the start of a Region name, case insensitive
* page: what page to start at (default=1)
* limit: the number of Regions per page (default=10)

**response**
```
{
  data: [
    {
      uuid, string,
      code: integer,
      name: string,
      type, string,
      geometry: geojson
    }
  ],
  pages: {
    current: integer,
    total: integer
  }
}
```

### GET /regions/:uuid
_Shows the Region for that uuid, or returns a 404 when no such Region exists._

**response**
```
{
  uuid, string,
  code: integer,
  name: string,
  type, string,
  geometry: geojson
}
```

### POST /regions
_Creates a new region, consisting out of multiple already defined regions._

**request**

```
Authorization: Bearer <JWT>
{
  name: string,
  type, string (Place, Care),
  children: [
    <uuid> string
  ]

}
```

**response**
```
{
  uuid, string,
  code: integer,
  name: string,
  type, string,
  geometry: geojson
}
```

### PUT /regions/:uuid
_Updates an existing Region. All fields are optional._

**request**

```
Authorization: Bearer <JWT>
{
  name: string,
  type, string (Place, Care),
  children: [
    <uuid> string
  ]

}
```

**response**
```
{
  uuid, string,
  code: integer,
  name: string,
  type, string,
  geometry: geojson
}
```

### DELETE /regions/:uuid
_Removes an existing Region and any connections._

**request**

```
Authorization: Bearer <JWT>
```

## Organizations
```
{
  uuid, string,
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
  locations: [
    {
      uuid: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      },
      coordinates: {
        lng: float,
        lat: float
      }
    }
  ]
}
```
* uuid: unique identifier
* name: the name of the organization
* contact_data: an object containing the general point of contact for the
organization. Regional Locations can have their own contact data.
* locations: the regional Locations of an Organization. This property is only returned by a few endpoints.

### GET /organizations
_List all the Organizations which satisfy the filter conditions. If no filter options
are supplied, all the Organizations are returned._

**request**

urlparameters
* q: the start of an Organization name, case insensitive
* page: what page to start at (default=1)
* limit: the number of Organizations per page (default=10)

**response**
```
{
  data: [
    {
      uuid, string,
      name: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      }
    }
  ],
  pages: {
    current: integer,
    total: integer
  }
}
```

### GET /organizations/:uuid
_Shows the Organization for that uuid, or returns a 404 when no such Organization exists._

**response**
```
{
  uuid, string,
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
  locations: [
    {
      uuid: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      },
      coordinates: {
        lng: float,
        lat: float
      }
    }
  ]
}
```

### GET /regions/:uuid/services/organizations
_List all the organizations which offer the requested Service in that Region._

**request**

urlparameters
* kind: the kind of service
* ground: the grounds of the service request
* page: what page to start at (default=1)
* limit: the number of Organizations per page (default=10)

**response**
```
{
  data: [
    {
      uuid, string,
      name: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      }
      locations: [
        {
          uuid: string,
          contact_data: {
            phone: string,
            email: string,
            address: string
          },
          coordinates: {
            lng: float,
            lat: float
          }
        }
      ]
    }
  ],
  pages: {
    current: integer,
    total: integer
  }
}
```

### POST /organizations
_Creates a new Organization. Only the name is required_

_When defining an Office as well, each Office definition needs at least one of
its contact_data properties set_

**request**

```
Authorization: Bearer <JWT>
{
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
  locations: [
    {
      uuid: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      },
      coordinates: {
        lng: float,
        lat: float
      }
    }
  ]
}
```

**response**
```
{
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
  locations: [
    {
      uuid: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      },
      coordinates: {
        lng: float,
        lat: float
      }
    }
  ]
}
```

### PUT /organizations/:uuid
_Updates an existing Organization. All fields are optional._

_To remove a contact datapoint, set it to null or an empty string._

**request**

```
Authorization: Bearer <JWT>
{
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
}
```

**response**
```
{
  name: string,
  contact_data: {
    phone: string,
    email: string,
    address: string
  }
  locations: [
    {
      uuid: string,
      contact_data: {
        phone: string,
        email: string,
        address: string
      },
      coordinates: {
        lng: float,
        lat: float
      }
    }
  ]
}
```

### DELETE /organizations/:uuid
_Removes an existing Organization, its Locations, and any connections._

**request**

```
Authorization: Bearer <JWT>
```
