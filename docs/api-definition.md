# API definition

## Users

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

* uuid: unique identifier
* code*: A code that is unique for that type. For example, a municipality code, or postal code.
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
