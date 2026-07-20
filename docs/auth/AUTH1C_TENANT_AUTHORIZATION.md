# Auth-1C tenant authorization

- Status: implemented and locally validated
- Date: 2026-07-20
- Schema change: none
- Migration: none

## Objective

Establish the first enforceable organization boundary for authenticated
application routes without trusting organization identifiers or roles
supplied by the client.

## Server resolution

The browser supplies only the organization slug contained in the route.

The server:

1. validates the active Better Auth session;
2. loads the authoritative user state;
3. normalizes the organization slug;
4. queries an ACTIVE membership for the session user;
5. requires the related organization to be ACTIVE;
6. checks the role against the explicit permission matrix;
7. returns the authoritative organization ID;
8. uses that ID in all downstream Prisma queries.

## Permission matrix

### ADMIN

All Auth-1C permissions.

### OPERATOR

Organization read, project read/manage, environment read/manage and
analysis execution.

### VIEWER

Read-only access to organization, projects and environments.

### REVIEWER

Reserved without operational access during Auth-1.

## Platform administrator

PLATFORM_ADMIN is not a MembershipRole and receives no implicit tenant
access.

A platform administrator needs an ACTIVE membership in an ACTIVE
organization before accessing its data.

## Protected routes

- `/app`
- `/app/[organizationSlug]`
- `/app/[organizationSlug]/projects`
- `/app/[organizationSlug]/environments`
- `/api/organizations/[organizationSlug]/context`

## Enumeration resistance

An unknown organization and an organization not authorized for the
current user produce the same external not-found result.

## Tenant-scoped reads

Project queries require:

`organizationId = context.organization.id`

Environment queries require a project whose organizationId equals the
resolved organization ID.

## Deferred

- organization creation;
- membership mutations;
- invitation acceptance;
- project and environment mutations;
- last active ADMIN transaction;
- disposable PostgreSQL integration tests;
- cross-tenant E2E tests;
- import and vulnerability domain isolation.
