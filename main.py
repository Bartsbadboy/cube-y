"""Fill the box, show the search moving, judge the result, save it.

    python main.py                      the 5 x 5 x 5 cube
    python main.py --box 10x5x1         another box
    python main.py --check FILE         judge a saved solution again

Exit code: 0 a valid solution, 1 no solution, 2 the judge refused it,
3 stopped by hand.
"""

import argparse
import sys
from pathlib import Path

from board import Board
from candidates import build_table
from checker import check
from display import layers, parse
from geometry import Box
from search import Stats, solve

FOUND, IMPOSSIBLE, REFUSED, STOPPED = 0, 1, 2, 3


def parse_box(text):
    try:
        nx, ny, nz = (int(n) for n in text.lower().split("x"))
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected NXxNYxNZ, like 5x5x5, got {text!r}")
    return Box(nx, ny, nz)


def box_name(box):
    return f"{box.nx}x{box.ny}x{box.nz}"


def progress_line(stats, board):
    rate = stats.placed / stats.elapsed if stats.elapsed else 0
    return (f"{stats.elapsed:8.1f} s · posées {stats.placed:,} · retirées {stats.removed:,}"
            f" · impasses {stats.dead_ends:,} · en place {len(board.stack)}"
            f" · record {stats.deepest} · {rate:,.0f} poses/s").replace(",", " ")


def judge(cells, box, out):
    errors = check(cells, (box.nx, box.ny, box.nz))
    if errors:
        print("Le juge refuse :", file=out)
        for e in errors:
            print(f"  - {e}", file=out)
        return REFUSED
    print("Le juge valide.", file=out)
    return FOUND


def run(box, solution_file, every, out):
    table = build_table(box)
    board = Board(box)
    stats = Stats(report=lambda s, b: print(progress_line(s, b), file=out, flush=True),
                  every=every)
    print(f"Boîte {box_name(box)} : {box.size} cases, "
          f"{sum(len(t) for t in table)} candidats.", file=out, flush=True)
    try:
        found = solve(board, table, stats)
    except KeyboardInterrupt:
        print(progress_line(stats, board), file=out)
        print("Arrêté à la main. Là où on en était :", file=out)
        print(layers(board.cells, box), file=out)
        return STOPPED
    print(progress_line(stats, board), file=out)
    if not found:
        print("Aucune solution : toutes les branches ont été essayées.", file=out)
        return IMPOSSIBLE
    text = layers(board.cells, box)
    print(text, file=out)
    verdict = judge(board.cells, box, out)
    if verdict == FOUND:
        solution_file.parent.mkdir(parents=True, exist_ok=True)
        solution_file.write_text(text, encoding="utf-8")
        print(f"Solution écrite dans {solution_file}", file=out)
    return verdict


def main(argv=None, out=sys.stdout):
    parser = argparse.ArgumentParser(description="Remplir une boîte avec des pentominos Y.")
    parser.add_argument("--box", type=parse_box, default=Box(5, 5, 5),
                        help="dimensions, par exemple 5x5x5 (par défaut)")
    parser.add_argument("--out", type=Path,
                        help="fichier de solution (par défaut solutions/<boîte>.txt)")
    parser.add_argument("--every", type=int, default=1_000_000,
                        help="une ligne d'avancement toutes les N pièces posées")
    parser.add_argument("--check", type=Path, metavar="FILE",
                        help="rejuger une solution sauvée, sans chercher")
    args = parser.parse_args(argv)

    if args.check:
        cells = parse(args.check.read_text(encoding="utf-8"), args.box)
        return judge(cells, args.box, out)
    solution_file = args.out or Path("solutions") / f"{box_name(args.box)}.txt"
    return run(args.box, solution_file, args.every, out)


if __name__ == "__main__":
    # Accents survive a redirected output on Windows too.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
