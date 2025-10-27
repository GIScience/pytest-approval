# pytest approval

[![Build Status](https://jenkins.heigit.org/buildStatus/icon?job=pytest-approval/main)](https://jenkins.heigit.org/job/pytest-approval/job/main/)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=pytest-approval&metric=alert_status)](https://sonarcloud.io/dashboard?id=pytest-approval)
[![PyPI - Version](https://img.shields.io/pypi/v/pytest-approval)](https://pypi.org/project/pytest-approval/)
[![LICENSE](https://img.shields.io/github/license/GIScience/pytest-approval)](COPYING)
[![status: active](https://github.com/GIScience/badges/raw/master/status/active.svg)](https://github.com/GIScience/badges#active)

A simple approval test library utilizing external diff programs such as
PyCharm and Visual Studio Code to compare approved and received output.

## About

Approval tests capture the output (a snapshot) of a piece of code and compare it
with a previously approved version of the output (the expected result).

It's most useful in environments where frequent changes are common or where
the output is of a complex nature but can be easily verified by humans, aided for
example by a diff-tool or a visual representation of the output (think of an image).

Once the output has been *approved* then as long as the output stays the same
the test will pass. A test fails if the *received* output is not identical to
the approved version. In that case, the difference between the received and the
approved output is reported to the tester.

For outputs that can be represented by text, a report can be as simple as
printing the difference to the terminal. Using diff programs with a graphical
user interface such as Meld, PyCharm or Visual Studio Code as *reporter* not
only helps to visualize the difference, but they can also be used as *approver*
by applying the changes of the received output to the approved output.

Not all data can or should be represented by text. In many cases an
image is the best and most easily verifiable representation.
PyCharm and Visual Studio Code can work with images as well.

> A picture’s worth a 1000 tests ([approvaltests.com](https://approvaltests.com/)).


<!-- ## Features -->
<!---->
<!-- - Auto approval mode: Helps cleaning up approval files -->
<!-- - Generated names of approval files are based on pytest nodeid -->


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
uv add pytest-approval

# Including image support
uv add --optional image pytest-approval
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


To verify binary files such as an image PyCharm or Visual Studio Code needs to
be installed. Examples:

```python
from PIL import Image
from pytest_approval import verify_binary, verify_image, verify_image_pillow


def test_verify_binary(image):
    with open("my_image.jpg", "rb") as file:
        buffer = file.read()
    assert verify_binary(buffer, extension=".jpg")


def test_verify_image(image):
    image = Image.open("my_image.jpg")
    assert verify_image(image, extension=".jpg", content_only=True)


def test_verify_image_pillow(image):
    image = Image.open("my_image.jpg")
    assert verify_image_pillow(image, extension=".jpg")
```


During development its sometimes helpful to show received and approved output,
to report, even though both are equal:

```python
from pytest_approval import verify, verify_json


def test_verify_string()
    assert verify("Hello World!", report_always=True)
```

### Auto approval

It is possible to run auto approve every approval tests:
```shell
uv run pytest --auto-approve
```

This is useful for elimination of approval files which are not in use anymore.
1. Make sure tests are green.
2. Then remove all approval files.
3. Run pytest in auto approval mode.


## Configuration

Approved and received files are stored next to the test file per default.
If you want to save those files in a specific directory instead, please set the `approvals-dir` key in your `pyproject.toml`:

```toml
[tool.pytest-approval]
"approvals-dir"="tests/approvals"  
```

The path is relative to pytest root (usually `pyproject.toml`).

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
uv run pre-commit install
uv run pytest
```

### Release

This project uses [SemVer](https://semver.org/).

To make a new release run `./scripts/release.sh <version>`.


## Alternatives

- [Syrupy](https://github.com/syrupy-project/syrupy) is a zero-dependency pytest snapshot plugin. It enables developers to write tests which assert immutability of computed results.
- [Approvaltests](https://github.com/approvals/ApprovalTests.Python) is an open source assertion/verification library to aid testing.

<!-- Approval happens though passing a command line argument `--snapshot-update` to pytest. Syrupy has not built-in diff reporter for images (See issues [#886](https://github.com/syrupy-project/syrupy/issues/886) and [#566](https://github.com/syrupy-project/syrupy/issues/566). -->


<!-- better default namer. if run with pytest namer takes nodeid into account and works with parametrized tests out of the box-->
<!-- Default behavior is to go through a list of reporters until one is found -->
<!-- Better list of reporters -->
<!-- Blocking behavior -->
<!-- If diff tool approves test is green imidiatly and received file is removed imidiatly not just after the next run -->
<!-- No HTTP request during testing to fetch empty binary files  -->
<!-- Less code -->
<!-- No dependencies -->
<!-- Modern python project (uv and ruff) -->
