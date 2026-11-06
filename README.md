# Images of Data Science

![code size](https://img.shields.io/github/languages/code-size/ivaquero/Images-of-Data-Science.svg)
![repo size](https://img.shields.io/github/repo-size/ivaquero/Images-of-Data-Science.svg)

A reproducible **teaching plotting toolkit** for statistics and graph-theory
charts. Every chart can be redrawn **under different parameters** from a single
specification, and the same specification drives **two independent backends** —
Python (matplotlib) and Julia (CairoMakie).

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
    SPEC --> JL["Julia backend<br/>julia/<br/>CHARTS registry → make_* (CairoMakie)"]

    PY --> O1["images/distrib/*.png"]
    JL --> O2["images/julia/distrib/*.png"]
```

The invariant for every `make_*` (in either language) is the same: parameters
are keyword-only, the defaults equal the chart's original magic numbers, and the
function **returns a figure** (no `plt.show`), so the CLI/`runall` script decides
when and where to save.

## Project Structure

```mermaid
flowchart TD
    ROOT["img-scientific/"]

    ROOT --> PKG["img_scientific/<br/>Python package"]
    ROOT --> JPKG["julia/<br/>Julia package"]
    ROOT --> IMG["images/<br/>rendered PNG gallery"]

    PKG --> INFRA["infra<br/>_io · _style · _spec<br/>_registry · _render · cli"]
    PKG --> SPECS["specs/distrib/<br/>30 language-neutral .toml"]
    PKG --> TDIST["distrib/<br/>30 spec-driven make_* modules"]
    PKG --> TPEND["graphs · metric · trials<br/>fractals · funcs · physics<br/>(standalone scripts, not yet spec-driven)"]

    JPKG --> JP["Project.toml"]
    JPKG --> JC["common.jl · charts.jl · runall.jl"]

    IMG --> IP["distrib/ · funcs/ · trials/<br/>(+ images/julia/ once instantiated)"]
```

- `img_scientific/` — the installable Python package. `_spec.py` reads the TOML
  specs, `_registry.py` provides the `@chart` decorator that maps each `id` to a
  `make_*`, and `_render.py` turns a spec into a saved PNG (lazily importing only
  the module it needs). Discovery is **spec-driven**, not by scanning imports.
- `julia/` — the Julia counterpart. `common.jl` re-reads the *same*
  `img_scientific/specs/*.toml`, `charts.jl` registers the mirrored `make_*`
  implementations, and `runall.jl` renders everything that has a Julia
  implementation and politely skips the rest.
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

### Functions & Metrics

Sigmoid, Entropy, Standard Error of Mean (SEM).

### Data-Science Trials

Central Limit Theorem, Law of Large Numbers, Convolution of Uniform Distribution,
Normal Distribution with 3 Sigmas, Normal Distribution's PDF and CDF.

### Complexity

Fractals: Sierpinski Triangle, Sierpinski Square, Koch Curve, Koch Flake.

Graphs: Erdős-Rényi, Watts-Strogatz, Barabási-Albert.

Physics: Ising Model.

## Credits

Charts by Xavier Yang ([@ivaquero](https://github.com/ivaquero)).
