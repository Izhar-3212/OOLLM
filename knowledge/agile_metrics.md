# Agile Metrics and Charts

## Purpose

Agile metrics help teams inspect progress, improve flow, and forecast delivery. Metrics are tools for learning and planning, never weapons for judging individuals or comparing teams.

---

## Velocity

Velocity is the Scrum metric for the average number of story points a team completes per Sprint. To calculate velocity in Scrum, sum the story points of fully completed stories (stories that meet the Definition of Done) in each Sprint, then average over the last three to six Sprints.

Example calculation:

* Sprint 1: 30 points completed
* Sprint 2: 36 points completed
* Sprint 3: 33 points completed
* Average velocity: (30 + 36 + 33) / 3 = 33 points per Sprint

Velocity is used in Sprint Planning to select a realistic amount of work and in release planning to forecast completion dates.

Rules for healthy velocity use:

* Only count fully completed work; partially done stories count as zero.
* Velocity is team-specific; never compare velocity between teams.
* Velocity is a planning tool, not a performance target. Treating velocity as a target causes point inflation and quality loss.

---

## Burn-Down Chart

A burn-down chart shows the amount of work remaining over time. The X-axis is time (days of a Sprint or Sprints of a release) and the Y-axis is remaining work (story points or hours).

How to read a burn-down chart:

* The ideal line shows perfectly even progress from total work to zero.
* The actual line shows real remaining work.
* If the actual line is above the ideal line, the team is behind.
* If the actual line is below the ideal line, the team is ahead.

Burn-down charts are simple but hide scope changes: added work makes the team look slower without showing why.

---

## Burn-Up Chart

A burn-up chart shows work completed over time with two lines: one for total scope and one for completed work. The chart "burns up" toward the scope line.

Advantages over burn-down:

* Scope changes are visible: when scope is added, the total scope line moves up.
* Better for long-term release tracking and stakeholder communication, because it separates progress from scope growth.

---

## Cumulative Flow Diagram (CFD)

A cumulative flow diagram is an area chart showing the count of work items in each workflow state (such as To Do, In Progress, Testing, Done) over time. It is the primary flow chart for Kanban teams.

How to read a CFD:

* A healthy CFD shows smooth, roughly parallel bands.
* A widening band indicates a bottleneck in that stage: work is arriving faster than it leaves.
* The vertical distance between bands approximates work in progress (WIP).
* The horizontal distance between bands approximates average cycle time.

---

## Lead Time and Cycle Time

Lead time is the total elapsed time from commitment (when a request is accepted) to delivery to the customer. Lead time measures the customer's waiting experience.

Cycle time is the elapsed time from when active work starts on an item until it is delivered. Cycle time measures workflow efficiency.

Lead time includes waiting time before work begins; cycle time does not. Shorter and more consistent lead and cycle times mean faster, more predictable delivery.

---

## Throughput

Throughput is the number of work items completed per unit of time, for example 12 stories per week. Throughput is counted in items, not story points, which makes it stable and simple. Throughput is the preferred input for probabilistic forecasting in Kanban systems.

---

## Little's Law

Little's Law describes the fundamental relationship of flow systems:

Average Cycle Time = Average Work In Progress / Average Throughput

Implications:

* Reducing WIP while throughput stays constant reduces cycle time.
* This is the mathematical reason WIP limits make delivery faster.
* Little's Law holds for stable systems over sufficiently long periods.

---

## Flow Efficiency

Flow efficiency is the percentage of total lead time during which an item is actively worked on:

Flow Efficiency = Active Work Time / Total Lead Time × 100%

Typical flow efficiency in knowledge work is 15% to 20%, meaning most of an item's life is spent waiting. Improving flow efficiency means attacking queues, handoffs, and blockers rather than pushing people to work faster.

---

## Monte Carlo Forecasting

Monte Carlo simulation uses historical throughput data to run thousands of simulated futures and produce probabilistic forecasts, for example: "There is an 85% chance of completing 40 items by March 15."

Benefits:

* Provides a range with confidence levels instead of a single-point estimate.
* Based on actual historical data rather than guesses.
* Works with throughput, so teams can forecast without estimating every item.

---

## Escaped Defects

Escaped defects are bugs discovered in production after release. Tracking escaped defects per release measures the effectiveness of the team's quality practices and Definition of Done.

---

## Metric Anti-Patterns

### Velocity as a Performance Target

Pressuring teams to increase velocity causes point inflation, cut corners, and burnout. Velocity should inform planning only.

### Comparing Teams by Velocity

Story points are team-specific by design. Cross-team velocity comparison is meaningless and destroys trust.

### Measuring Individual Utilization

Optimizing for everyone being busy increases WIP and slows the system. Optimize flow of work, not utilization of workers.

### Vanity Metrics

Metrics that look good but drive no decisions (hours logged, tasks started, lines of code) waste attention. Every tracked metric should answer a real planning or improvement question.
