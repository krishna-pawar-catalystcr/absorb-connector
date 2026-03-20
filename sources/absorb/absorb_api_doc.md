# Absorb LMS API Documentation

## Authorization

The Absorb Integration API supports username/password authentication as the primary method. This method authenticates using credentials to receive an API token for subsequent requests.

### Username/Password Authentication (Preferred)

**Endpoint:** `POST /authenticate`

**Base URLs by Region:**
- US: `https://rest.myabsorb.com/authenticate`
- CA: `https://rest.myabsorb.ca/authenticate`
- EU: `https://rest.myabsorb.eu/authenticate`
- AU: `https://rest.myabsorb.com.au/authenticate`

**Header Parameters:**
- `x-api-key`: Your private API key (required for authentication request)
- `x-api-version`: API version (optional, defaults to latest; recommended: `2`)

**Request Body:**
```json
{
  "username": "your-username",
  "password": "your-password",
  "privateKey": "your-private-key-guid"
}
```

**Response:**
Returns a string token that must be used in subsequent API requests via the `Authorization` header as a Bearer token.

**Example Authentication Request:**
```http
POST /authenticate HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Content-Type: application/json

{
  "username": "admin",
  "password": "your-password",
  "privateKey": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Example Response:**
```json
"abc123def456ghi789"
```

**Example Subsequent Request Using Token:**
```http
GET /users HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer abc123def456ghi789
```

### Private API Key (Alternative)

The Absorb Integration API can also authenticate using a private key directly in the `x-api-key` header for each request. The private key can be obtained in the Absorb portal settings.

**Header Parameters:**
- `x-api-key`: The private API key (required)
- `x-api-version`: API version (optional, defaults to latest; recommended: `2`)

**Example Request:**
```http
GET /users HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
```

### OAuth 2.0 (Alternative)

Absorb also supports OAuth 2.0 authentication. See [OAuth 2.0 Documentation](https://docs.myabsorb.com/integration-api/v2/docs/authentication/oauth) for details.

---

## Object List

The following objects are accessible via the Absorb Integration API v2:

| Object | Endpoint | Description |
|--------|----------|-------------|
| Users | `/users` | Learner, instructor, admin, and manager user records |
| Departments | `/departments` | Organizational departments |
| Courses | `/courses` | Online courses, instructor-led courses, course bundles, curricula |
| Enrollments | `/users/{userId}/enrollments`, `/courses/{courseId}/enrollments` | User course enrollments |
| Groups | `/groups` | User groups |
| Roles | `/roles` | User roles |
| Countries | `/countries` | Country list |
| Provinces | `/provinces` | Province/state list (requires countryId) |

The object list is static - these are the predefined endpoints available in the Absorb Integration API.

---

## Object Schema

### Users

**List Endpoint:** `GET /users`

**Get Single Endpoint:** `GET /users/{userId}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Unique user identifier |
| departmentId | string (guid) | User's department ID |
| firstName | string | First name |
| middleName | string | Middle name |
| lastName | string | Last name |
| username | string | Unique username |
| emailAddress | string | Contact email address |
| externalId | string | External ID for integrations |
| ccEmailAddresses | array[string] | CC email addresses (max 5) |
| languageId | integer | Language ID |
| gender | integer | Gender (0=None, 1=Male, 2=Female) |
| address | string | Mailing address |
| address2 | string | Mailing address part two |
| city | string | City |
| provinceId | string (guid) | Province ID |
| countryId | string (guid) | Country ID |
| postalCode | string | Postal/zip code |
| phone | string | Phone number |
| employeeNumber | string | Employee number |
| location | string | Location |
| jobTitle | string | Job title |
| referenceNumber | string | Reference number |
| dateHired | datetime | Date hired |
| dateTerminated | datetime | Date terminated |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |
| lastLoginDate | datetime | Last login date |
| notes | string | Notes |
| customFields | object | Custom fields (decimal1-5, string1-30, datetime1-5, bool1-5) |
| roleIds | array[string] | Role IDs |
| activeStatus | integer | Active status (0=Active, 1=Inactive) |
| isLearner | boolean | Is learner |
| isAdmin | boolean | Is admin |
| isInstructor | boolean | Is instructor |
| isManager | boolean | Is manager |
| supervisorId | string (guid) | Supervisor ID |
| hasUsername | boolean | Has username |

