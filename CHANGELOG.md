# CHANGELOG

## Current Main

- build/tests: add pytest-randomly to run tests in random order (#2296c6f)
* build(ci)/tests: add pytest-xdist and run tests in CI in parallel (5d663a5)

## 0.12.0

- fix: add pycharm and code programs paths for macOS to BINARY_REPORER (#c2ae2be)
- build: run uv sync --upgrade (#f08e0ab)
- docs: various improvements to the documentation
- build(ci): run pytest-markdown-docs in CI (#8544303)

## 0.11.0

- fix: use last `]` of pytest node ID for computing hash naming  (#999a298)
    - previously naming of parametrized tests produced unexpected name if parameter
      contained multiple closing brackets (`]`)
- refactor: add auto-approve as argument to private _verify function and add
  path with directories to NAMES_WITHOUT_EXTENSION list (#097763b)
- fix: remove approval file if reporting failed and file is empty (#9727e66)
- refactor: do not raise assertion error if gnu diff is reporter (#839f370)
- feat: verify ploty figure (#2076c69, #3b19d68)

## 0.9.0

- feat: use gnu diff tool as reporter if CI is detected via env (#fa622be)

## 0.8.0

- feat(datetime-scrubber): support milliseconds format between 1 and 6 places (#5d343bbcc1111cf46b0f06b5949eda036531cea9)

## 0.7.0

- feat: make usage of multiple scrubbers possible (#5136457)

## 0.6.0

- feat: add uuid scrubber (#d86f1f1ca37e15e99df62006e464ba0e3feab3c5)

## 0.5.0

- feat: add more formats to date-time scrubber (#b03be9e)

## 0.4.0

- feat: optional scrub text input by providing a scrubber function. A datetime scrubber is provided. (#10d6ca5)

## 0.3.0

- fix: move utility function depended on pillow to conditional block (#965920f)

## 0.2.0

* fix: create parent directories of file names if not exists (#6a37909)
