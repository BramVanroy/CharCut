from pytest import fixture


@fixture
def example_saudis():
    return {"hyp": "this week the saudis denied information published in the new york times",
            "ref": "saudi arabia denied this week information published in the american new york times",
            "charcut": 0.20915032679738563}


@fixture
def example_estimate():
    return {"hyp": "this is in fact an estimate",
            "ref": "this is actually an estimate",
            "charcut": 0.16363636363636364}


@fixture
def example_corpus():
    return {"hyp": ["this week the saudis denied information published in the new york times", "this is in fact an estimate"],
            "ref": ["saudi arabia denied this week information published in the american new york times", "this is actually an estimate"],
            "charcut": 0.1971153846153846}
