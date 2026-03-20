"""Static schema definitions for Absorb LMS connector tables.

This module contains all Spark StructType schema definitions and table metadata
for the Absorb Lakeflow connector. These are derived from the Absorb Integration API v2
documentation.
"""

from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    StringType,
    BooleanType,
    ArrayType,
    DecimalType,
    IntegerType,
)


# =============================================================================
# Users Table
# =============================================================================

USERS_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("departmentId", StringType(), True),
        StructField("firstName", StringType(), True),
        StructField("middleName", StringType(), True),
        StructField("lastName", StringType(), True),
        StructField("username", StringType(), True),
        StructField("emailAddress", StringType(), True),
        StructField("externalId", StringType(), True),
        StructField("ccEmailAddresses", ArrayType(StringType(), True), True),
        StructField("languageId", IntegerType(), True),
        StructField("gender", IntegerType(), True),
        StructField("address", StringType(), True),
        StructField("address2", StringType(), True),
        StructField("city", StringType(), True),
        StructField("provinceId", StringType(), True),
        StructField("countryId", StringType(), True),
        StructField("postalCode", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("employeeNumber", StringType(), True),
        StructField("location", StringType(), True),
        StructField("jobTitle", StringType(), True),
        StructField("referenceNumber", StringType(), True),
        StructField("dateHired", StringType(), True),
        StructField("dateTerminated", StringType(), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
        StructField("lastLoginDate", StringType(), True),
        StructField("notes", StringType(), True),
        StructField("customFields", StringType(), True),
        StructField("roleIds", ArrayType(StringType(), True), True),
        StructField("activeStatus", IntegerType(), True),
        StructField("isLearner", BooleanType(), True),
        StructField("isAdmin", BooleanType(), True),
        StructField("isInstructor", BooleanType(), True),
        StructField("isManager", BooleanType(), True),
        StructField("supervisorId", StringType(), True),
        StructField("hasUsername", BooleanType(), True),
    ]
)

USERS_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": "dateEdited",
    "ingestion_type": "cdc",
}


# =============================================================================
# Departments Table
# =============================================================================

DEPARTMENTS_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("useDepartmentContactDetails", BooleanType(), True),
        StructField("companyName", StringType(), True),
        StructField("phoneNumber", StringType(), True),
        StructField("emailAddress", StringType(), True),
        StructField("externalId", StringType(), True),
        StructField("parentId", StringType(), True),
        StructField("currencyId", StringType(), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
    ]
)

DEPARTMENTS_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": None,
    "ingestion_type": "snapshot",
}


# =============================================================================
# Courses Table
# =============================================================================

PRICE_STRUCT = StructType(
    [
        StructField("id", StringType(), True),
        StructField("departmentId", StringType(), True),
        StructField("currency", StringType(), True),
        StructField("amount", DecimalType(10, 2), True),
    ]
)

EXPIRE_DURATION_STRUCT = StructType(
    [
        StructField("years", IntegerType(), True),
        StructField("months", IntegerType(), True),
        StructField("days", IntegerType(), True),
        StructField("hours", IntegerType(), True),
    ]
)

COURSES_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("courseType", StringType(), True),
        StructField("name", StringType(), True),
        StructField("description", StringType(), True),
        StructField("notes", StringType(), True),
        StructField("externalId", StringType(), True),
        StructField("accessDate", StringType(), True),
        StructField("expireType", IntegerType(), True),
        StructField("expireDuration", StringType(), True),
        StructField("expiryDate", StringType(), True),
        StructField("activeStatus", IntegerType(), True),
        StructField("tagIds", ArrayType(StringType(), True), True),
        StructField("resourceIds", ArrayType(StringType(), True), True),
        StructField("editorIds", ArrayType(StringType(), True), True),
        StructField("prices", StringType(), True),
        StructField("competencyDefinitionIds", ArrayType(StringType(), True), True),
        StructField("prerequisiteCourseIds", ArrayType(StringType(), True), True),
        StructField("postEnrollmentCourseIds", ArrayType(StringType(), True), True),
        StructField("allowCourseEvaluation", BooleanType(), True),
        StructField("categoryId", StringType(), True),
        StructField("certificateUrl", StringType(), True),
        StructField("audience", StringType(), True),
        StructField("goals", StringType(), True),
        StructField("vendor", StringType(), True),
        StructField("companyCost", DecimalType(10, 2), True),
        StructField("learnerCost", DecimalType(10, 2), True),
        StructField("companyTime", DecimalType(10, 2), True),
        StructField("learnerTime", DecimalType(10, 2), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
    ]
)

