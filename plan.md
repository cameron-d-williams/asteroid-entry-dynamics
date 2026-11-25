# Asteroid Entry Dynamics — Working Project Plan

> Status: draft / living document. Revise as experiments reveal what is worthwhile.

## 1. Purpose and scope

Independently reimplement and extend the atmospheric-entry solver from the Imperial College London MSc Applied Computational Science and Engineering Deep Impact group project. Use asteroid entry as a test case for numerical methods, high-throughput simulation, differentiable hybrid dynamics and scientific machine learning, with transferable relevance to robotics simulation and research engineering.

**Research question:** How can adaptive integration, parallel computation and differentiable simulation improve the efficiency and reliability of atmospheric-entry modelling, and can gradient-enhanced neural surrogates reduce the cost of repeated simulation?

Four core work packages:

1. Numerical integration, verification and adaptive time-stepping.
2. High-throughput CPU/GPU simulation.
3. Differentiable, event-driven physics.
4. Standard and gradient-enhanced neural surrogates.

PINNs, geographic damage modelling and learned corrections to real-world physics are outside the initial scope. No speedup or superiority of any method is assumed.

## 2. Work package 1 — Physics and numerical foundations

### 1A. Independent fixed-step baseline

- [ ] Re-derive the governing ODEs and document units, assumptions and state ordering: velocity, mass, entry angle, altitude, downrange distance, radius and spreading rate.
- [ ] Implement the original physical assumptions first, allowing a fair comparison with the coursework solver.
- [ ] Implement classical RK4 independently; separate the RHS, integrator, event handling and output sampling.
- [ ] Add altitude-dependent gravity and compare exponential, log-linear tabular and an appropriate reference atmosphere; assess each change separately.
- [ ] Represent fragmentation onset, maximum pancake radius and termination explicitly as events, with appropriate state resets and event location. Distinguish ground impact, ablation/energy cutoff, atmospheric exit and numerical failure.
- [ ] Document physical limitations, including the pancake model and treatment of mass loss and energy transfer.

### 1B. Energy deposition

The original backward finite difference is an interval-average kinetic-energy gradient, not backward Euler. RK4 integrates ODEs; it is not a differentiation scheme.

- [ ] Derive the chain-rule expression for kinetic energy `E = 0.5*m*v**2`:

  `dE/dz = (m*v*dv/dt + 0.5*v**2*dm/dt) / (dz/dt)`

- [ ] Compare backward, central and higher-order finite differences against this expression on smooth analytical profiles and numerical trajectories. Use nonuniform-grid formulas or a common grid when appropriate.
- [ ] Use the chain-rule expression as the primary pointwise diagnostic; retain interval averages as a conservative energy-accounting comparison.
- [ ] Distinguish net kinetic-energy loss from an atmospheric energy-transfer proxy (including the role of gravity and assumptions about ablated mass).
- [ ] Handle near-zero vertical velocity explicitly; consider energy loss per time or path length for grazing trajectories.
- [ ] Locate deposition peaks using sufficiently resolved or continuous trajectory output, rather than relying solely on saved sample maxima.
- [ ] Optionally integrate cumulative energy transfer as an additional state for energy-budget checks.

### 1C. Verification and validation

- [ ] Write unit tests for atmosphere interpolation, units, initial conditions, RHS and energy calculations.
- [ ] Verify against analytical drag-free and constant-density drag-only solutions.
- [ ] Demonstrate fourth-order RK4 convergence on a smooth problem; test convergence separately around events.
- [ ] Compare full trajectories and event times against a tightly converged independent SciPy solution (e.g. DOP853, with equivalent event logic).
- [ ] Test mass/velocity positivity, event ordering, radius bounds and appropriate energy accounting.
- [ ] If available, compare against the original Chelyabinsk reference profile as a limited physical validation exercise; distinguish observations from numerical reference solutions.

### 1D. Adaptive integration

- [ ] Implement adaptive RK4 step doubling to understand local error estimation.
- [ ] Implement embedded Dormand–Prince RK5(4), including scaled error norms, component-specific absolute tolerances, relative tolerances and step acceptance/rejection.
- [ ] Compare fixed and adaptive variants of the same method where practical, to isolate adaptivity from integration order.
- [ ] Keep internal timesteps independent of requested output times.
- [ ] Benchmark fixed RK4, adaptive RK4 and RK45 at matched output accuracy, using the same physics, initial conditions and event definitions.

**Deliverables:** tested reference solver; energy-deposition comparison; convergence plots; adaptive timestep visualisation; error-versus-cost curves.

