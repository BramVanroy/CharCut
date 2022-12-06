# CharCut
Character-based MT evaluation and difference highlighting

CharCut compares outputs of MT systems with reference translations. It can compare multiple file pairs simultaneously and produce HTML outputs showing character-based differences along with scores that are directly inferred from the lengths of those differences, thus making the link between evaluation and visualisation straightforward.

The matching algorithm is based on an iterative search for longest common substrings, combined with a length-based threshold that limits short and noisy character matches. As a similarity metric this is not new, but to the best of our knowledge it was never applied to highlighting and scoring of MT outputs. It has the neat effect of keeping character-based differences readable by humans.

Accidentally, the scores inferred from those differences correlate very well with human judgments, similarly to other great character-based metrics like [chrF(++)](https://github.com/m-popovic/chrF) or [CharacTER](https://github.com/rwth-i6/CharacTER). It was evaluated here:
> Adrien Lardilleux and Yves Lepage: "CharCut: Human-Targeted Character-Based MT Evaluation with Loose Differences". In [Proceedings of IWSLT 2017](http://workshop2017.iwslt.org/64.php).

It is intended to be lightweight and easy to use, so the HTML outputs are, and will be kept, slick on purpose.

Note (Bram Vanroy): the remainder of this README has been changed to reflect the changes I have made to make the package more usable from a Python package perspective,
e.g., by using hypotheses/references directly without files. 

## Installation

```shell
pip install charcut
```

This will install the command `calculate-charcut`.


Basic usage:
```shell
calculate-charcut cand.txt,ref.txt
```
where `cand.txt` and `ref.txt` contain corresponding candidate (MT) and reference (human) segments, 1 per line. Multiple file pairs can be specified on the command line: candidates with references, candidates with other candidates, etc.
By default, only document-level scores are displayed on standard output. To produce an HTML output file, use the `-o` option:

```shell
calculate-charcut cand.txt,ref.txt -o mydiff.html
```

A few more options are available; call
```shell
calculate-charcut -h
```
to list them.

Consider lowering the `-m` option value (minimum match size) for non-alphabetical writing systems such as Chinese or Japanese. The default value (3 characters) should be acceptable for most European languages, but depending on the language and data, larger values might produce better looking results.

## Modifications by Bram Vanroy

Bram Vanroy made some changes to this package that do not affect the result of the metric but that should improve usability. He also packaged the library for pip and added some tests to ensure the same results with the original library. Code has been rewritten to make it easier to use from within Python without the need of files as input. In Python, the following entry point now exists:

```python
def calculate_charcut(
    hyps: Union[str, List[str]],
    refs: Union[str, List[str]],
    html_output_file: str = None,
    plain_output_file: str = None,
    src_file: str = None,
    match_size: int = 3,
    alt_norm: bool = False,
    verbose: bool = False
) -> Tuple[float, int]:
```

where `hyps` and `refs` are indiviual sentences `str` or a list of sentences `List[str]`. This function has the same capabilities and arguments as the command-line script that is available (discussed above). This command line script is now available as an installed entry point rather than a separate Python script. You can call that from the command line with `calculate-charcut`.

## License

[GPLv3](LICENSE)