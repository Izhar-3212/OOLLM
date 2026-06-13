# Agile Estimation

## Definition

Agile estimation is the process of determining the relative size, effort, or complexity of work items to enable effective planning and forecasting.

Estimation in Agile:

* Is relative, not absolute.
* Focuses on complexity and effort, not time.
* Is collaborative and team-based.
* Improves through practice and feedback.
* Enables predictability, not precision.

---

## Purpose

Agile estimation exists to:

* Enable sprint planning and capacity decisions.
* Provide forecasting for stakeholders.
* Identify complexity and risks early.
* Build shared understanding within teams.
* Track team velocity and improvement over time.

---

## Core Concepts

### Relative Estimation

Definition:

Comparing work items against each other rather than estimating in absolute terms.

Principle:

Humans are better at comparing things than assigning absolute values.

Example:

* "Is this story bigger or smaller than that one?"
* "This is about twice as complex as that one."

Benefits:

* Faster than absolute estimation.
* More accurate for uncertain work.
* Reduces anchoring bias.

---

### Story Points

Definition:

A unit of measure for expressing the overall size of a user story or feature.

Components:

* Effort (amount of work)
* Complexity (difficulty of implementation)
* Uncertainty (unknowns and risks)

Scale:

Typically uses modified Fibonacci sequence:

* 0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89

Rationale:

* Larger numbers reflect increasing uncertainty.
* Gaps between numbers prevent false precision.
* Encourages relative thinking.

---

### Ideal Days

Definition:

The amount of work an item would take if there were no interruptions, meetings, or delays.

Characteristics:

* Assumes perfect conditions.
* Not the same as elapsed time.
* Useful for teams transitioning from time-based estimation.

Limitations:

* People interpret "ideal day" differently.
* Less effective than story points for relative sizing.
* Can create false precision.

---

## Estimation Techniques

### Planning Poker

Definition:

Planning Poker is a consensus-based, gamified technique for estimating user stories. After a discussion of the story, every estimator privately selects a Fibonacci card and all cards are revealed simultaneously. The simultaneous reveal prevents anchoring bias; discussion of high and low outliers continues until the team reaches consensus.

Process:

1. Product Owner presents a user story.
2. Team discusses requirements and acceptance criteria.
3. Each estimator privately selects a card (Fibonacci number).
4. All cards are revealed simultaneously.
5. If estimates vary widely, high and low estimators explain reasoning.
6. Team re-estimates until consensus is reached.

Benefits:

* Prevents anchoring bias.
* Ensures all voices are heard.
* Builds shared understanding.
* Makes estimation collaborative and engaging.

Variations:

* **Fibonacci Poker**: Uses 1, 2, 3, 5, 8, 13, 21
* **T-Shirt Poker**: Uses XS, S, M, L, XL
* **Async Poker**: Team votes remotely over time

---

### T-Shirt Sizing

Definition:

Estimating work using clothing sizes as a relative scale.

Scale:

* XS (Extra Small)
* S (Small)
* M (Medium)
* L (Large)
* XL (Extra Large)
* XXL (Extra Extra Large)

Use Cases:

* High-level roadmap planning.
* Initial backlog prioritization.
* Communicating with non-technical stakeholders.
* Early-stage estimation before detailed refinement.

Mapping to Story Points:

* XS = 1 point
* S = 2-3 points
* M = 5 points
* L = 8 points
* XL = 13 points
* XXL = Split the story

---

### Affinity Estimation

Definition:

A rapid, visual technique for sizing multiple stories by grouping them by relative size.

Process:

1. Create columns on a wall or board: XS, S, M, L, XL.
2. Team members silently place stories in columns.
3. Review placements as a group.
4. Adjust stories that seem misplaced.
5. Assign Fibonacci values to columns.

Benefits:

* Very fast for large backlogs.
* Highly visual and collaborative.
* Builds consensus quickly.
* Good for initial backlog refinement.

Limitations:

* Less precise than Planning Poker.
* Can be dominated by loud voices.
* Requires physical or virtual space.

---

### Bucket System

Definition:

A hybrid technique combining affinity estimation with sequential refinement.

Process:

1. Create buckets labeled with Fibonacci numbers.
2. Place a "reference story" in the appropriate bucket.
3. Team places remaining stories relative to the reference.
4. Discuss and adjust outliers.

Benefits:

* Faster than Planning Poker for large backlogs.
* More structured than pure affinity estimation.
* Good balance of speed and accuracy.

---

### Three-Point Estimation

Definition:

Estimating using three scenarios: best case, most likely, and worst case.

Formula:

Expected Estimate = (Optimistic + 4 × Most Likely + Pessimistic) / 6

Example:

* Optimistic: 3 days
* Most Likely: 5 days
* Pessimistic: 10 days
* Expected: (3 + 20 + 10) / 6 = 5.5 days

Benefits:

* Accounts for uncertainty and risk.
* Provides range, not single point.
* Useful for high-risk or complex work.

Use Cases:

* Fixed-price contracts.
* High-uncertainty initiatives.
* Stakeholder communications requiring confidence intervals.

---

## Velocity and Capacity

### Velocity

Definition:

The average number of story points a team completes per sprint.