**Gate:** do not optimise or generate training labels until the baseline, events and important physical outputs have demonstrated convergence.

## 3. Work package 2 — High-throughput CPU/GPU simulation

**Question:** Does reducing work per trajectory through adaptivity or executing many trajectories in parallel yield the best throughput at a given accuracy? Can the two be combined effectively?

- [ ] Learn JAX arrays, pure functions, `jit`, `vmap` and `lax` control flow.
- [ ] Port fixed and adaptive integration to JAX, retaining the verified NumPy implementation as a reference.
- [ ] Benchmark sequential CPU, compiled CPU, batched CPU and batched GPU for both fixed and adaptive stepping, as hardware permits.
- [ ] Use equivalent event handling and output summaries; avoid creating a pandas DataFrame inside each simulation.
- [ ] Separate compilation, transfer and execution costs; warm up compiled functions and synchronise device execution before timing.
- [ ] Test batch sizes, memory use, float32 versus float64, and variable integration lengths / masked work.
- [ ] Optionally investigate grouping trajectories by expected computational difficulty.
- [ ] Compare against Diffrax as an independent library implementation rather than treating it as a black box.

**Deliverables:** reproducible benchmark scripts; throughput and scaling plots; matched-accuracy comparison; hardware and software configuration records.

**Gate:** verify numerical equivalence before attributing runtime improvements to a hardware or implementation change. GPU access and FP64 performance are not assumed.

## 4. Work package 3 — Differentiable, event-driven physics

**Question:** Can derivatives of physically meaningful trajectory outputs be computed accurately and efficiently, including when physical events shift in time?

- [ ] Learn forward/reverse automatic differentiation, JVPs, VJPs and Jacobians.
- [ ] Begin with smooth dynamics; compare JAX derivatives against central finite differences across perturbation sizes and independently integrated forward sensitivity equations.
- [ ] Compute derivatives of continuous outputs with respect to radius, entry velocity, density, strength and angle; use scaled inputs/outputs when comparing sensitivities.
- [ ] Study fragmentation onset and pancake saturation as hybrid-system transitions; derive event-time sensitivities and investigate saltation/reset corrections.
- [ ] Check automatic differentiation through event root finding and adaptive integration rather than assuming it captures the intended physical derivative.
- [ ] Study grazing events, changes in event sequence and non-unique deposition peaks; flag undefined or unreliable gradients rather than forcing differentiability.
- [ ] Compare gradient accuracy and computational cost across methods.
- [ ] Perform a small synthetic inverse problem with known parameters; assess identifiability and parameter recovery.
- [ ] Compare first-order Jacobian-based uncertainty propagation with Monte Carlo on the original local ensemble.

**Deliverables:** differentiable solver; gradient verification plots; event sensitivity case studies; inverse problem and uncertainty propagation results.

**Gate:** only use gradient labels in surrogate training where their numerical accuracy and physical meaning have been checked.

## 5. Work package 4 — Neural surrogate modelling

**Question:** Does adding verified simulation gradients improve prediction accuracy, gradient fidelity or training-data efficiency sufficiently to justify their cost?

Start with scalar outputs rather than full trajectories (e.g. peak deposition, peak altitude, cumulative energy transfer, flight duration and residual mass). Keep output definitions fixed across methods.

- [ ] Generate labels from the validated solver; the supplied CSVs contain inputs, not output labels.
- [ ] Train linear/polynomial regression baselines; optionally test a Gaussian process on smaller samples.
- [ ] Train a modest standard multilayer perceptron (MLP).
- [ ] Train the same MLP architecture using both output values and verified Jacobians (gradient-enhanced / Sobolev training).
- [ ] Normalise inputs, outputs and gradient terms; tune the gradient loss weight using validation data only.
- [ ] Compare increasing training sizes (e.g. 100, 500, 1,000, 5,000, 10,000), holding test data fixed; repeat training across random seeds.
- [ ] Test local interpolation, broader-domain generalisation and event-boundary failure cases separately. Avoid gradient supervision where derivatives are undefined.
- [ ] Compare inference throughput with the fastest validated physics solver at comparable output accuracy, including data generation, gradient generation and training costs.
- [ ] Calculate amortised cost and break-even workload; report failures and tail errors, not only mean accuracy.

**Deliverables:** reproducible training pipeline; learning curves; value and gradient error distributions; accuracy–throughput and break-even plots.

**Optional extension:** trajectory surrogate or uncertainty-aware fallback to the physics solver, only if the scalar study is complete and motivates it.

## 6. Data and experimental design

