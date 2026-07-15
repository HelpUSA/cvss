from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(r"D:\dev\cvss")
WEB = ROOT / "web"

SCHEMA_PATH = (
    WEB / "prisma" / "schema.prisma"
)

MIGRATION_NAME = "202607150001_auth1a_additive_schema"

MIGRATION_ROOT = (
    WEB / "prisma" / "migrations"
)

MIGRATION_SQL = (
    MIGRATION_ROOT
    / MIGRATION_NAME
    / "migration.sql"
)

MIGRATION_LOCK = (
    MIGRATION_ROOT
    / "migration_lock.toml"
)

BASE_SCHEMA_LENGTH = 1869

EXPECTED_BASE_SCHEMA_HASH = (
    "b7dc53f68607cce175c69137f09eea1e70c7a8cd5f16b26c212cb1cc2c409195"
)

EXPECTED_PACKAGES = {
    "better-auth": "1.6.23",
    "@better-auth/prisma-adapter": "1.6.23",
    "@node-rs/argon2": "2.0.2",
}

EXPECTED_ENUMS = {
    "UserStatus",
    "PlatformRole",
    "OrganizationStatus",
    "MembershipRole",
    "MembershipStatus",
    "ProjectStatus",
    "EnvironmentStatus",
}

EXPECTED_MODELS = {
    "User",
    "Session",
    "Account",
    "Verification",
    "Organization",
    "Membership",
    "Project",
    "Environment",
    "Invitation",
    "PasswordResetToken",
    "SecurityAuditEvent",
}

LEGACY_MODELS = {
    "Run",
    "Assessment",
    "Comparison",
    "AuditEvent",
}


def fail(message: str) -> None:
    print(
        "AUTH1A_SCHEMA_VALIDATION_ERROR="
        + message
    )
    raise SystemExit(1)


def normalize_statement(
    statement: str,
) -> str:
    return re.sub(
        r"\s+",
        " ",
        statement,
    ).strip()


schema_bytes = SCHEMA_PATH.read_bytes()

if len(schema_bytes) <= BASE_SCHEMA_LENGTH:
    fail("schema was not extended")

base_prefix = schema_bytes[
    :BASE_SCHEMA_LENGTH
]

base_hash = hashlib.sha256(
    base_prefix
).hexdigest()

if (
    base_hash
    != EXPECTED_BASE_SCHEMA_HASH
):
    fail(
        "legacy schema prefix changed: "
        + base_hash
    )

schema_text = schema_bytes.decode(
    "utf-8-sig",
    errors="strict",
)

model_names = set(
    re.findall(
        r"^\s*model\s+(\w+)\s*\{",
        schema_text,
        flags=re.MULTILINE,
    )
)

enum_names = set(
    re.findall(
        r"^\s*enum\s+(\w+)\s*\{",
        schema_text,
        flags=re.MULTILINE,
    )
)

missing_models = sorted(
    EXPECTED_MODELS - model_names
)

missing_enums = sorted(
    EXPECTED_ENUMS - enum_names
)

missing_legacy = sorted(
    LEGACY_MODELS - model_names
)

if missing_models:
    fail(
        "missing models: "
        + ",".join(missing_models)
    )

if missing_enums:
    fail(
        "missing enums: "
        + ",".join(missing_enums)
    )

if missing_legacy:
    fail(
        "missing legacy models: "
        + ",".join(missing_legacy)
    )

required_schema_markers = (
    "email                 String               @unique",
    "emailVerified         Boolean              @default(false)",
    "password              String?   @db.Text",
    "@@unique([providerId, accountId])",
    "@@unique([organizationId, userId])",
    "@@unique([organizationId, slug])",
    "@@unique([projectId, slug])",
    "model SecurityAuditEvent {",
)

for marker in required_schema_markers:
    if marker not in schema_text:
        fail(
            "missing schema marker: "
            + marker
        )

package = json.loads(
    (WEB / "package.json").read_text(
        encoding="utf-8-sig",
    )
)

lock = json.loads(
    (WEB / "package-lock.json").read_text(
        encoding="utf-8-sig",
    )
)

