<!--
Sync Impact Report
Version change: template placeholders → 1.0.0
Modified principles: N/A (initial adoption from template)
Added sections: Core Principles I–IV; Specification Traceability; Review & Quality Gates
Removed sections: Fifth placeholder principle (consolidated into four user-driven principles)
Templates requiring updates:
  - .specify/templates/plan-template.md — ✅ updated (Constitution Check gates)
  - .specify/templates/spec-template.md — ✅ updated (constitution alignment note)
  - .specify/templates/tasks-template.md — ✅ updated (testing vs constitution)
  - .specify/templates/commands/*.md — ⚠ N/A (directory not present; commands live under .cursor/commands)
Follow-up TODOs: None
-->

# test_speckit Constitution

## Core Principles

### I. Code Quality

All production code MUST pass the project’s lint, format, and static analysis checks with zero
unjustified suppressions. Changes MUST follow established naming, module structure, and error-handling
patterns in this repository; new public surfaces MUST be documented or self-evident at call sites.
Material complexity MUST be justified in review (or in the plan’s Complexity Tracking when
exceptional). **Rationale:** Consistent quality keeps reviews fast, reduces defects, and preserves
refactorability.

### II. Testing Standards

Automated tests MUST accompany behavior changes: unit tests for core logic; integration or contract
tests when boundaries, persistence, or external systems change. When fixing regressions, contributors
MUST add or extend a test that would have failed before the fix, unless the plan records a justified
exception. Flaky tests MUST be fixed, skipped only with a tracked owner and remediation deadline, or
removed after replacement coverage. Feature specs MUST keep each user story independently testable
with a clear **Independent Test** description. **Rationale:** Tests encode intent and prevent
repeat failures across releases.

### III. User Experience Consistency

User-facing flows MUST reuse established interaction, visual, and copy patterns (components,
navigation, spacing, terminology) unless the specification documents an intentional deviation.
Interactive UI MUST be keyboard-usable and expose meaningful names/roles for assistive technologies
where applicable. Loading, empty, and error states MUST be explicit—no silent failures or ambiguous
dead ends. **Rationale:** Consistency reduces training cost, accessibility risk, and support load.

### IV. Performance Requirements

Every feature MUST declare measurable performance expectations in the plan and/or spec (for example
p95 latency, throughput, bundle size, frame time, or memory) appropriate to the user surface and
scale. Implementations MUST avoid known anti-patterns (unbounded work on hot paths, N+1 data access,
blocking the UI thread) unless documented and approved in Complexity Tracking. Degradations beyond
agreed budgets MUST be remediated or the specification MUST be explicitly revised before release.
**Rationale:** Performance is a product attribute; budgets make trade-offs objective.

## Specification Traceability

Functional requirements in feature specifications MUST map to user stories and to measurable success
criteria. Non-functional expectations governed by this constitution—especially UX consistency and
performance—MUST appear as success criteria or explicit non-functional requirements where they apply,
not only as informal notes.

## Review & Quality Gates

Pull requests MUST be checked against this constitution (and the Implementation Plan’s Constitution
Check). Merge MUST NOT proceed with unresolved violations unless Complexity Tracking records an
approved justification. Continuous integration MUST run lint, tests, and any repository-defined
performance or bundle checks configured for the branch.

## Governance

This constitution supersedes conflicting informal practices for this repository. Amendments require
an update to `.specify/memory/constitution.md`, semantic version bump, propagation to dependent
templates where principles change review or spec expectations, and an entry in the Sync Impact
Report comment at the top of this file. Maintainers SHOULD review compliance at least once per
release cycle or when principles materially change.

**Version**: 1.0.0 | **Ratified**: 2025-03-27 | **Last Amended**: 2025-03-27
