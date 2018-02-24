from __future__ import print_function, division
import sys
import csv
import argparse
import os

from bvh_converter.bvhplayer_skeleton import process_bvhfile, process_bvhkeyframe

"""
Based on: http://www.dcs.shef.ac.uk/intranet/research/public/resmes/CS0111.pdf

Notes:
 - For each frame we have to recalculate from root
 - End sites are semi important (used to calculate length of the toe? vectors)
"""


def main():
    parser = argparse.ArgumentParser(
        description="Extract joint location data from BVH file format.")
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    fname = args.filename

    if not os.path.exists(fname):
        print("Error: file {} not found.".format(fname))
        sys.exit(0)
    print("Input filename: {}".format(fname))

    other_s = process_bvhfile(fname)

    print("Analyzing frames...")
    for i in range(other_s.frames):
        new_frame = process_bvhkeyframe(other_s.keyframes[i], other_s.hips,
                                        other_s.dt * i)
    print("done")

    with open("output.csv", 'w') as f:
        writer = csv.writer(f, lineterminator="\n")
        header, frames = other_s.get_frames()
        writer.writerow(header)
        for frame in frames:
            writer.writerow(frame)

    print("Output file: output.csv")


if __name__ == "__main__":
    main()