**Example Request:**
```http
GET /users?_limit=100&_offset=0 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

**Example Response:**
```json
{
  "totalItems": 150,
  "returnedItems": 100,
  "limit": 100,
  "offset": 0,
  "users": [
    {
      "id": "a14c149a-2ce0-41d4-b532-02189ad3cb22",
      "departmentId": "b25c149a-2ce0-41d4-b532-02189ad3cb23",
      "firstName": "John",
      "lastName": "Doe",
      "username": "jdoe",
      "emailAddress": "john.doe@example.com",
      "isLearner": true,
      "isAdmin": false,
      "activeStatus": 0,
      "dateAdded": "2023-01-15T10:30:00Z"
    }
  ]
}
```

---

### Departments

**List Endpoint:** `GET /departments`

**Get Single Endpoint:** `GET /departments/{id}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Department identifier |
| name | string | Department name |
| useDepartmentContactDetails | boolean | Use department contact details |
| companyName | string | Company name |
| phoneNumber | string | Phone number |
| emailAddress | string | Email address |
| externalId | string | External ID |
| parentId | string (guid) | Parent department ID |
| currencyId | string (guid) | Currency ID |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |

**Example Request:**
```http
GET /departments?_limit=50 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Courses

**List Endpoint:** `GET /courses`

**Get Single Endpoint:** `GET /courses/{courseId}`

**List User's Available Courses:** `GET /users/{userId}/courses`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Course identifier |
| courseType | string | Course type (OnlineCourse, InstructorLedCourse, CourseBundle, Curriculum) |
| name | string | Course name |
| description | string | Course description (supports HTML) |
| notes | string | Notes |
| externalId | string | External ID |
| accessDate | datetime | Access date |
| expireType | integer | Expiry type (0=None, 1=Date, 2=Duration) |
| expireDuration | object | Duration until expiry (years, months, days, hours) |
| expiryDate | datetime | Expiry date |
| activeStatus | integer | Status (0=Active, 1=Inactive) |
| tagIds | array[string] | Tag IDs |
| resourceIds | array[string] | Resource IDs |
| editorIds | array[string] | Editor IDs |
| prices | array[object] | Prices (id, departmentId, currency, amount) |
| competencyDefinitionIds | array[string] | Competency definition IDs |
| prerequisiteCourseIds | array[string] | Prerequisite course IDs |
| postEnrollmentCourseIds | array[string] | Post-enrollment course IDs |
| allowCourseEvaluation | boolean | Allows course evaluation |
| categoryId | string (guid) | Category ID |
| certificateUrl | string | Certificate URL |
| audience | string | Target audience |
| goals | string | Course goals |
| vendor | string | Vendor |
| companyCost | decimal | Company cost |
| learnerCost | decimal | Learner cost |
| companyTime | decimal | Company time |
| learnerTime | decimal | Learner time |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |

**Example Request:**
```http
GET /courses?_limit=100&_offset=0 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Enrollments

**List User Enrollments:** `GET /users/{userId}/enrollments`

**List Course Enrollments:** `GET /courses/{courseId}/enrollments`

**Get User Enrollment for Course:** `GET /users/{userId}/enrollments/{courseId}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Enrollment identifier |
| courseId | string (guid) | Course identifier |
| courseName | string | Course name |
| userId | string (guid) | User identifier |
| progress | decimal | Percentage completed |
| score | decimal | Score percentage |
| status | integer | Status (0=NotStarted, 1=InProgress, 2=PendingApproval, 3=Complete, 4=NotComplete, 5=Failed, 6=Declined, 7=PendingEvaluationRequired, 8=OnWaitlist, 9=Absent, 10=NotApplicable, 11=PendingProctor, 12=ReadyForReview) |
| dateCompleted | datetime | Completion date |
| dateExpires | datetime | Expiry date |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |
| dateStarted | datetime | Start date |
| fullName | string | Learner full name |
| courseVersionId | string (guid) | Course version ID |
| acceptedTermsAndConditions | boolean | Terms accepted |
| timeSpentTicks | integer | Time spent (ticks) |
| timeSpent | string | Time spent (duration) |
| enrollmentKeyId | string (guid) | Enrollment key ID |
| certificateId | string (guid) | Certificate ID |
| credits | decimal | Credits |
| isActive | boolean | Is active enrollment |
| dateDue | datetime | Due date |
| accessDate | datetime | Access date |
| jobTitle | string | Job title |
| courseCollectionId | string (guid) | Course bundle/curriculum ID |
| avatar | string | Avatar path |

**Example Request:**
```http
GET /users/a14c149a-2ce0-41d4-b532-02189ad3cb22/enrollments?_limit=100 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Groups

**List Endpoint:** `GET /groups`

**Get Single Endpoint:** `GET /groups/{id}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Group identifier |
| name | string | Group name |
| isAutomatic | boolean | Is automatically managed |
| userIds | array[string] | User IDs (max 50,000; default ID "00000000-0000-0000-0000-000000000000" indicates more users) |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |

**Example Request:**
```http
GET /groups?_limit=50 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Roles

