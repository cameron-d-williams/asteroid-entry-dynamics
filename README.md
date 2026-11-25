# Asteroid Entry Dynamics

A scientific Python project investigating numerical integration, high-throughput simulation, differentiable physics and gradient-enhanced surrogate modelling of asteroid atmospheric entry.

## Project status

Currently under active development.

## Research objectives

- Independent implementation and verification of atmospheric-entry dynamics.
- Adaptive numerical integration and error control.
- Batched CPU and GPU simulation.
- Differentiation through event-driven physical dynamics.
- Standard and gradient-enhanced neural surrogate modelling.

## Development setup

Requires Python 3.12 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run pytest
```

## Project roadmap

See [plan.md](plan.md) for the working research plan.

## Background

This project is an independent research extension of the Deep Impact group coursework undertaken as part of the MSc Applied Computational Science and Engineering at Imperial College London.