| Dataset | Purpose |
| --- | --- |
| A — Original coursework ensemble (10 to 100,000 rows per supplied file) | Local uncertainty propagation, representative performance and Monte Carlo convergence |
| B — Broader experimental design | Space-filling sampling (Latin hypercube or scrambled Sobol), physically justified bounds, generalisation and workload diversity |
| C — Event-boundary stress tests | Paired perturbations near changes in fragmentation/termination regimes, gradient verification and numerical robustness |

- [ ] Audit schema, units, missing values, duplicates, overlap, distributions and correlations directly from the supplied files; record dataset provenance.
- [ ] Use the five physical input dimensions for the baseline solver. Geographical coordinates are unnecessary unless a location-dependent model is introduced.
- [ ] Preserve the original ensemble as a local uncertainty distribution, not a global asteroid population. Do not infer physical occurrence probabilities from the broader experimental design.
- [ ] Use seeded nested subsets for scaling experiments and identical scenarios for paired solver comparisons.
- [ ] Start development with 10–100 cases, accuracy/tolerance studies with representative 100–1,000 cases, and detailed analysis with up to 10,000; use 50,000–100,000 for throughput where practical. Larger synthetic ensembles are optional.
- [ ] Keep independent training, validation and test splits; reserve separate broader-domain and boundary test sets. Never tune on the test sets.
- [ ] Store one summary row per scenario, method and configuration; save full trajectories for selected diagnostic cases.

## 7. Common evaluation protocol

| Category | Measurements |
| --- | --- |
| Physical outputs | Trajectory error on common valid times/altitudes, event times, peak deposition and altitude, cumulative energy, residual mass and outcome disagreements |
| Numerical work | RHS evaluations, accepted/rejected steps, minimum timestep, solver failures |
| Performance | Wall-clock time, trajectories/s, batch size, memory, compile and transfer time, hardware and precision |
| Differentiability | Scaled Jacobian error, gradient convergence, event-time derivative error, invalid-gradient frequency |
| Surrogates | MAE/RMSE, median and 95th-percentile errors, gradient error, generalisation, training/inference cost |
| Ensemble statistics | Mean, variance, quantiles, sampling uncertainty and paired numerical bias |

Set application-relevant accuracy thresholds before the main benchmark. Compare methods at matched accuracy rather than matched timestep alone. Repeat timings and report variability, seeds, configurations and failure rates. Separate physical-model changes from numerical-method changes.

## 8. Suggested repository structure

```text
asteroid-entry-dynamics/
├── plan.md
├── README.md
├── pyproject.toml
├── src/asteroid_entry/
│   ├── physics.py
│   ├── atmosphere.py
│   ├── gravity.py
│   ├── energy.py
│   ├── events.py
│   ├── integrators/
│   ├── sensitivities/
│   └── surrogates/
├── tests/
├── notebooks/
├── experiments/
├── benchmarks/
├── data/
└── results/
```

Create modules as needed rather than scaffolding everything immediately. Check coursework data/code redistribution permissions before publishing; attribute the original group project and document independent contributions.

## 9. Learning resources

- Numerical integration: [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).
- Compilation, batching and AD: [JAX documentation](https://docs.jax.dev/).
- Differentiable ODEs: [Diffrax documentation](https://docs.kidger.site/diffrax/).
- Hybrid dynamics: [Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems](https://arxiv.org/abs/2306.06862).
- Neural networks: Equinox or another JAX-compatible library; study gradient-enhanced (Sobolev) training before implementing the second model.

## 10. Immediate next steps

- [ ] Initialise the repository and Python environment.
- [ ] Write a derivation notebook and explicitly document the baseline physical assumptions.
- [ ] Implement a pure RHS and fixed-step RK4 independently.
- [ ] Derive and test the energy gradient.
- [ ] Establish analytical tests and an independent numerical reference.
- [ ] Only then begin adaptive integration experiments.

## 11. Portfolio narrative and open questions

Provisional title: **Asteroid Entry Dynamics — High-Throughput Differentiable Simulation and Gradient-Enhanced Surrogates**.

The intended research signal is understanding of numerical verification, event-driven dynamics, automatic differentiation, parallel simulation and rigorous learned-model evaluation. The asteroid system is a useful hybrid-dynamics test case, not a full robotics contact simulator.

Open questions: achievable adaptive/GPU speedup; diversity of event sequences in the input ensemble; validity of event gradients; whether simpler surrogates outperform neural networks; whether derivative supervision pays for itself. These are experiments, not established results. Revise the scope after each work-package gate.
