import pytest

from pytest_approval import scrub

datetime_text_exmaples = (
    "Tue May 13 16:30:00",
    "Wed Nov 17 22:28:33 EET 2021",
    "Tue May 13 2014 23:30:00.789",
    "Tue May 13 16:30:00 -0800 2014",
    "13 May 2014 23:50:49,999",
    "May 13, 2014 11:30:00 PM PST",
    "23:30:00",
    "2014/05/13 16:30:59.786",
    "2020-9-10T08:07Z",
    "2020-09-9T08:07Z",
    "2020-09-10T8:07Z",
    "2020-09-10T08:07Z",
    "2020-09-10T08:07:89Z",
    "2020-09-10T01:23:45.678Z",
    "2023-07-16 17:39:03.293919",
    "2023-12-06T11:59:47.090226",
    "20210505T091112Z",
    "Tue May 13 16:30:00 2014",
    "Wed Dec 11 14:59:44 2024",
    "2021-09-10T08:07:00+03:00",
    "2021-01-01T00:00:00+00:00",
    "20250527_125703",
    "2020-02-02",
)


@pytest.mark.parametrize("example", datetime_text_exmaples)
def test_scrub_datetime(example: str):
    scrub_datetime = scrub.get_datetime_scrubber(example)
    assert scrub_datetime(f"prefix {example} postfix") == "prefix {{DATETIME}} postfix"


@pytest.mark.parametrize("example", ("", "foo"))
def test_scrub_datetime_not_found(example):
    with pytest.raises(scrub.NoDatetimeScrubberFoundError) as error:
        scrub.get_datetime_scrubber(example)
    assert example in str(error.value)
