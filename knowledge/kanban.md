# Kanban Method

## Definition

Kanban is a flow-based work management method focused on optimizing the delivery of value through a system. It improves visibility, predictability, efficiency, and continuous improvement by managing workflow rather than individual utilization.

---

## Core Principles

### Change Management Principles

* Start with the current process.
* Agree to pursue incremental and evolutionary change.
* Respect existing roles, responsibilities, and titles.
* Encourage leadership at all levels.

### Service Delivery Principles

* Understand and focus on customer needs.
* Manage work as a system.
* Improve flow continuously.
* Use data to drive decisions.

---

## Core Practices

### Visualize Workflow

Represent the actual workflow using a Kanban board.

Example:

Backlog -> Analysis -> Development -> Code Review -> Testing -> UAT -> Deployment -> Done

Guidelines:

* Workflow stages must reflect reality.
* All work should be visible.
* Blocked work should be explicitly identified.

### Limit Work In Progress (WIP)

WIP limits constrain the maximum number of work in progress items allowed in each workflow stage. WIP limits are important because they reduce multitasking and context switching, expose bottlenecks in the workflow, improve flow and flow efficiency, shorten cycle time, and increase predictability. When a column reaches its WIP limit, that stage is a bottleneck and the team swarms to finish existing work instead of starting new work.

Objectives:

* Reduce multitasking and context switching.
* Expose bottlenecks early.
* Improve flow efficiency.
* Improve predictability.

Rule:

* New work should not enter a stage when its WIP limit has been reached. Finish work before starting new work ("stop starting, start finishing").

### Manage Flow

Optimize the movement of work through the system.

Monitor:

* Queue sizes
* Waiting time
* Blocked items
* Work item age
* Throughput
* Lead time
* Cycle time

Goal:

* Maximize flow efficiency.
* Minimize delays and bottlenecks.

### Make Policies Explicit

Document workflow rules.

Examples:

* Entry criteria
* Exit criteria
* Definition of Ready
* Definition of Done
* Class of Service rules
* Escalation policies

### Implement Feedback Loops

Recommended cadences:

* Daily Kanban
* Replenishment Meeting
* Service Delivery Review
* Risk Review
* Operations Review
* Strategy Review

### Improve Collaboratively

Use empirical evidence to improve the system.

Approach:

* Measure
* Analyze
* Experiment
* Learn
* Adapt

---

## Pull System

Kanban is a pull-based system.

Rules:

* Work is pulled when capacity becomes available.
* Work should not be pushed onto individuals.
* Teams pull the highest-priority eligible work item.

Benefits:

* Reduced overload
* Faster flow
* Better predictability

---

## Workflow Boundaries

### Commitment Point

The point where the team commits to delivering a work item.

Examples:

* Ready
* Selected
* To Do

### Delivery Point

The point where value reaches the customer.

Examples:

* Production deployment
* Customer acceptance
* Service fulfillment

---

## Flow Metrics

### Lead Time

Definition:

Time elapsed between commitment point and delivery point.

Formula:

Lead Time = Delivery Date - Commitment Date

Purpose:

Measures customer-facing delivery speed.

### Cycle Time

Definition:

Time elapsed between active work start and delivery.

Formula:

Cycle Time = Delivery Date - Start Date

Purpose:

Measures workflow efficiency.

### Throughput

Definition:

Number of work items completed during a specific period.

Examples:

* 20 items per week
* 80 items per month

Purpose:

Used for forecasting.

### Work In Progress (WIP)

Definition:

Total number of active work items currently in the workflow.

Purpose:

Controls system load.

### Work Item Age

Definition:

Time an unfinished work item has spent in the workflow.

Purpose:

Identifies delivery risk and stagnation.

---

## Service Level Expectation (SLE)

Definition:

A probabilistic expectation for delivery time.

Example:

85% of Standard work items complete within 8 days.

Purpose:

* Improve predictability.
* Set stakeholder expectations.
* Detect flow degradation.

---

## Classes of Service

### Expedite

Characteristics:

* Critical urgency
* Highest priority
* Dedicated capacity
* Strict WIP control

Examples:

* Production outage
* Security incident

### Fixed Date

Characteristics:

* Delivery deadline exists

Examples:

* Compliance deadline
* Product launch

### Standard

Characteristics:

* Default work type

Examples:

* Features
* Enhancements
* Defect fixes

### Intangible

Characteristics:

* Long-term value
* Low immediate urgency

Examples:

* Documentation
* Refactoring
* Technical debt reduction

### Risk Reduction / Opportunity Enablement

Characteristics:

* Reduces future risk
* Enables future business opportunities

Examples:

* Security improvements
* Architectural modernization
* Proofs of concept

---

## Forecasting

Forecasts should be based on historical flow metrics.

Preferred inputs:

* Throughput
* Lead time distribution
* Cycle time distribution

Questions Kanban should answer:

* When is this likely to be completed?
* How much work can be completed by a target date?
* What confidence level exists for the forecast?

---

## Anti-Patterns

### Excessive WIP

Symptoms:

* Frequent context switching
* Long cycle times
* Delayed delivery

### Hidden Blockers

Symptoms:

* Work appears active but is waiting.

### Push-Based Assignment

Symptoms:

* Managers continuously assign work regardless of capacity.

### Ignoring Flow Metrics

Symptoms:

* Decisions based solely on estimates.
* No measurement of actual delivery performance.

### Optimizing Resource Utilization

Symptoms:

* Individuals remain busy.
* Overall system throughput decreases.

Preferred optimization target:

* Flow efficiency
* Delivery predictability
* Customer outcomes

---

## Success Criteria

A healthy Kanban system demonstrates:

* Visible workflow
* Explicit policies
* Controlled WIP
* Stable flow
* Predictable delivery
* Data-driven forecasting
* Continuous improvement
* Customer-focused outcomes