COURSES_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": "dateEdited",
    "ingestion_type": "cdc",
}


# =============================================================================
# Enrollments Table
# =============================================================================

ENROLLMENTS_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("courseId", StringType(), True),
        StructField("courseName", StringType(), True),
        StructField("userId", StringType(), True),
        StructField("progress", DecimalType(5, 2), True),
        StructField("score", DecimalType(5, 2), True),
        StructField("status", IntegerType(), True),
        StructField("dateCompleted", StringType(), True),
        StructField("dateExpires", StringType(), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
        StructField("dateStarted", StringType(), True),
        StructField("fullName", StringType(), True),
        StructField("courseVersionId", StringType(), True),
        StructField("acceptedTermsAndConditions", BooleanType(), True),
        StructField("timeSpentTicks", LongType(), True),
        StructField("timeSpent", StringType(), True),
        StructField("enrollmentKeyId", StringType(), True),
        StructField("certificateId", StringType(), True),
        StructField("credits", DecimalType(10, 2), True),
        StructField("isActive", BooleanType(), True),
        StructField("dateDue", StringType(), True),
        StructField("accessDate", StringType(), True),
        StructField("jobTitle", StringType(), True),
        StructField("courseCollectionId", StringType(), True),
        StructField("avatar", StringType(), True),
    ]
)

ENROLLMENTS_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": "dateEdited",
    "ingestion_type": "cdc",
}


# =============================================================================
# Groups Table
# =============================================================================

GROUPS_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("isAutomatic", BooleanType(), True),
        StructField("userIds", ArrayType(StringType(), True), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
    ]
)

GROUPS_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": None,
    "ingestion_type": "snapshot",
}


# =============================================================================
# Roles Table
# =============================================================================

ROLES_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("description", StringType(), True),
        StructField("dateEdited", StringType(), True),
        StructField("dateAdded", StringType(), True),
    ]
)

ROLES_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": None,
    "ingestion_type": "snapshot",
}


# =============================================================================
# Countries Table
# =============================================================================

COUNTRIES_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("countryCode", StringType(), True),
        StructField("name", StringType(), True),
    ]
)

COUNTRIES_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": None,
    "ingestion_type": "snapshot",
}


# =============================================================================
# Provinces Table
# =============================================================================

PROVINCES_SCHEMA = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("countryId", StringType(), True),
        StructField("countryName", StringType(), True),
    ]
)

PROVINCES_METADATA = {
    "primary_keys": ["id"],
    "cursor_field": None,
    "ingestion_type": "snapshot",
}


# =============================================================================
# Table Registry
# =============================================================================

TABLE_SCHEMAS = {
    "users": USERS_SCHEMA,
    "departments": DEPARTMENTS_SCHEMA,
    "courses": COURSES_SCHEMA,
    "enrollments": ENROLLMENTS_SCHEMA,
    "groups": GROUPS_SCHEMA,
    "roles": ROLES_SCHEMA,
    "countries": COUNTRIES_SCHEMA,
    "provinces": PROVINCES_SCHEMA,
}

TABLE_METADATA = {
    "users": USERS_METADATA,
    "departments": DEPARTMENTS_METADATA,
    "courses": COURSES_METADATA,
    "enrollments": ENROLLMENTS_METADATA,
    "groups": GROUPS_METADATA,
    "roles": ROLES_METADATA,
    "countries": COUNTRIES_METADATA,
    "provinces": PROVINCES_METADATA,
}

SUPPORTED_TABLES = list(TABLE_SCHEMAS.keys())