Calculation:

Velocity = Sum of completed story points / Number of sprints

Example:

* Sprint 1: 34 points
* Sprint 2: 38 points
* Sprint 3: 36 points
* Average Velocity: 36 points/sprint

Purpose:

* Forecast future sprint capacity.
* Track team improvement over time.
* Enable release planning.

Important Notes:

* Velocity is team-specific (never compare teams).
* Velocity is a planning tool, not a performance metric.
* Velocity fluctuates—use rolling averages.
* Only count fully completed work (meets Definition of Done).

---

### Capacity

Definition:

The amount of work a team can commit to in a specific sprint, accounting for availability and known interruptions.

Calculation:

Capacity = (Team members × Available days × Focus factor) - Known interruptions

Example:

* 4 developers × 10 days × 0.7 focus = 28 ideal days
* Minus 3 days of holidays = 25 ideal days

Purpose:

* Determine realistic sprint commitments.
* Account for vacations, holidays, and meetings.
* Prevent overcommitment.

Focus Factor:

* Typical range: 0.6 to 0.8
* Accounts for meetings, interruptions, and context switching.
* Calibrate based on historical data.

---

## Estimation Best Practices

### Estimate as a Team

Principle:

The people doing the work should estimate the work.

Benefits:

* Builds shared understanding.
* Leverages diverse perspectives.
* Increases commitment to estimates.
* Surfaces hidden complexity.

---

### Use Relative Sizing

Principle:

Compare stories to each other, not to absolute time.

Benefits:

* Faster and more accurate.
* Reduces false precision.
* Accounts for team-specific factors.

---

### Re-estimate Regularly

Principle:

Estimates should be updated as understanding improves.

When to re-estimate:

* During backlog refinement.
* When requirements change.
* When new information emerges.
* Before sprint planning.

---

### Split Large Stories

Principle:

Stories larger than 13 points should be split.

Techniques:

* Split by workflow steps.
* Split by business rules.
* Split by user types.
* Split by happy path vs. edge cases.
* Split by CRUD operations.

Benefits:

* Easier to estimate accurately.
* Reduces risk of incomplete work.
* Enables more frequent delivery.

---

### Track Estimation Accuracy

Principle:

Compare estimates to actual outcomes to improve over time.

Metrics:

* Estimate vs. actual story points.
* Estimation variance by size category.
* Forecast accuracy for releases.

Benefits:

* Identifies systematic biases.
* Improves team calibration.
* Builds stakeholder trust.

---

## Common Anti-Patterns

### Management Dictates Estimates

Problem:

Managers assign estimates without team input.

Result:

* Unrealistic commitments.
* Reduced team ownership.
* Decreased morale.

Solution:

* Empower the team to estimate.
* Use estimates for planning, not performance evaluation.

---

### Estimating in Hours

Problem:

Teams estimate in hours instead of relative size.

Result:

* False precision.
* Anchoring to individual productivity.
* Inaccurate forecasts.

Solution:

* Use story points for relative sizing.
* Focus on complexity, not time.
* Track velocity for forecasting.

---

### Anchoring Bias

Problem:

First estimate influences all subsequent estimates.

Result:

* Groupthink.
* Suppression of diverse perspectives.
* Inaccurate estimates.

Solution:

* Use Planning Poker with simultaneous reveal.
* Encourage independent thinking.
* Discuss outliers openly.

---

### Treating Velocity as a Target

Problem:

Teams are pressured to increase velocity every sprint.

Result:

* Point inflation.
* Reduced quality.
* Burnout.
* Gaming the system.

Solution:

* Use velocity for planning, not performance.
* Focus on value delivery, not points.
* Celebrate sustainable pace.

---

### Estimating Without Refinement

Problem:

Teams estimate stories they don't understand.

Result:

* Wildly inaccurate estimates.
* Scope creep during sprints.
* Missed commitments.

Solution:

* Invest in backlog refinement.
* Ensure stories meet Definition of Ready.
* Clarify requirements before estimating.

---

### Ignoring Uncertainty

Problem:

Teams provide single-point estimates for uncertain work.

Result:

* Missed deadlines.
* Stakeholder disappointment.
* Loss of trust.

Solution:

* Use ranges for uncertain work.
* Apply three-point estimation.
* Communicate confidence levels.

---

## Success Criteria

Effective Agile estimation demonstrates:

* Team-based, collaborative estimation.
* Relative sizing using story points.
* Regular backlog refinement.
* Accurate velocity tracking.
* Realistic capacity planning.
* Continuous improvement in estimation accuracy.
* Stakeholder understanding of estimation uncertainty.
* Sustainable pace without point inflation.
* Split stories for better accuracy.
* Focus on value delivery over point maximization.

---

## Relationship to Planning and Forecasting

Estimation enables:

* Sprint Planning: Commit to realistic work.
* Release Planning: Forecast delivery dates.
* Capacity Planning: Account for team availability.
* Stakeholder Communication: Set expectations.
* Continuous Improvement: Track and improve accuracy.

Hierarchy:

Estimation
├── Story Points (Relative Size)
├── Velocity (Team Capacity)
├── Capacity (Sprint Availability)
└── Forecasting (Release Planning)