dependencies: dict[str, str] = {}

for bucket in (
    "dependencies",
    "devDependencies",
    "optionalDependencies",
):
    dependencies.update(
        package.get(bucket, {}) or {}
    )

for (
    name,
    expected_version,
) in EXPECTED_PACKAGES.items():
    declared = dependencies.get(name)

    if declared != expected_version:
        fail(
            "dependency mismatch: "
            f"{name}={declared!r}"
        )

    locked = (
        lock.get("packages", {})
        .get(
            f"node_modules/{name}",
            {},
        )
        .get("version")
    )

    if locked != expected_version:
        fail(
            "lock mismatch: "
            f"{name}={locked!r}"
        )

if not MIGRATION_SQL.exists():
    fail("migration SQL is missing")

if not MIGRATION_LOCK.exists():
    fail("migration lock is missing")

migration_lock_text = (
    MIGRATION_LOCK.read_text(
        encoding="utf-8",
    )
)

if (
    'provider = "postgresql"'
    not in migration_lock_text
):
    fail(
        "migration lock provider "
        "is not PostgreSQL"
    )

sql = MIGRATION_SQL.read_text(
    encoding="utf-8",
)

if not sql.strip():
    fail("migration SQL is empty")

sql_without_comments = re.sub(
    r"/\*.*?\*/",
    "",
    sql,
    flags=re.DOTALL,
)

sql_without_comments = re.sub(
    r"(?m)^\s*--.*$",
    "",
    sql_without_comments,
)

for legacy_model in LEGACY_MODELS:
    if re.search(
        rf'"{re.escape(legacy_model)}"',
        sql_without_comments,
        flags=re.IGNORECASE,
    ):
        fail(
            "migration references "
            "legacy model: "
            + legacy_model
        )

statements = [
    normalize_statement(statement)
    for statement
    in sql_without_comments.split(";")
    if statement.strip()
]

if not statements:
    fail(
        "migration contains "
        "no SQL statements"
    )

created_tables: set[str] = set()
created_enums: set[str] = set()
index_target_tables: set[str] = set()
altered_tables: set[str] = set()

on_update_clause_count = len(
    re.findall(
        r"\bON\s+UPDATE\b",
        sql_without_comments,
        flags=re.IGNORECASE,
    )
)

top_level_update_count = 0

for statement in statements:
    if re.match(
        r"^UPDATE\b",
        statement,
        flags=re.IGNORECASE,
    ):
        top_level_update_count += 1

        fail(
            "top-level UPDATE statement detected"
        )

    destructive_match = re.match(
        (
            r"^(DROP|TRUNCATE|DELETE|INSERT|"
            r"MERGE|GRANT|REVOKE|CALL|DO)\b"
        ),
        statement,
        flags=re.IGNORECASE,
    )

    if destructive_match:
        fail(
            "destructive or unauthorized "
            "SQL statement detected: "
            + destructive_match.group(1)
        )

    enum_match = re.match(
        r'^CREATE\s+TYPE\s+"([^"]+)"\s+AS\s+ENUM\b',
        statement,
        flags=re.IGNORECASE,
    )

    if enum_match:
        enum_name = enum_match.group(1)

        if enum_name not in EXPECTED_ENUMS:
            fail(
                "unexpected enum created: "
                + enum_name
            )

        created_enums.add(enum_name)
        continue

    table_match = re.match(
        r'^CREATE\s+TABLE\s+"([^"]+)"\s*\(',
        statement,
        flags=re.IGNORECASE,
    )

    if table_match:
        table_name = table_match.group(1)

        if table_name not in EXPECTED_MODELS:
            fail(
                "unexpected table created: "
                + table_name
            )

        created_tables.add(table_name)
        continue

    index_match = re.match(
        (
            r'^CREATE\s+(?:UNIQUE\s+)?INDEX\s+'
            r'"[^"]+"\s+ON\s+"([^"]+)"\s*\('
        ),
        statement,
        flags=re.IGNORECASE,
    )

    if index_match:
        table_name = index_match.group(1)

        if table_name not in EXPECTED_MODELS:
            fail(
                "index targets unauthorized table: "
                + table_name
            )

        index_target_tables.add(table_name)
        continue

    foreign_key_match = re.match(
        (
            r'^ALTER\s+TABLE\s+"([^"]+)"\s+'
            r'ADD\s+CONSTRAINT\s+"[^"]+"\s+'
            r'FOREIGN\s+KEY\b'
        ),
        statement,
        flags=re.IGNORECASE,
    )

    if foreign_key_match:
        table_name = (
            foreign_key_match.group(1)
        )

        if table_name not in EXPECTED_MODELS:
            fail(
                "foreign key alters "
                "unauthorized table: "
                + table_name
            )

        altered_tables.add(table_name)
        continue

    if re.fullmatch(
        r"BEGIN",
        statement,
        flags=re.IGNORECASE,
    ):
        continue

    if re.fullmatch(
        r"COMMIT",
        statement,
        flags=re.IGNORECASE,
    ):
        continue

    fail(
        "unexpected SQL statement: "
        + statement[:300]
    )

