# Lakeflow Absorb LMS Community Connector

This documentation provides setup instructions and reference information for the Absorb LMS source connector.

## Prerequisites

- An active Absorb LMS account with API access enabled
- A private API key obtained from Absorb portal settings
- An Absorb account with a username and password
- Admin or appropriate permissions to access the Integration API

## Setup

### Required Connection Parameters

To configure the connector, provide the following parameters in your connector options:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `portal_url` | Yes | Absorb portal region. Must be one of: US, CA, EU, AU |
| `private_api_key` | Yes | Private API key from Absorb portal settings |
| `username` | Yes | Absorb account username |
| `password` | Yes | Absorb account password |

**Portal URL Options:**
- US: `https://rest.myabsorb.com`
- CA: `https://rest.myabsorb.ca`
- EU: `https://rest.myabsorb.eu`
- AU: `https://rest.myabsorb.com.au`

### How to Obtain Required Parameters

1. **Private API Key:**
   - Log in to your Absorb admin portal
   - Navigate to **Settings** > **Integrations** > **API Keys** (or similar path)
   - Create a new API key or use an existing one
   - Copy the private API key GUID

2. **Portal URL:**
   - Identify your Absorb portal region (US, CA, EU, or AU) based on your account

3. **Username/Password:**
   - Use your Absorb admin account credentials

### Create a Unity Catalog Connection

A Unity Catalog connection for this connector can be created in two ways via the UI:
1. Follow the Lakeflow Community Connector UI flow from the "Add Data" page
2. Select any existing Lakeflow Community Connector connection for this source or create a new one
3. Include `externalOptionsAllowList` with the value `max_records_per_batch, country_id` to enable table-specific options

The connection can also be created using the standard Unity Catalog API.

## Supported Objects

The connector supports the following objects from Absorb LMS:

| Object | Description | Primary Key | Ingestion Type |
|--------|-------------|-------------|---------------|
| `users` | Learner, instructor, admin, and manager user records | `id` | Incremental (CDC) |
| `departments` | Organizational departments | `id` | Snapshot |
| `courses` | Online courses, instructor-led courses, course bundles, curricula | `id` | Incremental (CDC) |
| `enrollments` | User course enrollments | `id` | Incremental (CDC) |
| `groups` | User groups | `id` | Snapshot |
| `roles` | User roles | `id` | Snapshot |
| `countries` | Country list | `id` | Snapshot |
| `provinces` | Province/state list | `id` | Snapshot |

### Incremental Ingestion

The following objects support incremental (CDC) synchronization using the `dateEdited` field as the cursor:

- **users** - Tracks user profile changes
- **courses** - Tracks course content updates
- **enrollments** - Tracks enrollment and completion status changes

The cursor field (`dateEdited`) is used to track changes between pipeline runs.

### Special Notes

**Enrollments Table:**
- Enrollments are fetched using the user-scoped endpoint `/users/{userId}/enrollments`
- Each enrollment record includes the `userId` field linking to the user
- The cursor tracks user changes for incremental sync

**Provinces Table:**
- If `country_id` is provided, fetches provinces for that country only
- If `country_id` is not provided, automatically fetches all provinces for all countries
- Each province record includes `countryId` and `countryName` fields

**Countries Table:**
- Returns a flat list of all countries

## Table Configurations

### Source & Destination

These are set directly under each `table` object in the pipeline spec:

| Option | Required | Description |
|---|---|---|
| `source_table` | Yes | Table name in the source system |
| `destination_catalog` | No | Target catalog (defaults to pipeline's default) |
| `destination_schema` | No | Target schema (defaults to pipeline's default) |
| `destination_table` | No | Target table name (defaults to `source_table`) |

### Common `table_configuration` options

These are set inside the `table_configuration` map alongside any source-specific options:

| Option | Required | Description |
|---|---|---|
| `scd_type` | No | `SCD_TYPE_1` (default) or `SCD_TYPE_2`. Only applicable to tables with CDC or SNAPSHOT ingestion mode |
| `primary_keys` | No | List of columns to override the connector's default primary keys |
| `sequence_by` | No | Column used to order records for SCD Type 2 change tracking |

### Source-Specific Table Configurations

**For the `provinces` table:**

| Option | Required | Description |
|---|---|---|
| `country_id` | No | The ID of the country to fetch provinces for. If not provided, all provinces for all countries are fetched |

**For incremental tables (users, courses, enrollments):**

| Option | Required | Description |
|---|---|---|
| `max_records_per_batch` | No | Maximum number of records to fetch per batch (default: 200) |

## Data Type Mapping

| Absorb Field Type | Databricks Type |
|-------------------|-----------------|
| String | String |
| Integer | Integer |
| Boolean | Boolean |
| Array | Array |
| Long | Long |
| Decimal | Decimal |

**Note:** Date and datetime fields in Absorb are returned as ISO 8601 formatted strings.

## How to Run

### Step 1: Clone/Copy the Source Connector Code
Follow the Lakeflow Community Connector UI, which will guide you through setting up a pipeline using the selected source connector code.

### Step 2: Configure Your Pipeline
1. Update the `pipeline_spec` in the main pipeline file (e.g., `ingest.py`).

2. Configure your tables:
```python
pipeline_spec = {
    "connection_name": "my_absorb_connection",
    "objects": [
        {
            "table": {
                "source_table": "users",
                "table_configuration": {
                    "scd_type": "SCD_TYPE_2",
                    "sequence_by": "dateEdited"
                }
            }
        },
        {
            "table": {
                "source_table": "courses",
                "table_configuration": {
                    "max_records_per_batch": "500"
                }
            }
        },
        {
            "table": {
                "source_table": "enrollments",
                "table_configuration": {
                    "max_records_per_batch": "500"
                }
            }
        },
        {
            "table": {
                "source_table": "departments"
            }
        },
        {
            "table": {
                "source_table": "countries"
            }
        },
        {
            "table": {
                "source_table": "provinces"
            }
        }
    ]
}
```

3. (Optional) Customize the source connector code if needed for special use cases.

### Step 3: Run and Schedule the Pipeline

#### Best Practices

- **Start Small**: Begin by syncing a subset of tables to test your pipeline
- **Use Incremental Sync**: Reduces API calls and improves performance for tables that support CDC
- **Set Appropriate Schedules**: Balance data freshness requirements with API usage limits
- **Configure Batch Size**: Adjust `max_records_per_batch` based on your API rate limits and data volume
- **Large Datasets**: For tables with thousands of records, incremental sync ensures only changed records are fetched

#### Troubleshooting

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication Failed (400) | Missing or invalid credentials | Verify username, password, and private API key are correct |
| Authentication Failed (403) | Portal disabled or API access not enabled | Contact Absorb admin to enable API access |
| No Data Returned | Incorrect table name | Check source_table matches supported object names exactly |
| Rate Limiting | Too many requests | Reduce `max_records_per_batch` or increase sync interval |

## References

- [Absorb Integration API Documentation](https://docs.myabsorb.com/integration-api/v2/)
- [Lakeflow Community Connectors Overview](https://docs.databricks.com/en/lakeflow/community-connectors.html)
