"""fractals/fern -- Barnsley fern IFS scatter (mirrors img_scientific/fractals/fern.py)."""

_t1((x, y)) = (0.85x + 0.04y, -0.04x + 0.85y + 1.6)
_t2((x, y)) = (0.20x - 0.26y, 0.23x + 0.22y + 1.6)
_t3((x, y)) = (-0.15x + 0.28y, 0.26x + 0.24y + 0.44)
_t4((x, y)) = (0.0, 0.16y)

const _FERN_TRANSFORMS = (_t1, _t2, _t3, _t4)
const _FERN_PROBABILITIES = [0.85, 0.07, 0.07, 0.01]

"""Draw an index in 1..length(probs) with the given (unimodal) weights."""
function _pick(rng, probs)
    u, c = rand(rng), 0.0
    for (i, p) in enumerate(probs)
        c += p
        u <= c && return i
    end
    length(probs)
end

function generate_fern(num_points, rng)
    cur = (0.0, 0.0)
    xs, ys = Float64[0.0], Float64[0.0]
    for _ in 1:num_points
        cur = _FERN_TRANSFORMS[_pick(rng, _FERN_PROBABILITIES)](cur)
        push!(xs, cur[1])
        push!(ys, cur[2])
    end
    xs, ys
end

function make_fern(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    xs, ys = generate_fern(p["num_points"], rng)
    fig = Figure(resolution = (400, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    scatter!(ax, xs, ys; color = to_color(p["color"]), markersize = p["point_size"])
    fig
end

register!("fractals/fern", make_fern)
