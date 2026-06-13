# User Stories and Agile Requirements

## Definition

A user story is a short, simple description of a feature told from the perspective of the person who desires the capability, usually a user or customer of the system. A user story is a placeholder for a conversation, not a detailed specification.

Standard user story format:

As a [type of user], I want [some goal], so that [some benefit].

Example:

As a registered customer, I want to save my shipping address, so that I can check out faster on future orders.

---

## The Three Cs of User Stories

User stories consist of three parts, known as the Three Cs:

* Card: the short written description of the story.
* Conversation: the discussion between the team and the Product Owner that uncovers details.
* Confirmation: the acceptance criteria that confirm the story is complete.

---

## INVEST Criteria

INVEST is a checklist for writing good user stories. A good user story is:

* Independent: it can be developed and delivered separately from other stories.
* Negotiable: it is not a fixed contract; details emerge through conversation.
* Valuable: it delivers visible value to users or customers.
* Estimable: the team has enough information to size it.
* Small: it is small enough to complete within one Sprint.
* Testable: it has clear acceptance criteria that can be verified.

If a story fails the INVEST criteria, split it or refine it before bringing it into a Sprint.

---

## Acceptance Criteria

Acceptance criteria define the specific, testable conditions a user story must satisfy to be considered complete. They are written from the user's perspective and agreed before development starts.

Common format (Gherkin / Given-When-Then):

Given [a context or precondition], when [an action is performed], then [an expected result occurs].

Example:

Given I am logged in, when I add an item to my cart and the item is out of stock, then I see an out-of-stock message and the item is not added.

Purpose of acceptance criteria:

* Clarify requirements and remove ambiguity.
* Guide development and testing.
* Form the basis for acceptance tests.
* Prevent scope creep within a story.

Each story should have acceptance criteria covering the happy path and important edge cases.

---

## Definition of Ready

The Definition of Ready is a team agreement listing the conditions a user story must meet before it can be pulled into a Sprint.

Typical Definition of Ready criteria:

* The story is clearly written and understood by the team.
* Acceptance criteria are defined.
* Dependencies are identified.
* The story is estimated.
* The story is small enough to complete in one Sprint.
* The business value is clear.

The Definition of Ready prevents teams from starting work on unclear items, reducing rework and mid-sprint surprises. It is a useful team practice but is not an official Scrum artifact.

---

## Splitting User Stories

Stories that are too large to complete in one Sprint should be split into smaller stories that are still valuable and testable. To split a large user story, slice it by workflow steps, business rule variations, user types, CRUD operations, or happy path versus edge cases.

Common story splitting strategies:

* By workflow steps: each step of the user journey becomes a story.
* By business rule variations: different rules become different stories.
* By user type: separate stories for admin users versus regular users.
* By CRUD operations: create, read, update, and delete as separate stories.
* By happy path versus edge cases: deliver the main flow first, then exceptions.
* By platform or interface: web, mobile, and API as separate stories.
* By data variations: support one data type first, then others.
* Spike then implement: split out a timeboxed research spike when uncertainty is high.

Each split piece must still deliver user value; avoid splitting into technical layers (such as "database story" and "UI story") because layer-based slices are not independently valuable.

---

## Epics, Features, and Themes

* Epic: a large body of work that cannot be completed in one Sprint and is broken down into smaller user stories.
* Feature: a service or capability of the product, typically delivered through several stories.
* Theme: a collection of related stories or epics grouped by a common goal, used for portfolio-level organization.

Hierarchy:

Theme -> Epic -> User Story -> Task

Tasks are the technical activities (design, code, test) Developers identify during Sprint Planning to deliver a story. Tasks are typically estimated in hours, while stories are estimated in story points.

---

## Story Mapping

Story mapping is a visual technique, popularized by Jeff Patton, for organizing user stories along two dimensions:

* Horizontal axis: the user journey or workflow activities in sequence.
* Vertical axis: priority, with the most essential stories at the top.

Benefits of story mapping:

* Shows the big picture of the product from the user's perspective.
* Helps identify a walking skeleton or minimum viable product: the top horizontal slice.
* Reveals gaps and dependencies in the backlog.
* Supports release planning by slicing the map into increments.

---

## Anti-Patterns

### Stories as Mini Contracts

Problem: Treating the story text as a complete specification eliminates the conversation, which is where shared understanding is built.

### Technical Stories Without User Value

Problem: Stories written as technical tasks ("upgrade the database") hide value from the Product Owner. Express the user or business outcome, or manage the work as enablement with explicit value.

### Stories Too Large to Finish

Problem: Large stories carry over Sprint after Sprint, hide risk, and destroy predictability. Apply splitting strategies and the INVEST criteria.

### Acceptance Criteria Written After Development

Problem: Criteria written late become a description of what was built rather than what was needed, so defects and rework increase.
