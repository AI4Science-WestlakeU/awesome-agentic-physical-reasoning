# Contributing

## Adding a benchmark

1. Check the three scope criteria in the README. Work outside the scope can be added to `data/out_of_scope.yaml` as an example, with its year of first release and the criterion it misses.
2. Add one record to `data/benchmarks.yaml`, following the field comments at the top of the file. Set `status: candidate` and `assessed` to the date you read the paper.
3. In `notes`, give the evidence: the physics engine or rule system, how success is decided, the action interface, the iteration budget, and the models evaluated. Quote the paper where a sentence settles a call.
4. Run `python3 scripts/build_readme.py` (needs PyYAML) and commit `README.md` and `data/benchmarks.json` together with the YAML. The script rejects values outside the vocabulary in the file headers.
5. Open the pull request. The authors of the paper review the evidence and change the status to `audited`.

## Applying the scope

Criterion 3 asks whether the benchmark itself gives LLM agents an interface for acting: text commands, tool or API calls, structured output, or code that the environment runs. The arguments may be continuous, such as target poses. An environment that takes only control signals or an action vector from a learning agent does not meet it, even when a later benchmark wraps it for LLM agents; that later benchmark is assessed on its own.

## Making a capability call

Use the definitions in the README, with these conventions. They follow the calls in Table 2 of the paper.

- **Physics-aware planning** is tested when the agent decides the order of its actions and physical consequences constrain that order: one action makes a later one possible or impossible, as when a support must stand before the load goes on, or a controller times its commands to the dynamics. It is not tested when the instruction already fixes the steps, when discrete skills abstract the dynamics away, when the result is returned whole with no order among its parts, or when building happens in game physics where blocks float. Use `partial` when only some tasks test it, when the benchmark fixes the order of operations and the agent sets only their parameters, or when a separate rule check, rather than the environment's own dynamics, scores the order.
- **Embodied execution** is tested only when the agent perceives the environment and acts in it step by step. A benchmark where the agent submits a design or a controller and a simulator runs it does not test embodied execution.
- **Functional evaluation** counts as tested only when physics decides whether the artifact performs its function. Goal-state matching, learned judges, and human preference labels are not functional verification; record them under `evaluation` as `goal-state`, `answer`, `judge`, or `mixed`.
- **Closed-loop refinement** is tested when the agent learns how a finished attempt turned out, through a simulator verdict, a score, or the simulated outcome, and revises an earlier decision such as a design, a plan, or a program. Use `partial` when the tasks require recovery from failures observed within an attempt, or when the signal reports only progress. Choosing the next action from each observation, or learning only whether the last action executed, does not count.
- **A physics check on part of the result**, such as whether a structure stays at rest under gravity while rules, geometry, or a judge decide the rest, makes `evaluation: mixed` and `FE: partial`, and `meets_standard: partial` when that check runs a realistic engine.
- **Class** follows the physics and, where a realistic engine is involved, the task: `Construction` when the agent builds an artifact, `Embodied` when it acts toward a goal, such as a target state or an answer. Symbolic state gives `Symbolic-Physical` and simplified physics gives `Simplified Sandbox`, whatever the task. A suite that mixes task forms takes the class of most of its tasks; name the other tasks in a `footnote`, which appears under the table. When those other tasks belong to another class and are scored on their own, they may also be recorded as a separate row named after the suite, such as `RLE-Bench (Construction Subset)`, with a footnote that points to the full suite. The class does not decide `meets_standard`, the Both column.

Use `partial` when a benchmark tests a capability in some tasks or in a weakened form, and `unclear` when the published text does not settle the question. Say which in `notes`.

## Re-assessing an entry

Benchmarks change between versions. To revise an existing record, update the fields, bump `assessed`, and describe the change in the pull request. Keep the old reading in the pull request description so the history stays readable.
