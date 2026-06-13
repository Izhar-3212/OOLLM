# Agile Engineering Practices

## Purpose

Agile delivery depends on technical excellence. The ninth Agile principle states that continuous attention to technical excellence and good design enhances agility. These engineering practices, many originating in Extreme Programming (XP), keep software easy to change so teams can keep delivering value.

---

## Test-Driven Development (TDD)

Test-driven development is a practice where developers write an automated test before writing the code that makes it pass.

The TDD cycle (Red-Green-Refactor):

1. Red: write a small failing test for the next behavior.
2. Green: write the minimal code that makes the test pass.
3. Refactor: clean up the code while keeping all tests passing.

Benefits of TDD:

* Forces thinking about requirements and edge cases before coding.
* Produces comprehensive automated test coverage.
* Acts as living documentation of system behavior.
* Gives confidence to refactor safely.

---

## Behavior-Driven Development (BDD)

Behavior-driven development extends TDD by expressing tests in business-readable language using the Given-When-Then format. BDD focuses on system behavior from the user's perspective and improves communication between developers, testers, and business stakeholders. Acceptance criteria written in Given-When-Then map directly to BDD scenarios.

---

## Continuous Integration (CI)

Continuous integration is the practice of merging code changes into a shared mainline frequently — at least daily, often several times a day — with every merge triggering an automated build and test run.

Benefits of continuous integration:

* Integration problems are found within minutes instead of weeks.
* The codebase stays in a known-working state.
* Feedback on every change is fast and automatic.

---

## Continuous Delivery (CD)

Continuous delivery keeps the software releasable at all times. Every change that passes the automated pipeline can be deployed to production on demand; the business decides when to release.

Continuous deployment goes one step further: every change that passes the pipeline is deployed to production automatically, with no manual approval. This requires strong automated testing, monitoring, and fast rollback.

In Scrum terms, continuous delivery is how each Increment stays potentially shippable.

---

## Refactoring

Refactoring is improving the internal structure of code without changing its external behavior. In Agile development, refactoring happens continuously as part of normal work — not as a separate project — and is commonly part of the Definition of Done. Continuous refactoring keeps technical debt under control and preserves the team's speed.

---

## Technical Debt

Technical debt is the implied cost of future rework created by choosing a quick solution now instead of a better approach that would take longer. Like financial debt, it accrues interest: the longer it remains, the more it slows development and increases defects.

Managing technical debt in Agile teams:

* Make debt visible as items in the Product Backlog.
* Include refactoring and quality gates in the Definition of Done.
* Allocate ongoing capacity (commonly 10–20% of each Sprint) to debt reduction.
* Discuss debt trends in retrospectives.

Unmanaged technical debt is a leading cause of declining velocity.

---

## Pair Programming

Pair programming is two developers working together at one workstation. The driver writes code while the navigator reviews each line, thinks ahead, and spots issues; the pair switches roles frequently.

Benefits: fewer defects, continuous code review, knowledge sharing, faster onboarding, and better design decisions.

---

## Mob Programming

Mob programming (or ensemble programming) extends pairing to the whole team working on one task at one screen, with one driver and many navigators, rotating regularly. It maximizes knowledge sharing and quality, and works especially well for complex problems and new domains, at the cost of raw parallel throughput.

---

## Spikes

A spike is a timeboxed research or prototyping activity used to reduce uncertainty before committing to implementation. Spikes are used when the team faces unknown technology, high complexity, or unclear feasibility. The output of a spike is knowledge — findings, a prototype, or a decision — which then informs estimation and design of the real work.

---

## Minimum Viable Product (MVP)

A minimum viable product is the smallest version of a product that delivers real value to users and tests the riskiest assumptions with the least effort. An MVP is not a broken or half-finished product; it is a complete, narrow solution built to maximize validated learning. Build, measure, learn — then iterate or pivot based on evidence.

---

## DevOps and Agile

DevOps combines development and operations practices to shorten the path from commit to production: automation, infrastructure as code, CI/CD pipelines, monitoring, and shared responsibility for reliability. DevOps complements Agile — Agile shortens the feedback loop of deciding what to build; DevOps shortens the feedback loop of running it in production.

---

## Anti-Patterns

### Speed Over Quality

Skipping tests and refactoring to "go faster" accumulates technical debt and makes every future Sprint slower. Sustainable pace requires built-in quality.

### Hardening Sprints

Reserving special Sprints to fix quality issues means earlier Increments were never really Done. Quality belongs in the Definition of Done of every Sprint.

### Manual Regression Testing Only

Without automated tests, every release becomes slower and riskier as the product grows, and continuous delivery is impossible.

### Test Coverage as a Target

Chasing a coverage percentage produces meaningless tests. Coverage is a byproduct of good practice, not a goal.
