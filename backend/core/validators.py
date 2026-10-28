"""Upload checks for icon files.

Icon files arrive from contributors, so neither the filename nor the browser's
content type is trusted: every check also looks at the bytes on the way in.

These are attached to the model fields, so they run for the API and for the Django
admin form. They do not run on ``Model.save()``, which is why the files already on
disk from ``import_icons`` are left exactly as they are -- the check is for new
uploads.
"""

import codecs
import re

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat

# 2 MB. These are map icons: the largest file in the imported set is a 439 KB PNG
# (median 13 KB), so the limit leaves room without inviting multi-megabyte artwork.
MAX_ICON_FILE_SIZE = 2 * 1024 * 1024

# How much of the file to read when identifying it. Enough for a PNG signature and
# for an SVG prologue (XML declaration, comments, a DOCTYPE) plus the root tag.
_HEAD_BYTES = 4096

# The first 8 bytes of every PNG file.
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# An SVG may open with an XML declaration, comments or a DOCTYPE before the root
# element, but the root element itself has to be <svg>.
_SVG_ROOT = re.compile(
    r"""\A\s*
        (?:
            <\?xml[^>]*\?>            # <?xml version="1.0"?>
          | <!--.*?-->                # a comment
          | <!DOCTYPE[^>\[]*(?:\[[^\]]*\])?[^>]*>
          | \s+
        )*
        <svg[\s>/]
    """,
    re.IGNORECASE | re.DOTALL | re.VERBOSE,
)


def _head(uploaded_file):
    """Read the start of an upload without disturbing the position it was handed to us at."""
    position = uploaded_file.tell() if hasattr(uploaded_file, "tell") else 0
    uploaded_file.seek(0)
    try:
        return uploaded_file.read(_HEAD_BYTES)
    finally:
        uploaded_file.seek(position)


def validate_icon_file_size(uploaded_file):
    """Reject anything over MAX_ICON_FILE_SIZE, before it is written under media/."""
    size = getattr(uploaded_file, "size", None)
    if size is None:
        return
    if size > MAX_ICON_FILE_SIZE:
        # Only the limit is quoted: filesizeformat rounds, so printing the upload's own
        # size next to it reads as "File is 2.0 MB; the limit is 2.0 MB."
        raise ValidationError(
            "File is too large: the limit is %(limit)s.",
            code="icon_file_too_large",
            params={"limit": filesizeformat(MAX_ICON_FILE_SIZE)},
        )


def validate_png_file(uploaded_file):
    """A .png name is not proof: check the PNG signature too."""
    FileExtensionValidator(allowed_extensions=["png"])(uploaded_file)
    if not _head(uploaded_file).startswith(_PNG_SIGNATURE):
        raise ValidationError(
            "Not a PNG file: the PNG signature is missing.",
            code="not_a_png",
        )


def validate_svg_file(uploaded_file):
    """A .svg name is not proof: check that the markup really opens an <svg> root."""
    FileExtensionValidator(allowed_extensions=["svg"])(uploaded_file)
    head = _head(uploaded_file)
    # Decoded incrementally with final=False: the read stops at a fixed byte count,
    # which can land in the middle of a multi-byte character, and a plain
    # bytes.decode() would call that valid file "not UTF-8".
    try:
        text = codecs.getincrementaldecoder("utf-8")().decode(head, False)
    except UnicodeDecodeError:
        raise ValidationError(
            "Not an SVG file: the contents are not UTF-8 text.",
            code="not_an_svg",
        )
    if not _SVG_ROOT.match(text):
        raise ValidationError(
            "Not an SVG file: no <svg> root element at the start of the file.",
            code="not_an_svg",
        )
