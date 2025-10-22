import pytest
from PIL import Image, PngImagePlugin

from pytest_approval.compare import (
    compare_files,
    compare_image_contents_only,
)


@pytest.fixture
def images_equal(tmp_path):
    """Two equal images with the same metadata."""
    img1 = Image.new("L", (100, 100), color=0)  # Black image
    img2 = Image.new("L", (100, 100), color=0)

    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", "Test Image 1")
    meta.add_text("Author", "Generator")

    img1.save(tmp_path / "image1.png", pnginfo=meta)
    img2.save(tmp_path / "image2.png", pnginfo=meta)
    return (tmp_path / "image1.png", tmp_path / "image2.png")


@pytest.fixture
def images_almost_equal(tmp_path):
    """Two equal images with the different metadata."""
    img1 = Image.new("L", (100, 100), color=0)  # Black image
    img2 = Image.new("L", (100, 100), color=0)

    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", "Test Image 1")
    meta.add_text("Author", "Generator")

    img1.save(tmp_path / "image1.png", pnginfo=meta)
    img2.save(tmp_path / "image2.png")  # Missing metadata is the difference
    return (tmp_path / "image1.png", tmp_path / "image2.png")


@pytest.fixture
def images_unequal_dimensions(tmp_path):
    """Two equal images with the different metadata."""
    img1 = Image.new("L", (100, 101), color=0)  # Black image
    img2 = Image.new("L", (101, 100), color=0)

    img1.save(tmp_path / "image1.png")
    img2.save(tmp_path / "image2.png")
    return (tmp_path / "image1.png", tmp_path / "image2.png")


def test_image_compare(images_equal):
    received, approved = images_equal
    assert compare_files(received, approved) is True
    assert compare_image_contents_only(received, approved) is True


def test_image_compare_equal(images_equal):
    received, approved = images_equal
    assert compare_files(received, approved) is True
    assert compare_image_contents_only(received, approved) is True


def test_image_compare_almost_equal(images_almost_equal):
    received, approved = images_almost_equal
    assert compare_files(received, approved) is False
    assert compare_image_contents_only(received, approved) is True


def test_image_compare_unequal_dimensions(images_unequal_dimensions):
    received, approved = images_unequal_dimensions
    assert compare_files(received, approved) is False
    assert compare_image_contents_only(received, approved) is False
