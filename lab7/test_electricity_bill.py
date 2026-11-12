from hypothesis import given, settings, strategies as st
from electricity_bill import units_consumed, daily_average, tariff_rate, RATES, SLAB

# Anything a fuzzer might throw at the functions: text, None, numbers, lists...
anything = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers()),
)


# ---------- 1. "Must never crash" fuzz tests (arbitrary input) ----------

@given(st.text() | st.none())
def test_units_consumed_no_crash(s):
    try:
        units_consumed(s)
    except Exception as e:
        assert False, f"units_consumed crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_daily_average_no_crash(s):
    try:
        daily_average(s)
    except Exception as e:
        assert False, f"daily_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_tariff_rate_no_crash(s):
    try:
        tariff_rate(s)
    except Exception as e:
        assert False, f"tariff_rate crashed with: {e!r} for input {s!r}"


# ---------- 2. Wider type fuzzing (ints, floats, bytes, lists, ...) ----------

@given(anything)
def test_all_functions_survive_any_type(x):
    for fn in (units_consumed, daily_average, tariff_rate):
        try:
            fn(x)
        except Exception as e:
            assert False, f"{fn.__name__} crashed with: {e!r} for input {x!r}"


# ---------- 3. Correctness properties on VALID input ----------

@given(st.integers(0, 10**9), st.integers(0, 10**9))
def test_units_consumed_valid(prev, curr):
    result = units_consumed(f"{prev}:{curr}")
    if curr >= prev:
        assert result == curr - prev
    else:                       # meter can't run backwards
        assert result is None


@given(st.lists(st.integers(0, 10**6), min_size=1, max_size=50))
def test_daily_average_valid(values):
    result = daily_average(",".join(map(str, values)))
    assert result == round(sum(values) / len(values), 2)
    assert min(values) <= result <= max(values)


@given(st.sampled_from(sorted(RATES)), st.sampled_from(sorted(SLAB)),
       st.booleans())
def test_tariff_rate_valid(cat, slab, lower):
    code = f"{cat}-{slab}"
    result = tariff_rate(code.lower() if lower else code)
    assert result == RATES[cat] * SLAB[slab]


# ---------- 4. Invalid-but-structured input must be rejected (None) ----------

@given(st.text())
def test_tariff_rate_rejects_unknown_codes(s):
    valid = {f"{c}-{sl}" for c in RATES for sl in SLAB}
    if s.strip().upper() not in valid:
        assert tariff_rate(s) is None


@given(st.integers(), st.integers())
def test_units_consumed_rejects_negative(a, b):
    if a < 0 or b < 0:
        assert units_consumed(f"{a}:{b}") is None
