from charcut import calculate_charcut


def test_example_saudis(example_saudis):
    hyp = example_saudis["hyp"]
    ref = example_saudis["ref"]
    result = calculate_charcut(hyp, ref)

    assert abs(result[0] - example_saudis["charcut"]) < 0.00000001


def test_example_estimate(example_estimate):
    hyp = example_estimate["hyp"]
    ref = example_estimate["ref"]
    result = calculate_charcut(hyp, ref)

    assert abs(result[0] - example_estimate["charcut"]) < 0.00000001