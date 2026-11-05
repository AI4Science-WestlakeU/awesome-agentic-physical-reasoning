<h1><img src="assets/awesome-apr-banner.png" alt="Awesome APR. Agentic Physical Reasoning" width="100%"></h1>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![NeurIPS 2026](https://img.shields.io/badge/NeurIPS%202026-Position%20Paper%20Track-6C3483)](https://neurips.cc/virtual/2026/poster/140116)
[![Project page](https://img.shields.io/badge/Project%20page-APR-1F6FEB)](https://ai4science-westlakeu.github.io/APR/)
[![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-lightgrey)](scripts/LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-2EA44F)](CONTRIBUTING.md)

A living audit of agentic physical reasoning (APR) benchmarks, which test LLM agents that act under physics.

Companion to the NeurIPS 2026 position paper *Evaluating Physical Reasoning in LLM Agents Requires Construction Benchmarks* ([project page](https://ai4science-westlakeu.github.io/APR/) · [OpenReview](https://openreview.net/forum?id=42PVaAYxLX)). The paper audits 11 benchmarks against one standard and five capabilities. This repository keeps that audit current after the paper is frozen: new benchmarks are assessed against the same standard and capabilities and added through issues and pull requests.

## The standard

An evaluation of physical reasoning must meet two minimum requirements.

1. **Functional verification.** Physics judges the outcome. The artifact the agent produces, such as a structure or a machine, works or it does not.
2. **Realistic physics.** Gravity, friction, and collision constrain every action along the way.

Together they form one standard. It prescribes no kind of task; in the audit so far, every benchmark that meets it is a construction benchmark, in which the agent builds an artifact. The audit also tracks five capabilities along the agent's loop from goal to verified artifact.

| Capability | Tests whether the agent can |
|---|---|
| **Goal-driven design** (GDD) | generate a solution from a functional specification rather than follow given step-by-step instructions |
| **Physics-aware planning** (PAP) | generate action sequences that obey physical constraints, anticipating how each action affects future states |
| **Embodied execution** (EE) | act in an environment with realistic physics while perceiving the state to inform actions |
| **Functional evaluation** (FE) | anticipate whether an artifact achieves its intended function, beyond receiving post-hoc verification |
| **Closed-loop refinement** (CLR) | receive evaluation signals, detect when goals are not achieved, and adapt upstream decisions |

The five are an initial taxonomy, and this repository is where it evolves.

## Scope

The audit has a fixed scope, the same as the paper's (Section 3.2). A benchmark enters the audit when it meets all three criteria.

1. LLM agents can be evaluated on it and interact with it.
2. Its environment is governed by physical dynamics, from symbolic rules to a rigid-body or richer engine.
3. It provides at least a text or API action interface for perceiving state and issuing commands, regardless of observation modality.

<!-- OUT_OF_SCOPE:START -->
<details>
<summary><b>Out-of-scope examples</b> (not exhaustive)</summary>

Related work outside the scope, grouped by the criterion it misses. Most examples come from Section 3.2 and Appendix B of the paper.

| Example | What it evaluates | Paper |
|---|---|---|
| **No interactive physics environment** · criterion 1 or 2 | | |
| Physion | Predicting physical outcomes from videos | [paper](https://openreview.net/forum?id=CXyZrKPz4CU) |
| Physion++ | Inferring physical properties from videos | [paper](https://openreview.net/forum?id=5Exz7eaBXH) |
| ComPhy | Compositional physical reasoning about objects and events in videos | [paper](https://openreview.net/forum?id=PgNEYaIc81Q) |
| CLEVR | Visual question answering on rendered scenes | [paper](https://doi.org/10.1109/cvpr.2017.215) |
| IntPhys 2 | Judging whether videos are physically possible | [paper](https://arxiv.org/abs/2506.09849) |
| GRASP | Language grounding and situated physics understanding in videos | [paper](https://doi.org/10.24963/ijcai.2024/696) |
| PhyBlock | Block assembly plans, scored against annotations and never executed in a simulator | [paper](https://openreview.net/forum?id=z6WfQ43sHr) |
| SWE-bench | Resolving GitHub issues | [paper](https://openreview.net/forum?id=VTF8yNQM66) |
| WebArena | Tasks on websites | [paper](https://openreview.net/forum?id=oKn9c6ytLx) |
| OSWorld | Tasks in real computer environments | [paper](https://openreview.net/forum?id=tN61DTr4Ed) |
| AgentBench | LLM agents across software, game, and web environments | [paper](https://openreview.net/forum?id=zAdUB0aCTQ) |
| GAIA | Questions for general AI assistants | [paper](https://openreview.net/forum?id=fibxvahvs3) |
| ToolBench | Using real-world APIs | [paper](https://openreview.net/forum?id=dHng2O0Jjr) |
| PhysReason | Physics problem solving, scored against reference answers and solution steps | [paper](https://doi.org/10.18653/v1/2025.acl-long.811) |
| PHYBench | Physics problem solving, scored against reference answers | [paper](https://doi.org/10.52202/085713-0044) |
| UGPhysics | Undergraduate physics problem solving, scored against reference answers | [paper](https://openreview.net/forum?id=EmLiyZGvrR) |
| PhyX | Physics problem solving with images, scored against reference answers | [paper](https://arxiv.org/abs/2505.15929) |
| VSI-Bench | Spatial question answering over videos | [paper](https://doi.org/10.1109/cvpr52734.2025.00994) |
| 3DSRBench | 3D spatial question answering over images | [paper](https://doi.org/10.1109/iccv51701.2025.00651) |
| SAT | Spatial question answering on simulated scenes | [paper](https://openreview.net/forum?id=DW8U8ZWa1U) |
| STI-Bench | Spatiotemporal question answering over videos | [paper](https://doi.org/10.1109/iccv51701.2025.00533) |
| Physics-IQ | Video continuations from generative models, compared with real recordings | [paper](https://doi.org/10.1109/wacv61042.2026.00099) |
| Cosmos-Reason1 | Yes-or-no and multiple-choice questions about videos of robots and driving | [paper](https://arxiv.org/abs/2503.15558) |
| EngDesign | Engineering design answers, scored by task scripts that sometimes run domain simulators | [paper](https://openreview.net/forum?id=Wmsnx7EPel) |
| SciLaws-Bench | Scientific law discovery from fixed data or from queries to a simulator that returns a hidden formula plus noise | [paper](https://arxiv.org/abs/2609.01552) |
| MaD Physics | Choosing measurements of simulated physical systems that the agent cannot act on, scored by predictions of later states | [paper](https://arxiv.org/abs/2605.10820) |
| **No text-based interaction interface** · criterion 3 | | |
| FurnitureBench | Long-horizon furniture assembly by a robot arm | [paper](https://doi.org/10.1177/02783649241304789) |
| IKEA Furniture Assembly | Long-horizon furniture assembly in simulation | [paper](https://doi.org/10.1109/icra48506.2021.9560986) |
| RAMP | Robotic assembly manipulation and planning | [paper](https://doi.org/10.1109/lra.2023.3330611) |
| Break and Make | Interactive structural understanding with LEGO bricks | [paper](https://doi.org/10.1007/978-3-031-19815-1_6) |
| DeepMind Control Suite | Continuous control tasks | [paper](https://arxiv.org/abs/1801.00690) |
| HumanoidBench | Whole-body humanoid locomotion and manipulation | [paper](https://doi.org/10.15607/rss.2024.xx.061) |
| Meta-World | Multi-task and meta reinforcement learning on tabletop manipulation | [paper](https://proceedings.mlr.press/v100/yu20a.html) |
| SoftGym | Deformable object manipulation | [paper](https://proceedings.mlr.press/v155/lin21a.html) |
| CARLA | Urban driving | [paper](https://proceedings.mlr.press/v78/dosovitskiy17a.html) |
| PHYRE | 2D physics puzzles solved by placing balls, one continuous action vector per attempt for learning agents | [paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/4191ef5f6c1576762869ac49281130c9-Paper.pdf) |
| **Not evaluation suites** · methods and generators | | |
| BrickGPT | Generating physically stable and buildable brick structures from text | [paper](https://doi.org/10.1109/iccv51701.2025.01373) |
| Assemble Them All | Physics-based assembly planning by disassembly | [paper](https://doi.org/10.1145/3550454.3555525) |
| MatchMaker | Automated asset generation for robotic assembly | [paper](https://doi.org/10.1109/icra55743.2025.11128440) |
| RoboGen | Generative simulation of tasks and data for robot learning | [paper](https://openreview.net/forum?id=SQIDlJd3hN) |

</details>
<!-- OUT_OF_SCOPE:END -->

## Audit

How to read the tables:

- **Class** names the task: Symbolic-Physical, symbolic state · Simplified Sandbox, simplified physics · Construction, building artifacts · Embodied, acting toward goals or answers. Construction and Embodied need a realistic engine for at least part of the benchmark, and the Physics column says how much. A suite that mixes kinds of task takes the class of most of its tasks.
- **Capabilities**: the five above. ✓ tested · ✗ not tested · ◐ tested in some tasks or in a weaker form · ? unclear from the published text.
- **Physics**: `symbolic` rule-based state · `simplified` gravity, friction, or collision left out · `realistic` a rigid-body or richer engine, 2D included · `partial` physics in only some tasks or some checks.
- **Evaluation**: `functional` physics tests the function · `goal-state` final state against goal conditions · `answer` against reference answers · `judge` a model or a human scores · `mixed` more than one.
- **Both**: the two minimum requirements together; ◐ when physics checks only part of the result. The class does not decide it, so a construction benchmark can still miss it.
- **Year**: first release. A dash in Code means no public code was found.

<!-- AUDIT:START -->
**In the paper** (Table 2, 11 benchmarks, 2 meet both requirements). Assessed in January 2026; BuildArena re-assessed in October 2026.

| Benchmark | Year | GDD | PAP | EE | FE | CLR | Physics | Evaluation | Both | Paper | Code |
|---|---|:-:|:-:|:-:|:-:|:-:|---|---|:-:|---|---|
| **Construction** · realistic physics, building artifacts | | | | | | | | | | | |
| BesiegeField | 2025 | ✓ | ✓ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2510.14980) | [code](https://github.com/Godheritage/BesiegeField) |
| BuildArena | 2025 | ✓ | ✓ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2510.16559) | [code](https://github.com/AI4Science-WestlakeU/BuildArena) |
| **Embodied** · realistic physics, acting toward goals | | | | | | | | | | | |
| EmbodiedBench | 2025 | ✗ | ✗ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2502.09560) | [code](https://github.com/EmbodiedBench/EmbodiedBench) |
| PARTNR | 2024 | ✗ | ✗ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2411.00081) | [code](https://github.com/facebookresearch/partnr-planner) |
| **Simplified Sandbox** · simplified physics | | | | | | | | | | | |
| MineAnyBuild | 2025 | ✓ | ✗ | ✗ | ✗ | ✗ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2505.20148) | [code](https://github.com/MineAnyBuild/MineAnyBuild) |
| Minecraft Builder Dialog | 2024 | ✓ | ✗ | ✗ | ✗ | ✗ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2407.12734) | — |
| Plancraft | 2024 | ✗ | ✗ | ✗ | ✗ | ✓ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2412.21033) | [code](https://github.com/gautierdag/plancraft) |
| TeamCraft | 2024 | ✓ | ✗ | ✗ | ✗ | ✗ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2412.05255) | [code](https://github.com/teamcraft-bench/teamcraft) |
| MineDojo | 2022 | ✗ | ✗ | ✗ | ✗ | ✓ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2206.08853) | [code](https://github.com/MineDojo/MineDojo) |
| **Symbolic-Physical** · symbolic state | | | | | | | | | | | |
| ScienceWorld | 2022 | ✗ | ✓ | ✗ | ✗ | ✗ | symbolic | goal-state | ✗ | [paper](https://arxiv.org/abs/2203.07540) | [code](https://github.com/allenai/ScienceWorld) |
| ALFWorld | 2020 | ✗ | ✗ | ✗ | ✗ | ✗ | symbolic | goal-state | ✗ | [paper](https://arxiv.org/abs/2010.03768) | [code](https://github.com/alfworld/alfworld) |

**Candidates** (30). Assessed from the published texts, pending review by the paper's authors. The evidence for each judgment is in `data/benchmarks.yaml`.

| Benchmark | Year | GDD | PAP | EE | FE | CLR | Physics | Evaluation | Both | Paper | Code |
|---|---|:-:|:-:|:-:|:-:|:-:|---|---|:-:|---|---|
| **Construction** · realistic physics, building artifacts | | | | | | | | | | | |
| ArtifactArena | 2026 | ✓ | ✓ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2610.06511) | [code](https://github.com/ArtifactArena/harness-public) |
| BrickBench | 2026 | ✓ | ✗ | ✗ | ◐ | ✓ | partial | mixed | ◐ | [paper](https://arxiv.org/abs/2610.12452) | [code](https://github.com/kulits/BrickAgent) |
| FunCADBench | 2026 | ✓ | ◐ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2610.26861) | [code](https://github.com/thegenlab/fun-CAD-harness) |
| LMBuild | 2026 | ✓ | ◐ | ✗ | ◐ | ✓ | partial | mixed | ◐ | [paper](https://arxiv.org/abs/2610.04292) | [code](https://github.com/Lumos-Jiateng/LMBuild) |
| PACE-Bench | 2026 | ✓ | ✓ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2608.14441) | [code](https://github.com/thunlp/PACE-Bench) |
| PolyBridgeBench | 2026 | ✓ | ✗ | ✗ | ✓ | ✓ | realistic | functional | ✓ | [paper](https://arxiv.org/abs/2609.21493) | — |
| **Embodied** · realistic physics, acting toward goals | | | | | | | | | | | |
| CaP-X | 2026 | ✗ | ◐ | ◐ | ✗ | ✓ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2603.22435) | [code](https://github.com/capgym/cap-x) |
| CodeActionBench | 2026 | ✗ | ◐ | ✓ | ✗ | ✓ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2609.33807) | [code](https://github.com/lyhkk/CodeActionBench) |
| ESI-Bench | 2026 | ✗ | ◐ | ✓ | ✗ | ✗ | realistic | answer | ✗ | [paper](https://arxiv.org/abs/2605.18746) | [code](https://github.com/ESI-Bench/ESI-Bench) |
| ESPIRE | 2026 | ✗ | ✗ | ✓ | ✗ | ◐ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2603.13033) | [code](https://github.com/spatigen/espire) |
| Embodied Agent Arena | 2026 | ✗ | ◐ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2610.00854) | [code](https://github.com/embodied-agent-arena/embodied-agent-arena) |
| Embodied Playground | 2026 | ◐ | ✓ | ✓ | ◐ | ◐ | realistic | mixed | ◐ | [paper](https://arxiv.org/abs/2610.27039) | [code](https://github.com/Winniechen2002/Embodied-Playground) |
| EmbodiedMemory-Bench | 2026 | ✗ | ✗ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2609.28236) | [code](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_memory) |
| EvoPolicyGym | 2026 | ✗ | ◐ | ✗ | ✗ | ✓ | partial | mixed | ✗ | [paper](https://arxiv.org/abs/2607.02440) | [code](https://github.com/Linzwcs/EvoPolicyGym) |
| HumanCLAW-Bench | 2026 | ✗ | ✗ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2607.27180) | [code](https://github.com/Human-CLAW/HumanCLAW) |
| LIBERO-Agent | 2026 | ✗ | ◐ | ✓ | ✗ | ◐ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2609.39507) | [code](https://github.com/dzj441/Libero-Agent) |
| PhysMent | 2026 | ✗ | ◐ | ✓ | ✗ | ✗ | realistic | answer | ✗ | [paper](https://arxiv.org/abs/2609.13152) | [code](https://github.com/DRJCompSciWiz/PhysMent---An-Interactive-Approach-For-LLM-Reasoning-In-Physics-Problems) |
| RLE-Bench<sup>[1]</sup> | 2026 | ◐ | ◐ | ◐ | ◐ | ✓ | realistic | mixed | ◐ | [paper](https://arxiv.org/abs/2609.34210) | [code](https://github.com/RLE-Bench/RLE-Bench) |
| ReactHuman | 2026 | ✗ | ◐ | ✗ | ✗ | ✗ | realistic | answer | ✗ | [paper](https://arxiv.org/abs/2609.10895) | — |
| RoboDojo + RoboProbe | 2026 | ✗ | ◐ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2609.24170) | [code](https://github.com/RoboProbe/RoboProbe) |
| RoboQuest | 2026 | ✗ | ◐ | ✓ | ✗ | ◐ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2610.10388) | [code](https://github.com/declare-lab/RoboQuest) |
| SpatialWorld | 2026 | ✗ | ✗ | ✓ | ✗ | ✗ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2606.09669) | [code](https://github.com/Hongcheng-Gao/SpatialWorld) |
| VABench | 2026 | ✗ | ◐ | ✓ | ✗ | ◐ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2609.19554) | [code](https://github.com/zhangzhongbo2213/VABench) |
| DeepPHY | 2025 | ✗ | ✓ | ✓ | ✗ | ✓ | realistic | goal-state | ✗ | [paper](https://arxiv.org/abs/2508.05405) | [code](https://github.com/XinrunXu/DeepPHY) |
| **Simplified Sandbox** · simplified physics | | | | | | | | | | | |
| DiscoverPhysics | 2026 | ✗ | ✗ | ✗ | ✗ | ✓ | simplified | mixed | ✗ | [paper](https://arxiv.org/abs/2605.26087) | [code](https://github.com/SampsonML/DiscoverPhysics) |
| Mine Odyssey | 2026 | ✗ | ✗ | ✗ | ✗ | ✓ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2610.11328) | [code](https://github.com/hkust-nlp/MineOdyssey) |
| MineCEraft | 2026 | ✓ | ◐ | ✗ | ◐ | ✗ | simplified | mixed | ✗ | [paper](https://arxiv.org/abs/2608.28884) | [code](https://github.com/SewoongLee/mineCEraft) |
| MineExplorer | 2026 | ✗ | ✗ | ✗ | ✗ | ✗ | simplified | goal-state | ✗ | [paper](https://arxiv.org/abs/2605.30931) | [code](https://github.com/meituan-longcat/MineExplorer) |
| VLATIM | 2026 | ◐ | ✗ | ✗ | ✗ | ✗ | simplified | mixed | ✗ | [paper](https://arxiv.org/abs/2605.11223) | [code](https://github.com/Marco2929/FMVLATIMBench) |
| **Symbolic-Physical** · symbolic state | | | | | | | | | | | |
| MECoBench | 2026 | ✗ | ✗ | ✗ | ✗ | ◐ | symbolic | goal-state | ✗ | [paper](https://arxiv.org/abs/2606.31966) | [code](https://github.com/q-i-n-g/MECoBench) |

<details>
<summary><sub>Notes (1)</sub></summary>

<sub>[1] RLE-Bench mixes task forms and takes the class of most of its 51 tasks, which are robot control, policy development, and perception. Four of its tasks are construction scored by physics in simulation. In them the agent builds a tower and a cantilever with a robot arm, designs a mobile base, and designs gravity compensation for a leader arm.</sub>

</details>
<!-- AUDIT:END -->

## Add a benchmark

Open an issue with the [*New benchmark*](../../issues/new?template=new-benchmark.yml) template, or send a pull request that adds a record to [`data/benchmarks.yaml`](data/benchmarks.yaml), or an out-of-scope example to [`data/out_of_scope.yaml`](data/out_of_scope.yaml), and runs `python3 scripts/build_readme.py`. New records enter as candidates and move to the audited tables once the paper's authors review the evidence. [CONTRIBUTING.md](CONTRIBUTING.md) lists the fields and the conventions for each judgment.

## Changelog

- 2026-11-05 · 24 candidates added, three of them released before the paper's submission but not in its audit (DeepPHY, ESPIRE, CaP-X). Out-of-scope examples listed under Scope. Classes follow physics and task.
- 2026-10-14 · Six candidates assessed from texts released after the paper's audit (ArtifactArena, PACE-Bench, PolyBridgeBench, RLE-Bench, LMBuild, BrickBench). BuildArena re-assessed on its later version, whose optional closed-loop protocol tests closed-loop refinement.
- 2026-01-29 · Initial audit: the 11 benchmarks of Table 2 in the paper.

## Citation

```bibtex
@inproceedings{deng2026construction,
  title     = {Evaluating Physical Reasoning in {LLM} Agents Requires Construction Benchmarks},
  author    = {Deng, Wenhao and Xia, Tian and Jiang, Yuru and Jose, Joemon M. and Wu, Tailin},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS), Position Paper Track},
  year      = {2026}
}
```

## License

The audit data and text are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The scripts are released under the MIT License (see [`scripts/LICENSE`](scripts/LICENSE)).
