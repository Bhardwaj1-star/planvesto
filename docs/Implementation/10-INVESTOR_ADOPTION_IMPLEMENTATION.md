# Investor Adoption Implementation

Explicit state transition: Recommendation → Review → Accept / Reject / Modify. Accept creates/updates Accepted Plan; Reject leaves the existing Accepted Plan unchanged; Modify re-enters the affected planning/Strategy flow.

Never treat recommendation generation as adoption. Preserve rejected/proposed versions.

References: `docs/User Journeys/10-INVESTOR_ADOPTION_JOURNEY.md`, `docs/User Journeys/11-ACCEPTED_PLAN_JOURNEY.md`.