from __future__ import annotations

import pytest
from PIL import Image

from scripts.collect_dataset import (
    CurationError,
    canonical_license,
    clean_html,
    render_woodcut,
    validate_source,
)


def test_canonical_license_accepts_only_project_families() -> None:
    assert canonical_license("Public domain") == "Public domain"
    assert canonical_license("CC0") == "CC0"
    assert canonical_license("CC BY 3.0") == "CC-BY 3.0"
    assert canonical_license("CC BY-SA 4.0") == "CC-BY-SA 4.0"

    with pytest.raises(CurationError, match="Licença não permitida"):
        canonical_license("Attribution")


def test_clean_html_preserves_readable_attribution() -> None:
    value = '<a href="https://commons.wikimedia.org/wiki/User:Example">Example</a><br>Own work'

    assert clean_html(value) == "Example; Own work"


def test_validate_source_requires_resolution_author_and_license() -> None:
    page = {
        "title": "File:Example.jpg",
        "canonicalurl": "https://commons.wikimedia.org/wiki/File:Example.jpg",
        "lastrevid": 123,
        "imageinfo": [
            {
                "width": 1024,
                "height": 768,
                "mime": "image/jpeg",
                "url": "https://upload.wikimedia.org/example.jpg",
                "sha1": "abc",
                "extmetadata": {
                    "Artist": {"value": "<b>Example Author</b>"},
                    "LicenseShortName": {"value": "CC BY-SA 4.0"},
                    "LicenseUrl": {"value": "https://creativecommons.org/licenses/by-sa/4.0/"},
                },
            }
        ],
    }

    source = validate_source(page)

    assert source["source_author"] == "Example Author"
    assert source["source_license"] == "CC-BY-SA 4.0"
    assert source["source_dimensions"] == [1024, 768]


def test_render_woodcut_has_stable_size_and_reduced_palette() -> None:
    source = Image.new("RGB", (900, 700))
    for x in range(source.width):
        shade = round(255 * x / (source.width - 1))
        for y in range(source.height):
            source.putpixel((x, y), (shade, shade, shade))

    rendered = render_woodcut(source, 512, (0.5, 0.5))

    assert rendered.size == (512, 512)
    colors = rendered.getcolors(maxcolors=3)
    assert colors is not None
    assert {color for _, color in colors} <= {(18, 18, 16), (246, 240, 222)}
