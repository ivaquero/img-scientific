# Images of Data Science

![code size](https://img.shields.io/github/languages/code-size/ivaquero/Images-of-Data-Science.svg)
![repo size](https://img.shields.io/github/repo-size/ivaquero/Images-of-Data-Science.svg)

A reproducible **teaching plotting toolkit** for statistics and graph-theory
charts. Every chart can be redrawn **under different parameters** from a single
specification, and the same specification drives **two independent backends** —
Python (matplotlib) and Julia (the Makie.jl ecosystem: CairoMakie for statistical
charts, GraphMakie for graph layouts).

## Architecture

The project follows a **spec contract** design: one repository, two packages,
coordinated by a language-neutral `specs/*.toml` layer. A spec only carries the
contract — `id · title · kind · module · out · params` — and **never** any
plotting logic. Each language therefore keeps its own `id → function` mapping,
so the two backends stay in sync on *what* to draw while remaining free in *how*
they draw it.

```mermaid
flowchart LR
    SPEC["specs/*.toml<br/>single source of truth<br/>(id · title · kind · module · out · params)"]

    SPEC --> PY["Python backend<br/>img_scientific/<br/>@chart registry → make_* (matplotlib)"]
    SPEC --> JL["Julia backend<br/>julia/<br/>CHARTS registry → make_* (Makie.jl)"]

    PY --> O1["images/distrib/*.png"]
    JL --> O2["images/julia/distrib/*.png"]
```

The invariant for every `make_*` (in either language) is the same: parameters
are keyword-only, the defaults equal the chart's original magic numbers, and the
function **returns a figure** (no `plt.show`), so the CLI/`runall` script decides
when and where to save.

## Project Structure

```mermaid
flowchart LR
    ROOT["img-scientific/"]

    ROOT --> PKG["img_scientific/<br/>Python package"]
    ROOT --> JPKG["julia/<br/>Julia package"]
    ROOT --> IMG["images/<br/>rendered PNG gallery"]

    PKG --> INFRA["infra<br/>_io · _style · _spec<br/>_registry · _render · cli"]
    PKG --> SPECS["specs/&lt;topic&gt;/<br/>57 language-neutral .toml"]
    PKG --> TCHART["7 spec-driven topics<br/>distrib · funcs · physics · trials<br/>metric · fractals · graphs<br/>(make_* modules + shared helpers)"]

    JPKG --> JP["Project.toml<br/>(CairoMakie · GraphMakie · Graphs<br/>· Distributions)"]
    JPKG --> JC["common.jl (bridge)<br/>charts.jl (loader)<br/>runall.jl"]
    JPKG --> JDIST["7 topic dirs, 1:1 with Python<br/>distrib · funcs · physics · trials<br/>metric · fractals · graphs<br/>(one file per chart, self-registering)"]

    IMG --> IP["images/&lt;topic&gt;/ (Python)<br/>images/julia/&lt;topic&gt;/ (Julia)<br/>7 topics each"]
```

- `img_scientific/` — the installable Python package. `_spec.py` reads the TOML
  specs, `_registry.py` provides the `@chart` decorator that maps each `id` to a
  `make_*`, and `_render.py` turns a spec into a saved PNG (lazily importing only
  the module it needs). Discovery is **spec-driven**, not by scanning imports.
- `julia/` — the Julia counterpart, plotting on the **Makie.jl ecosystem**
  (CairoMakie for the statistical charts; GraphMakie's `graphplot` drives the
  `graphs/` topic). `common.jl` re-reads the *same*
  `img_scientific/specs/*.toml`; the chart bodies are split **one file per chart**
  under `distrib/` (mirroring `img_scientific/distrib/distrib_*.py`), each
  self-registering with `register!("distrib/<id>", ...)` — the Julia analogue of
  Python's `@chart` decorator; `charts.jl` is now just a thin loader that pulls
  in the shared `_helpers.jl` and every chart file; and `runall.jl` renders
  everything that has a Julia implementation and politely skips the rest.
- `images/` — output gallery. Python writes to `images/<topic>/`; Julia writes to
  `images/julia/<topic>/` so the two never overwrite each other.
- `python/` — leftover standalone scripts from the pre-packaging layout (kept for
  reference).

## Quick Start

Python (installs the `imgsci` command):

```bash
pip install -e .
imgsci list                     # every chart that has a spec (no plotting deps needed)
imgsci render distrib/geom_pmf  # draw one chart
imgsci render distrib/norm_pdf --set x_num=400   # override a parameter
imgsci gallery --topic distrib  # re-render a whole topic into images/
```

Julia:

```julia
cd julia
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. runall.jl     # render every chart with a Julia impl
```

## Chart Catalog

### Probability Distributions

Discrete: Bernoulli, Binomial, Geometric, Hypergeometric, Negative Binomial,
Negative Hypergeometric, Poisson, Multinomial, Categorical.

Continuous: Normal, Log-Normal, Multi-Variate Normal, 3-D Normal, Exponential,
Beta, Gamma, Laplace, Cauchy, Chi-Square, Student-t, F, Uniform, Weibull,
Dirichlet.

### Functions

Sigmoid.

### Covariance & Information Metrics

Covariance ellipse, prior × likelihood covariance product, 3-D covariance
(ellipsoid surface, scatter, marginal surface), entropy, standard error of the
mean (SEM).

### Data-Science Trials

Central Limit Theorem, Law of Large Numbers, convolution of uniforms, product of
two Gaussians, normal distribution with 3 sigmas, normal PDF and CDF.

### Fractals & Complexity

Barnsley fern, multifractal (generalized) dimensions, Koch curve, Koch
snowflake, Sierpinski squares, Sierpinski triangle, Ising model (Wolff cluster).

### Graphs & Networks

Erdős–Rényi G(n, p) and G(n, m), complete directed graph, Watts-Strogatz
rewiring, the small-world C(p)/L(p) experiment, and regular graphs.

## Credits

Charts by Xavier Yang ([@ivaquero](https://github.com/ivaquero)).
