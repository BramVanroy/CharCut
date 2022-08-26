import os
from collections import Counter
from html import escape
from itertools import chain


def ops2html(styled_ops, seg_id):
    for op in styled_ops:
        _, _, slice, dist, css, css_id = op
        substr_id = "seg{}_{}".format(seg_id, css_id)
        dist_str = "({:+d})".format(dist) if dist else ""
        slice_len = len(slice)
        esc_slice = escape(slice)
        yield '<span title="{css}{dist_str}: {slice_len}" class="{css} {substr_id}" ' "onmouseenter=\"enter('{substr_id}')\" onmouseleave=\"leave('{substr_id}')\">" "{esc_slice}</span>".format(
            **locals()
        )


def cand2html(ops, seg_id):
    for i, (styled_cand, _) in enumerate(ops):
        cand_id = "{}.{}".format(seg_id, i)
        yield """        <td class="compcol trg">{}</td>""".format("".join(ops2html(styled_cand, cand_id)))


def ref2html(ops, seg_id):
    for i, (_, styled_ref) in enumerate(ops):
        cand_id = "{}.{}".format(seg_id, i)
        yield """        <td class="compcol trg">{}</td>""".format("".join(ops2html(styled_ref, cand_id)))


def scores2html(score_pairs):
    for cost, div in score_pairs:
        score = (1.0 * cost / div) if div else 0
        yield """        <td class="score"><span class="detail">{:.0f}/{:.0f}= </span>{:.0%}</td>""".format(
            cost, div, score
        )


def basenames2html(idx, basename_pairs, bullets):
    # idx=0 for cand; idx=1 for ref
    cell = '        <td class="compcol seghead">{}{}</td>'
    return "\n".join(cell.format(bullets.get(pair[idx], ""), pair[idx]) for pair in basename_pairs)


def segs2html(segs, ops, score_pairs, src_basename, basename_pairs, bullets):
    """Apply highlighting on a single segment pair."""
    seg_id, origin, src, cand_refs = segs
    origin_str = '<p class="info">({})</p>'.format(origin) if origin else ""
    src_str = (
        """      <tr><td colspan="{}" class="seghead">{}</td></tr>
      <tr><td colspan="{}" class="srcrow src">{}</td></tr>""".format(
            len(ops), src_basename, len(ops), escape(src)
        )
        if src
        else "<!-- no source -->"
    )
    cand_basename_cells = basenames2html(0, basename_pairs, bullets)
    ref_basename_cells = basenames2html(1, basename_pairs, bullets)
    cand_cells = "\n".join(cand2html(ops, seg_id))
    ref_cells = "\n".join(ref2html(ops, seg_id))
    score_cells = "\n".join(scores2html(score_pairs))
    return """
<tr>
  <td class="mainrow">{seg_id}{origin_str}</td>
  <td class="mainrow">
    <table>
{src_str}
      <tr>
{cand_basename_cells}
      </tr>
      <tr>
{cand_cells}
      </tr>
      <tr>
{ref_basename_cells}
      </tr>
      <tr>
{ref_cells}
      </tr>
      <tr>
{score_cells}
      </tr>
    </table>
  </td>
</tr>""".format(
        **locals()
    )


def make_coloured_bullets(basenames):
    """
    Create a mapping between filenames and corresponding coloured HTML bullet.
    """
    # Predefined list of colours, used in turn.
    # If the filenames are more numerous, the colours are just re-used.
    colours = ["#00d000", "#d0d000", "#d000d0", "#d0d0d0", "#d00000", "#0000d0", "#00d0d0"]
    # Colour only filenames that are used at least twice
    to_colour = [name for name, count in Counter(basenames).most_common() if count > 1]
    bullet = '<span style="color:{}">&#9632;</span> '
    return {to_colour: bullet.format(colours[i % len(colours)]) for i, to_colour in enumerate(to_colour)}


def html_dump(out_file, aligned_segs, styled_ops, seg_scores, doc_costs, doc_divs, file_pair, src_file):
    """
    Apply highlighting on all segments and output them in HTML.

    aligned_segs are the input segments as returned by load_input_files().
    styled_ops are the decorated operations as returned by compare_segments().
    seg_scores are the pairs (cost, div) as returned by score_all().
    """
    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>charcut output</title>
  <style>
    body {font-family: sans-serif; font-size: 11pt;}
    table, td, th {border-spacing: 0;}
    th {padding: 10px;}
    td {padding: 5px;}
    th {border-top: solid black 2px; font-weight: normal;}
    #key {margin-left: auto; margin-right: auto; text-align: left;}
    .tophead {border-bottom: solid black 1px;}
    .src {font-style: oblique;}
    .trg {font-family: Consolas, monospace;}
    .del {font-weight: bold; color: #f00000;}
    .ins {font-weight: bold; color: #0040ff;}
    .shift {font-weight: bold;}
    .match {}
    .mainrow {border-top: solid black 1px; padding: 1em;}
    .srcrow {padding-bottom: 15px;}
    .compcol {border-left: solid lightgray 2px;}
    .seghead {color: gray; padding-bottom: 0;}
    .score {font-family: Consolas, monospace; font-size: large; text-align: center;}
    .detail {font-size: xx-small; color: gray; text-align: right;}
    .info {font-size: xx-small; color: gray;}
  </style>
  <script>
    function enter(cls) {
      var elts = document.getElementsByClassName(cls);
      for (var i=0; i<elts.length; i++)
        elts[i].style.backgroundColor = "yellow";
    }
    function leave(cls) {
      var elts = document.getElementsByClassName(cls);
      for (var i=0; i<elts.length; i++)
        elts[i].style.backgroundColor = "transparent";
    }
  </script>
</head>
<body>
<table>
<tr>
  <th class="tophead">Seg. id</th>
  <th class="tophead">
    <table id="key">
      <tr>
        <td>Segment comparison:</td>
        <td class="trg">
          <span class="del">Deletion</span><br/>
          <span class="ins">Insertion</span><br/>
          <span class="shift">Shift</span>
        </td>
      </tr>
    </table>
  </th>
</tr>"""
    print(html_top, file=out_file)
    src_basename = os.path.basename(src_file) if src_file else ""
    basename_pairs = [list(map(os.path.basename, pair.split(","))) for pair in file_pair]
    bullets = make_coloured_bullets(chain(*basename_pairs))
    prev_id = None
    for segs, ops, score_pairs in zip(aligned_segs, styled_ops, seg_scores):
        if prev_id:
            # There may be mismatches with unsafe input
            try:
                skipped = int(segs[0]) - int(prev_id) - 1
            except ValueError:
                # Some seg ids contain letters, just ignore
                skipped = None
            if skipped:
                print(
                    """
<tr>
  <td class="info" title="Mismatch - {} seg. skipped">[...]</td>
</tr>""".format(
                        skipped
                    ),
                    file=out_file,
                )

        prev_id = segs[0]
        print(segs2html(segs, ops, score_pairs, src_basename, basename_pairs, bullets), file=out_file)

    score_cell = '<td class="score"><span class="detail">{:.0f}/{:.0f}= </span>{:.0%}</td>'
    score_row = "".join(
        score_cell.format(doc_cost, doc_div, (1.0 * doc_cost / doc_div) if doc_div else 0)
        for doc_cost, doc_div in zip(doc_costs, doc_divs)
    )
    print(
        """
<tr>
  <th>Total</th>
  <th>
    <table style="width:100%"><tr>{}</tr></table>
  </th>
</tr>
</table>
</html>""".format(
            score_row
        ),
        file=out_file,
    )
