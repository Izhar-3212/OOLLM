# Scaling Agile and Hybrid Approaches

## When Scaling Is Needed

A single Scrum Team of ten or fewer people is the most effective unit of Agile delivery. Scaling frameworks become relevant when many teams must work on the same product and coordinate dependencies, integration, and shared goals. The first rule of scaling: descale first — simplify the product, architecture, and organization before adding coordination structure.

---

## Scrum of Scrums

A Scrum of Scrums coordinates multiple Scrum Teams working on the same product. Each team sends a representative to a regular (often daily or twice-weekly) coordination meeting focused on cross-team dependencies, integration issues, and impediments that need escalation. It is a coordination meeting, not a status meeting, and is the lightest-weight scaling pattern.

---

## Nexus

Nexus is a scaling framework from Scrum.org for three to nine Scrum Teams working on one product from one Product Backlog. Nexus adds:

* A Nexus Integration Team accountable for ensuring an integrated Increment.
* Nexus-level events that wrap the regular Scrum events (Nexus Sprint Planning, Nexus Daily Scrum, Nexus Sprint Review, Nexus Sprint Retrospective).
* A single integrated Increment per Sprint across all teams.

Nexus stays close to plain Scrum and emphasizes integration as the primary scaling problem.

---

## LeSS (Large-Scale Scrum)

LeSS applies one-team Scrum to many teams with minimal additions: one Product Owner, one Product Backlog, one Sprint, and one shippable Increment across two to eight teams (LeSS Huge extends beyond eight). LeSS strongly favors feature teams over component teams and organizational descaling — removing roles and structures rather than adding them.

---

## SAFe (Scaled Agile Framework)

SAFe (the Scaled Agile Framework) is a comprehensive framework for scaling Agile across large enterprises, providing defined roles, artifacts, and events at team, program, and portfolio levels. Its signature elements are the Agile Release Train and PI Planning.

Key SAFe concepts:

* Agile Release Train (ART): a long-lived team of Agile teams (typically 50–125 people) that plans and delivers together.
* PI Planning: a cadence-based (typically quarterly) planning event where all teams on the train plan the next Program Increment together.
* Roles such as Release Train Engineer, Product Management, and System Architect.

SAFe is widely adopted in large enterprises and is also widely criticized: it adds substantial process and roles, and poorly implemented SAFe can become waterfall with Agile vocabulary. Teams should treat SAFe as a toolkit to adapt, not a mandate to install wholesale.

---

## Spotify Model

The Spotify model describes squads (autonomous teams), tribes (groups of squads), chapters (skill-based groups across squads), and guilds (communities of interest). Important caveat: Spotify itself describes it as a snapshot of their culture at one time, not a framework to copy. Copying the structure without the underlying culture of autonomy and trust rarely works.

---

## Scrumban

Scrumban is a hybrid of Scrum and Kanban. Teams typically keep Scrum's roles and events while adopting Kanban practices: visualizing workflow on a board, limiting work in progress, managing flow with cycle time and throughput metrics, and pulling work continuously.

Common reasons teams adopt Scrumban:

* Work is interrupt-driven (support, operations) and fixed Sprint commitments fit poorly.
* The team wants flow metrics and WIP limits without abandoning Scrum events.
* The team is evolving from Scrum toward continuous flow.

---

## Choosing an Approach

Guidance for selecting frameworks:

* One team: plain Scrum or Kanban — no scaling framework needed.
* A few teams, one product: Scrum of Scrums, Nexus, or LeSS keep overhead low.
* Large enterprise with many products and heavy coordination needs: SAFe provides structure, at the cost of weight.
* Interrupt-driven or flow-centric work: Kanban or Scrumban.

Principles that apply regardless of framework:

* Prefer the lightest structure that solves the actual coordination problem.
* Keep a single Product Backlog and single Product Owner voice per product.
* Optimize for delivering integrated, working product every iteration.
* Invest in technical practices (CI/CD, test automation); no framework compensates for inability to integrate.

---

## Scaling Anti-Patterns

### Scaling Before Mastering the Basics

Rolling out a scaling framework when individual teams cannot yet deliver a Done Increment amplifies dysfunction instead of fixing it.

### Component Teams Everywhere

Teams organized around technical layers (database team, API team, UI team) create dependency chains where no team can deliver value alone. Prefer cross-functional feature teams.

### Process Theater

Adopting the ceremonies and titles of a framework without changing how decisions are made produces Agile in name only — sometimes called "dark Scrum" or "SAFe theater."

### Dependency Management Instead of Dependency Removal

Mature scaling reduces dependencies through architecture and team design; immature scaling builds ever-larger coordination meetings to manage them.
