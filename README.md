# BVH Converter
Converts BVH file to joint location CSV and optionally joint rotation CSV using an algorithm from cgspeed/bvhplay and a BVH file parser from cgkit.

* Python 2/3 compatible

## Usage
After you install through PyPi it's very simple to use this utility. Simply open a terminal and run the following command:
```
$ bvh-converter <filename>
```
If your shell complains that "bvh-converter" could not be found, use the following instead:
```
$ python -m bvh-converter <filename>
```
If you want to output the rotations to a CSV table as well, add the `-r` or `--rotation` flag:
```
$ bvh-converter -r <filename>
```
