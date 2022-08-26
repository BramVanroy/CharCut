import argparse
import gzip

from charcut.charcut import run_on


def make_base_parser():
    """Initiates a CL parser with base arguments used by standalone program and other calling modules"""
    parser = argparse.ArgumentParser(
        description="""Character-based difference
        highlighting and scoring, based on loose differences. By default, just print the document-level
        score on stdout (0~1, lower is better)."""
    )
    parser.add_argument(
        "-m", "--match-size", type=int, default=3, help="min match size in characters (default: %(default)s)"
    )
    parser.add_argument(
        "-n",
        "--alt-norm",
        action="store_true",
        help="""alternative normalization scheme: use only the candidate's length
                             for normalization (default: %(default)s)""",
    )
    return parser


def add_parser_output_options(parser):
    """Populate a CL base parser with output options"""
    parser.add_argument(
        "-o", "--html-output-file", help="generate a html file with per-segment scores and highlighting"
    )
    parser.add_argument("-p", "--plain-output-file", help="generate a plain text file with per-segment scores only")


def parse_args():
    """Parse and return command line options."""
    parser = make_base_parser()
    add_parser_output_options(parser)
    parser.add_argument("-s", "--src_file", help="source file, only used for display")
    parser.add_argument(
        "file_pair",
        nargs="+",
        help="list of comma-separated file pairs to compare, e.g. " "mt1.txt,ref.txt mt2.txt,ref.txt mt1.txt,mt2.txt",
    )
    return parser.parse_args()


def read_gz8(filename):
    """Read a utf8, possibly gzipped, file into memory, as a list of lines."""
    opener = gzip.open if filename.endswith(".gz") else open
    with opener(filename, "rb") as f:
        return [line.decode("u8") for line in f]


def load_input_files(args):
    """
    Load input files specified in the CL arguments into memory.

    Returns a list of 4-tuples: (segment_id, origin, src_segment,
                                 [(candidate_segment, reference_segment), ...])
    "origin" is always None (present for compatibility with other modules handling sdlxliff files).
    "src_segment" is None if the source file was not passed on the CL.
    There is one (candidate_segment, reference_segment) for each positional argument on the command line.
    """
    cand_ref_file_pairs = [pair.split(",") for pair in args.file_pair]
    cand_ref_zips = [list(map(read_gz8, file_pair)) for file_pair in cand_ref_file_pairs]
    # src file is optional
    src_segs = read_gz8(args.src_file) if args.src_file else [None] * len(cand_ref_zips[0][0])
    for cand_segs, ref_segs in cand_ref_zips:
        assert len(src_segs) == len(cand_segs) == len(ref_segs)
    # Transpose lists
    cand_ref_segs = list(zip(*[list(zip(*cand_ref)) for cand_ref in cand_ref_zips]))
    return [
        (i, None, src.strip() if src else src, [(cand.strip(), ref.strip()) for cand, ref in cand_refs])
        for i, (src, cand_refs) in enumerate(zip(src_segs, cand_ref_segs), 1)
    ]


def main():
    args = parse_args()
    aligned_segs = load_input_files(args)
    run_on(aligned_segs, args)


if __name__ == "__main__":
    main()
