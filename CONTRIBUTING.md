Contributions are highly welcomed!

Bug reports, pull requests are welcomed and invited.

Also, if you used this to produce something - please open an issue with a photo showing it (or link to a place showing it) :)

For bigger changes I strongly encourage to create an issue first to review the idea.

# License

Note that by contributing code you are licensing it to license used by this reporitory.

# Installing development dependencies

`pip install --user -e .[dev]`

(may require replacing `pip` by `pip3` on some setups)

# Detect code style issues

`pylint **/*.py --include-naming-hint=y --variable-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$ --argument-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$ --disable=C0103`

It includes a workaround for bug [#2018](https://github.com/PyCQA/pylint/issues/2018) and disables rule `C0103` with many false positives (too eager to convert variables into constants).

# Automatically reformat code to follow Python coding standards

Line length is an exception, this project allows also longer ones.

`autopep8 --max-line-length 110 --in-place --recursive .`

[PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
