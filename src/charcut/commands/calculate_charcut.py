import argparse

from charcut.charcut import calculate_charcut_file_pairs


def make_base_parser():
    """Initiates a CL parser with base arguments used by standalone program and other calling modules"""
    parser = argparse.ArgumentParser(
        description="""Character-based difference
        highlighting and scoring, based on loose differences. By default, just print the document-level
        score on stdout (0~1, lower is better).""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-m", "--match-size", type=int, default=3, help="min match size in characters")
    parser.add_argument(
        "-n",
        "--alt-norm",
        action="store_true",
        help="alternative normalization scheme: use only the candidate's length for normalization",
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
        help="list of comma-separated file pairs to compare, e.g. 'mt1.txt,ref.txt mt2.txt,ref.txt mt1.txt,mt2.txt'",
    )
    return parser.parse_args()


def main():
    args = vars(parse_args())
    file_pair = args.pop("file_pair")
    src_file = args.pop("src_file")
    return calculate_charcut_file_pairs(file_pair, src_file, **args)


if __name__ == "__main__":
    main()
