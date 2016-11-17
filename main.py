from __future__ import print_function, division
import sys
import csv

from cgkit_skeleton import process_bvhfile, process_bvhkeyframe
import logging

log = logging.getLogger("converter")

"""
Based on: http://www.dcs.shef.ac.uk/intranet/research/public/resmes/CS0111.pdf

Notes:
 - For each frame we have to recalculate from root
 - End sites are semi important (used to calculate length of the toe? vectors)
"""


def setup_logger(level):
    log.setLevel(level)

    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    stdout_handler.setLevel(level)

    fhandler = logging.FileHandler(
        filename='output.log', encoding='utf-8', mode='a')
    fhandler.setFormatter(fmt)

    log.addHandler(fhandler)
    log.addHandler(stdout_handler)


if __name__ == "__main__":
    setup_logger(logging.DEBUG)
    fname = sys.argv[1]
    print("Input filename: {}".format(fname))

    other_s = process_bvhfile(fname)
    for i in range(other_s.frames):
        new_frame = process_bvhkeyframe(other_s.keyframes[i], other_s.hips,
                                        other_s.dt * i)

    with open("output.csv", 'w') as f:
        writer = csv.writer(f, lineterminator="\n")
        header, frames = other_s.get_frames()
        writer.writerow(header)
        for frame in frames:
            writer.writerow(frame)
