from charcut import calculate_charcut


def test_corpus(example_corpus):
    hyps = example_corpus["hyp"]
    refs = example_corpus["ref"]
    result = calculate_charcut(hyps, refs)

    assert abs(result[0] - example_corpus["charcut"]) < 0.00000001
