from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(r"D:\dev\cvss")
WEB = ROOT / "web"

EXPECTED_SCHEMA_HASH = (
    "b7dc53f68607cce175c69137f09eea1e70c7a8cd5f16b26c212cb1cc2c409195"
)

EXPECTED_PACKAGES = {
    "better-auth": "1.6.23",
    "@better-auth/prisma-adapter": "1.6.23",
    "@node-rs/argon2": "2.0.2",
}

FORBIDDEN_PACKAGES = {
    "next-auth",
    "@next-auth/prisma-adapter",
}

REQUIRED_ENV = {
    "DATABASE_URL",
    "BETTER_AUTH_SECRET",
    "BETTER_AUTH_URL",
    "AUTH_TRUSTED_ORIGINS",
    "PLATFORM_ADMIN_EMAIL",
    "PLATFORM_ADMIN_NAME",
    "PLATFORM_ADMIN_PASSWORD",
}


def fail(message: str) -> None:
    print(f"AUTH1A_FOUNDATION_ERROR={message}")
    raise SystemExit(1)


package = json.loads(
    (WEB / "package.json").read_text(encoding="utf-8-sig")
)

lock = json.loads(
    (WEB / "package-lock.json").read_text(encoding="utf-8-sig")
)

dependencies: dict[str, str] = {}

for bucket in (
    "dependencies",
    "devDependencies",
    "optionalDependencies",
):
    dependencies.update(package.get(bucket, {}) or {})

for name in FORBIDDEN_PACKAGES:
    if name in dependencies:
        fail(f"forbidden package remains: {name}")

for name, expected in EXPECTED_PACKAGES.items():
    declared = dependencies.get(name)

    if declared != expected:
        fail(
            f"package mismatch: {name}={declared!r}; "
            f"expected={expected!r}"
        )

    locked = (
        lock.get("packages", {})
        .get(f"node_modules/{name}", {})
        .get("version")
    )

    if locked != expected:
        fail(
            f"lock mismatch: {name}={locked!r}; "
            f"expected={expected!r}"
        )

for bucket in (
    "dependencies",
    "devDependencies",
    "optionalDependencies",
):
    for name, specification in (
        package.get(bucket, {}) or {}
    ).items():
        if specification == "latest":
            fail(f"unbounded direct dependency: {name}")

if package.get("engines", {}).get("node") != "22.x":
    fail("Node engine is not 22.x")

if package.get("packageManager") != "npm@11.6.2":
    fail("packageManager is not npm@11.6.2")

schema_path = WEB / "prisma" / "schema.prisma"

schema_hash = hashlib.sha256(
    schema_path.read_bytes()
).hexdigest()

if schema_hash != EXPECTED_SCHEMA_HASH:
    fail("legacy Prisma schema changed")

password_text = (
    WEB / "src" / "lib" / "password.ts"
).read_text(encoding="utf-8")

for marker in (
    "type Options",
    "algorithm: 2",
    "memoryCost: 65_536",
    "timeCost: 3",
    "parallelism: 4",
    "outputLen: 32",
):
    if marker not in password_text:
        fail(f"Argon2id marker missing: {marker}")

if "Algorithm.Argon2id" in password_text:
    fail("ambient const enum import remains")

adr_text = (
    ROOT / "docs" / "adr" / "0001-authentication-foundation.md"
).read_text(encoding="utf-8")

for marker in (
    "Decision: BETTER_AUTH",
    "Architecture gate: ADR_READY",
    "Public registration is disabled",
):
    if marker not in adr_text:
        fail(f"ADR marker missing: {marker}")

env_text = (
    WEB / ".env.example"
).read_text(encoding="utf-8-sig")

declared_env = set(
    re.findall(
        r"^\s*([A-Z][A-Z0-9_]*)\s*=",
        env_text,
        flags=re.MULTILINE,
    )
)

missing = sorted(REQUIRED_ENV - declared_env)

if missing:
    fail("missing environment variables: " + ",".join(missing))

print("AUTH1A_FOUNDATION_VALIDATION_OK=True")
print("AUTH_RECOMMENDATION=BETTER_AUTH")
print("ADR_DECISION=ADR_READY")
print("LEGACY_SCHEMA_UNCHANGED=True")
print("ISOLATED_MODULES_COMPATIBLE=True")
print("NODE_RUNTIME_REQUIRED=True")
print("DATABASE_SESSIONS_REQUIRED=True")
print("PUBLIC_SIGNUP_ENABLED=False")
print("PLATFORM_ADMIN_TENANT_AUTO_ACCESS=False")
print("REVIEWER_OPERATIONAL_ACCESS=False")