**List Endpoint:** `GET /roles`

**Get Single Endpoint:** `GET /roles/{id}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Role ID |
| name | string | Role name |
| description | string | Role description |
| dateEdited | datetime | Last edited date |
| dateAdded | datetime | Date added |

**Example Request:**
```http
GET /roles HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Countries

**List Endpoint:** `GET /countries`

**Get Single Endpoint:** `GET /countries/{id}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Country ID |
| countryCode | string | Country code |
| name | string | Country name |

**Example Request:**
```http
GET /countries HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

### Provinces

**List Endpoint:** `GET /provinces?countryId={countryId}`

**Get Single Endpoint:** `GET /provinces/{id}`

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (guid) | Province ID |
| name | string | Province name |

**Example Request:**
```http
GET /provinces?countryId=a14c149a-2ce0-41d4-b532-02189ad3cb22 HTTP/1.1
Host: rest.myabsorb.com
x-api-key: your-private-api-key
x-api-version: 2
Authorization: Bearer your-auth-token
```

---

## Get Object Primary Keys

| Object | Primary Key | Field Name |
|--------|-------------|------------|
| Users | Yes | `id` |
| Departments | Yes | `id` |
| Courses | Yes | `id` |
| Enrollments | Yes | `id` |
| Groups | Yes | `id` |
| Roles | Yes | `id` |
| Countries | Yes | `id` |
| Provinces | Yes | `id` |

All objects use `id` (string, GUID format) as the primary key. There is no API to retrieve primary key metadata - it is static based on the API specification.

---

## Object's Ingestion Type

| Object | Ingestion Type | Rationale |
|--------|---------------|-----------|
| Users | `cdc` | Supports `dateEdited` field for incremental sync; changes tracked |
| Departments | `snapshot` | Rarely changes; no reliable change tracking field |
| Courses | `cdc` | Supports `dateEdited` field for incremental sync |
| Enrollments | `cdc` | Supports `dateEdited` and `modifiedSince` filter for incremental sync |
| Groups | `snapshot` | Changes infrequently; no reliable change tracking field |
| Roles | `snapshot` | Static reference data; rarely changes |
| Countries | `snapshot` | Static reference data; rarely changes |
| Provinces | `snapshot` | Static reference data; rarely changes |

**Note on Deletion Handling:**
- The Absorb API does not provide a dedicated endpoint for fetching deleted records.
- For `cdc` objects (Users, Courses, Enrollments), implement a soft-sync approach using `dateEdited` filtering.
- Deleted records can be identified by comparing current state against previous state or by checking `activeStatus` field for Users (0=Active, 1=Inactive).

---

## Read API for Data Retrieval

### Pagination

All list endpoints support pagination via query parameters:

| Parameter | Description | Default | Max |
|-----------|-------------|---------|-----|
| `_offset` | Page offset (0-indexed) | 0 | 65535 |
| `_limit` | Items per page | 20 | 1000 |

**Example:**
```http
GET /users?_offset=0&_limit=100 HTTP/1.1
```

Iterate through pages by incrementing `_offset` until no records are returned.

### Sorting

Use `_sort` query parameter with comma-separated field names. Prefix with `-` for descending order.

**Example:**
```http
GET /users?_sort=-dateAdded,lastName HTTP/1.1
```

### Filtering

Use `_filter` query parameter with OData filter syntax:

