"""The single authority-free canonical content encoding and digest primitive.

This module is deliberately the *only* place in the repository where canonical
bytes and their digest are produced. Two independent copies of a
canonicalization rule are two rules that can silently drift apart, and a drift
between them would make one layer's "same content" the other layer's
"different content" without either layer failing. Sharing one primitive makes
that class of divergence impossible rather than merely discouraged.

`Canonicalization != Authority` is the boundary this module keeps. It encodes
and hashes; it decides nothing. It has no notion of a specification, an
experiment, a freeze, a verdict, or a birth, and it grants no permission to any
caller. A layer that imports it therefore inherits exactly one thing — a
deterministic byte encoding — and no authority whatsoever from any other layer
that also imports it.
"""

from __future__ import annotations

import hashlib
import json
from typing import Final

CANONICAL_HASH_ALGORITHM: Final = "sha256"

CANONICALIZATION_IS_NOT_AUTHORITY_NOTE: Final = (
    "canonical encoding and digesting decide nothing: sharing this primitive "
    "transfers a byte encoding between layers, never an authority"
)


def canonical_bytes(encoded: object) -> bytes:
    """Return the canonical bytes of an already-encoded JSON-compatible value.

    The caller owns the encoding schema. This function only fixes the byte
    representation of that schema: sorted keys, no insignificant whitespace,
    unescaped non-ASCII, and UTF-8 with surrogates passed through rather than
    silently replaced.
    """

    return json.dumps(
        encoded, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8", "surrogatepass")


def canonical_digest(content: bytes) -> str:
    """Return the hexadecimal digest of canonical bytes under the fixed algorithm."""

    if type(content) is not bytes:
        raise TypeError("a canonical digest requires canonical bytes")
    return hashlib.sha256(content).hexdigest()


def is_canonical_digest(value: object) -> bool:
    """Return whether a value has the exact shape of a canonical digest."""

    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


__all__ = [
    "CANONICALIZATION_IS_NOT_AUTHORITY_NOTE",
    "CANONICAL_HASH_ALGORITHM",
    "canonical_bytes",
    "canonical_digest",
    "is_canonical_digest",
]
