# Authentication and Resource Authorization

Load when the request concerns restricting endpoints, role/policy checks, or deciding access against a loaded entity. The central distinction: **declarative endpoint authorization** (attribute-based, before the resource exists) versus **imperative resource authorization** (code-based, after the resource is loaded).

## Authentication is not authorization

Authentication establishes identity; authorization decides access. Configuring authentication does not, by itself, restrict any endpoint. To require authenticated users by default, add a **fallback authorization policy**; otherwise unauthenticated requests reach endpoints that lack their own `[Authorize]`.

## Declarative authorization

Declarative checks are attributes evaluated by the framework before data binding and before any resource is loaded:

- `[Authorize]` — requires an authenticated user.
- `[Authorize(Roles = "...")]` — role check against the user's claims.
- `[Authorize(Policy = "...")]` — a named policy built from one or more `IAuthorizationRequirement`s, each evaluated by a handler against the user's claims.

Use these when the decision depends only on the user's identity and claims, not on the contents of a specific entity.

## Resource-based authorization is imperative

When the decision depends on the resource itself — "can this user edit **this** document" — declarative attributes cannot express it: they run before the resource is loaded. Use the imperative path:

1. Inject `IAuthorizationService` (registered by the framework at startup, available via DI).
2. Load the resource.
3. Call `AuthorizeAsync(user, resource, policyName)` or `AuthorizeAsync(user, resource, requirements)`.
4. Branch on the returned `AuthorizationResult.Succeeded`.

Do not replace this with an ad-hoc `if (user == resource.Owner)` that bypasses the authorization model; route the decision through the policy and handler so it is testable and auditable.

## What to check in a review

1. Is authentication configured but no fallback policy, leaving endpoints open by default?
2. Does an `[Authorize]` attribute try to decide based on a resource that is not yet loaded?
3. Is a resource-level decision implemented imperatively with `IAuthorizationService` rather than inline owner checks?
4. Is the policy/handler model used for anything beyond a trivial role check?

## Verified vs synthesis

The authentication/authorization separation, the fallback-policy requirement, the declarative model, and the `IAuthorizationService.AuthorizeAsync` resource pattern are documented in the Microsoft authorization pages. The review checklist is synthesis (structuring of documented facts).

## Official references

- Introduction to authorization in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/security/authorization/introduction
- Resource-based authorization: https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resourcebased
