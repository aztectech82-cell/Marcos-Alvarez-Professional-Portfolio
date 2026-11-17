# Axiom 15 — Iterative Wellness-App Product Development

Axiom 15 is a pre-revenue wellness-app concept developed through web prototypes, an MBA capstone, and a native Apple-platform architecture. The case study demonstrates product iteration, data/privacy boundaries, deterministic local behavior, and fail-closed release engineering.

## Verified Milestones

- Six full application versions were built and iterated over roughly three months in 2026.
- The product served as the real client project for a UC Riverside MGT 238 Management Synthesis capstone team.
- A U.S. Intent-to-Use trademark application was filed June 16, 2026: Serial 99887976, Class 009, owner VFT LLC.

The filing is an application, not a registered trademark.

## Product Work

- Responsive web MVP with session navigation, progress/streak state, and payment-integration scaffolding.
- Native Swift/SwiftUI source scaffold for iPhone and a separate private Mac development target.
- Deterministic 5-, 10-, and 15-minute session planning.
- Local JSON-vault architecture with ordered atomic writes, export, and confirmed deletion flows.
- StoreKit 2 entitlement boundaries.
- Safety content available independently of paid access.
- Unit tests for access tiers, timing, persistence, deletion/export, reflection bounds, and calendar input states.

## Release Engineering

The current native scaffold is intentionally not release-ready. Release gates reject unavailable calendar calculations, unapproved public copy, private-target leakage, and improperly configured AI features. It has not been compiled or archived with Xcode in the Windows development environment.

This is a deliberate product lesson: a working prototype, a payment scaffold, and a filed application do not equal a launch-ready consumer product.

## Claims and Safety Boundary

Axiom 15 is not presented as a medical device or treatment. The public architecture separates reflective wellness content from health claims, keeps crisis/safety routes outside the paywall, and requires legal, privacy, licensing, accessibility, and device validation before release.

No personal journal, health information, birth data, confidential product copy, or private target source is included in this portfolio.
