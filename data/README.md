# Research Data

## Directory structure

| Directory | Purpose |
|---|---|
| `raw/` | Original, unmodified input datasets |
| `processed/` | Cleaned data and generated simulation labels |
| `synthetic/` | Independently generated experimental scenarios |

## Original datasets

The original input datasets originate from the Deep Impact group coursework undertaken as part of the MSc Applied Computational Science and Engineering at Imperial College London.

Six datasets contain 10, 100, 1,000, 10,000, 50,000 and 100,000 initial-condition samples respectively.

### Physical parameters

| Parameter | Unit |
|---|---|
| Radius | m |
| Velocity | m/s |
| Density | kg/m³ |
| Strength | Pa |
| Entry angle | degrees from horizontal |

The datasets also contain entry latitude, longitude and bearing, which are not required by the initial atmospheric-entry solver.

## Statistical interpretation

The original datasets represent a concentrated uncertainty ensemble around a nominal asteroid-entry scenario, rather than comprehensive coverage of the physical parameter space.

Broader experimental datasets will be generated independently for generalisation, numerical robustness and event-sensitivity studies.

## Reproducibility

Future data-generation scripts will document sampling distributions, physical parameter bounds and random seeds.

## Availability

Original coursework datasets are excluded from version control pending confirmation of redistribution permissions. Generated datasets and simulation outputs are also excluded to avoid unnecessary repository size.