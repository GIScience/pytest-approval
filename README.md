# README

A simple approval test library utilizing external diff programs such as
PyCharm and Visual Studio Code to compare approved and received output.

## About

Approval tests capture the output (a snapshot) of a piece of code and compare it
with a previously approved version of the output.

It's most useful in environments where frequent changes are expected or where
the output is of a complex nature but can be easily verified by humans, aided for
example by a diff-tool or a visual representation of the output.

Once the output has been *approved* then as long as the output stays the same
the test will pass. A test fails if the *received* output is not identical to
the approved version. In that case, the difference between the received and the
approved output is reported to the tester.

For outputs that can be represented by text, a report can be as simple as
printing the difference to the terminal. Using diff programs with a graphical
user interface such as PyCharm or Visual Studio Coder as *reporter* not
only helps to visualize the difference, but they can also be used as *approver*
by applying the changes of the received output to the approved output.

Not all data can or should be represented by text. In many cases an
image is the best and most easily verifiable representation.
PyCharm and Visual Studio Code can work with images as well.

> A picture’s worth a 1000 tests ([approvaltests.com](https://approvaltests.com/)).


## Requirements

OS
- Linux/Unix
- MacOS

One of following programs installed:
- PyCharm
- Visual Studio Code
- Meld
- GNU Diffutils (`diff`)


## Installation

```sh
uv add git+https://github.com/GIScience/asyncpg-recorder.git
```


## Usage

Verify text:

```python
from pytest_approval import verify, verify_json


def test_verify_string()
    assert verify("Hello World!")


def test_verify_dict()
    # automatic conversion to JSON
    assert verify_json({"msg": "Hello World!"})
```


Verify binary files such as an image:

```python
from pytest_approval import  verify_binary


def test_verify_binary(image):
    with open("my_image.jpg", "rb") as file:
        buffer = file.read()
    assert verify_binary(buffer, extension=".jpg")
```

If you want to save the approved files in a specific directory, set the variable approved-dir in your pyproject.toml.
The path should be relative to pyproject.toml.

```toml
[tool.asyncpg-recorder]
"approved-dir"="tests/approved"
```

To automatically approve all results, set the flag --auto_approve.

```shell
uv run pytest --auto-approve
```

<!-- ## Configuration -->
<!---->
<!-- ### Approver/Reporter -->
<!---->
<!-- Per default `pytest-approval` tries a list of diff programs as reporters until a working one is found. -->
<!---->
<!-- You can provide your own list in the `pyproject.toml` file: -->
<!---->
<!-- ```toml -->
<!-- [tool.pytest-approval] -->
<!-- reporters = [ -->
<!--     [ -->
<!--         "meld", -->
<!--         "%received", -->
<!--         "%approved", -->
<!--     ], -->
<!--     [ -->
<!--         "diff", -->
<!--         "--unified", -->
<!--         "--color", -->
<!--         "--suppress-common-lines", -->
<!--         "--label", -->
<!--         "received", -->
<!--         "--label", -->
<!--         "approved", -->
<!--         "%received", -->
<!--         "%approved", -->
<!--     ], -->
<!-- ] -->
<!-- ``` -->
<!---->
<!-- This list will be put in front of the [list of default reporters](pytest_approval/definitions.py). -->

## Development

```sh
uv sync --all-extras
uv run pytest
```

### Release

This project uses [CalVer](https://calver.org/).

Format is: `YYYY.MM.DD` (E.g `2025.9.2`).

In case of releasing twice on one day add a micro number starting with 1:
`YYYY.MM.DD_micro` (E.g. `2025.9.2_1`).

## Alternatives

*[Syrupy](https://github.com/syrupy-project/syrupy) is a zero-dependency pytest snapshot plugin. It enables developers to write tests which assert immutability of computed results.*

<!-- Approval happens though passing a command line argument `--snapshot-update` to pytest. Syrupy has not built-in diff reporter for images (See issues [#886](https://github.com/syrupy-project/syrupy/issues/886) and [#566](https://github.com/syrupy-project/syrupy/issues/566). -->

*[Approvaltests](https://github.com/approvals/ApprovalTests.Python) is an open source assertion/verification library to aid testing.*

<!-- better default namer. if run with pytest namer takes nodeid into account and works with parametrized tests out of the box-->
<!-- Default behavior is to go through a list of reporters until one is found -->
<!-- Better list of reporters -->
<!-- Blocking behavior -->
<!-- If diff tool approves test is green imidiatly and received file is removed imidiatly not just after the next run -->
<!-- No HTTP request during testing to fetch empty binary files  -->
<!-- Less code -->
<!-- No dependencies -->
<!-- Modern python project (uv and ruff) -->