missing_created_tables = sorted(
    EXPECTED_MODELS - created_tables
)

unexpected_created_tables = sorted(
    created_tables - EXPECTED_MODELS
)

missing_created_enums = sorted(
    EXPECTED_ENUMS - created_enums
)

unexpected_created_enums = sorted(
    created_enums - EXPECTED_ENUMS
)

if missing_created_tables:
    fail(
        "migration does not create tables: "
        + ",".join(missing_created_tables)
    )

if unexpected_created_tables:
    fail(
        "migration creates extra tables: "
        + ",".join(
            unexpected_created_tables
        )
    )

if missing_created_enums:
    fail(
        "migration does not create enums: "
        + ",".join(missing_created_enums)
    )

if unexpected_created_enums:
    fail(
        "migration creates extra enums: "
        + ",".join(
            unexpected_created_enums
        )
    )

for legacy_model in LEGACY_MODELS:
    if re.search(
        (
            rf'\bREFERENCES\s+'
            rf'"{re.escape(legacy_model)}"'
        ),
        sql_without_comments,
        flags=re.IGNORECASE,
    ):
        fail(
            "migration creates relation to "
            + legacy_model
        )

print("AUTH1A_SCHEMA_VALIDATION_OK=True")
print("AUTH1A_MIGRATION_SQL_VALID=True")
print("AUTH1A_MIGRATION_ADDITIVE_ONLY=True")
print("LEGACY_SCHEMA_PREFIX_UNCHANGED=True")
print("LEGACY_MODELS_REFERENCED_BY_SQL=False")
print("DESTRUCTIVE_SQL_DETECTED=False")

print(
    "TOP_LEVEL_UPDATE_STATEMENT_COUNT="
    f"{top_level_update_count}"
)

print(
    "ON_UPDATE_CLAUSE_COUNT="
    f"{on_update_clause_count}"
)

print(
    "ON_UPDATE_CLAUSES_ACCEPTED_AS_REFERENTIAL_ACTIONS=True"
)

print(
    "CREATED_TABLE_COUNT="
    f"{len(created_tables)}"
)

print(
    "CREATED_ENUM_COUNT="
    f"{len(created_enums)}"
)

print(
    "INDEX_TARGET_TABLE_COUNT="
    f"{len(index_target_tables)}"
)

print(
    "FOREIGN_KEY_SOURCE_TABLE_COUNT="
    f"{len(altered_tables)}"
)

print("DATABASE_CONNECTION_USED=False")
print("DATABASE_MODIFIED=False")
print("MIGRATION_APPLIED=False")
print("USER_MODEL_PRESENT=True")
print("SESSION_MODEL_PRESENT=True")
print("ACCOUNT_MODEL_PRESENT=True")
print("VERIFICATION_MODEL_PRESENT=True")
print("TENANT_MODELS_PRESENT=True")
print("SECURITY_AUDIT_EVENT_PRESENT=True")
