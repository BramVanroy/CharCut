from pathlib import Path

from charcut.charcut import calculate_charcut_file_pairs


def test_cli_default_kwargs(example_corpus):
    curr_dir = Path(__file__).parent.resolve()

    # The files here contain the same lines as the data in example_corpus!
    # File_pair is expected to be a list of X,Y strings
    file_pair = [",".join(map(str, [curr_dir / "hyps.txt", curr_dir / "refs.txt"]))]
    src_file = None
    charcut_score, num_seqs = calculate_charcut_file_pairs(file_pair, src_file)

    assert abs(charcut_score - example_corpus["charcut"]) < 0.00000001
    assert num_seqs == len(example_corpus["ref"]) == len(example_corpus["hyp"])