**Supported Operations:** `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `and`, `or`, `not`, `()`

**Supported Functions:** `substringof`, `endswith`, `startswith`, `tolower`, `toupper`

**Examples:**
```http
GET /users?_filter=dateEdited%20ge%20datetime%272023-01-01T00:00:00Z%27 HTTP/1.1
GET /users?_filter=startsWith(lastName,'Smith') HTTP/1.1
GET /users?_filter=id%20eq%20guid%27a14c149a-2ce0-41d4-b532-02189ad3cb22%27 HTTP/1.1
```

### Incremental Sync Strategy

For objects supporting incremental sync (`cdc` type):

1. **Cursor Field:** Use `dateEdited` as the cursor field for incremental sync
2. **Sort Order:** Sort by `dateEdited` ascending for consistent incremental reads
3. **Lookback Window:** Implement a lookback of 24-48 hours to handle late-arriving updates
4. **Delete Detection:** TBD - Absorb API does not provide explicit delete tracking; implement soft-sync by comparing against previous state

**Example Incremental Request:**
```http
GET /users?_filter=dateEdited%20ge%20datetime%272024-01-15T00:00:00Z%27&_sort=dateAdded HTTP/1.1
```

**Note:** The `modifiedSince` query parameter is deprecated; use `_filter=dateEdited ge datetime'...'` instead.

### Rate Limits

- **Standard Limit:** 200 requests per second
- **Burst Limit:** 100 additional requests (buffer for short overruns)
- **Response on Limit:** HTTP 429 Too Many Requests

**Recommended Handling:**
- Implement exponential backoff with jitter on 429 responses
- Consider throttling requests at 150-180 requests/second as a safety margin
- Monitor rate limit responses and adjust accordingly

---

## Field Type Mapping

| API Field Type | JSON Type | Description |
|----------------|-----------|-------------|
| string | string | Text fields |
| string (guid) | string | UUID format identifiers |
| integer | integer | Whole numbers |
| decimal | number | Floating point numbers |
| boolean | boolean | True/false |
| datetime | string | ISO 8601 format (e.g., "2024-01-15T10:30:00Z") |
| array[T] | array | Lists of values |
| duration | string | ISO 8601 duration format |

**Special Field Behaviors:**
- `customFields`: Dynamic object containing decimal1-5, string1-30, datetime1-5, bool1-5
- `gender`: Enum (0=None, 1=Male, 2=Female)
- `activeStatus`: Enum (0=Active, 1=Inactive)
- `expireType`: Enum (0=None, 1=Date, 2=Duration)
- `enrollment status`: Enum (0-12 values as listed above)
- `timeSpent`: Represented as both ticks (int64) and duration (string)

---

## Known Quirks

1. **Nested Property Filtering:** Custom fields can be filtered using `[parentProperty]/[property]` syntax (e.g., `_filter=customFields/string1 eq 'test'`)

2. **Nested Property Sorting:** Custom fields can be sorted using the same dot notation (e.g., `_sort=-customFields/decimal1`)

3. **Blank String Limitation:** Due to technical limitations, blank strings ('') and null are not supported in nested property filters

4. **Dynamic Rules Delay:** Assets using dynamic rules may take up to 10 minutes to process user updates

5. **Group UserIds Limit:** Returns max 50,000 userIds; default ID "00000000-0000-0000-0000-000000000000" indicates more users exist

6. **Multi-Session ILC:** Enrollments API does not support multi-session instructor-led courses (ILCs)

7. **Region-Specific Base URLs:** Must choose correct regional endpoint (US, CA, EU, AU) based on Absorb account location

---

## Research Log

| Source Type | URL | Accessed (UTC) | Confidence | What it confirmed |
|-------------|-----|----------------|------------|------------------|
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs | 2025-03-17 | High | Authentication, pagination, filtering, rate limits |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/authentication/ | 2025-03-17 | High | Auth endpoint, request/response format |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/users | 2025-03-17 | High | Users endpoint, schema, filtering |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/departments | 2025-03-17 | High | Departments endpoint, schema |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/courses/ | 2025-03-17 | High | Courses endpoint, schema |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/enrollments/ | 2025-03-17 | High | Enrollments endpoint, schema, status codes |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/groups | 2025-03-17 | High | Groups endpoint, schema |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/roles | 2025-03-17 | High | Roles endpoint, schema |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/countries | 2025-03-17 | High | Countries endpoint, schema |
| Official Docs | https://docs.myabsorb.com/integration-api/v2/docs/provinces | 2025-03-17 | High | Provinces endpoint, schema |

---

## Sources and References

- **Official Absorb Integration API Documentation:** https://docs.myabsorb.com/integration-api/v2/docs
- **Authentication Documentation:** https://docs.myabsorb.com/integration-api/v2/docs/authentication/
- **OAuth 2.0 Documentation:** https://docs.myabsorb.com/integration-api/v2/docs/authentication/oauth
- **Users API:** https://docs.myabsorb.com/integration-api/v2/docs/users
- **Departments API:** https://docs.myabsorb.com/integration-api/v2/docs/departments
- **Courses API:** https://docs.myabsorb.com/integration-api/v2/docs/courses/
- **Enrollments API:** https://docs.myabsorb.com/integration-api/v2/docs/enrollments/
- **Groups API:** https://docs.myabsorb.com/integration-api/v2/docs/groups
- **Roles API:** https://docs.myabsorb.com/integration-api/v2/docs/roles
- **Countries API:** https://docs.myabsorb.com/integration-api/v2/docs/countries
- **Provinces API:** https://docs.myabsorb.com/integration-api/v2/docs/provinces

**Confidence Level:** Official API documentation - highest confidence

All information documented herein is sourced directly from the official Absorb Integration API documentation. No third-party implementations were referenced.
