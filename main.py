#!/usr/bin/env python3
"""Passive-aggressive fridge note.

When run, writes the fridge's one note to /output/entry.txt.
The note is a single line: dry, petty, specific. The fridge keeps
score of the owner's late-night visits and has taken the vegetables'
side in the dispute.
"""

import os
import tempfile

NOTE = (
    "2:14 AM. Visit #3 tonight, #41 this week. "
    "The leftovers have filed a complaint, the carrots are witnesses, "
    "and the light is now on a timer."
)


def main() -> None:
    out_dir = "/output"
    # Create the output directory if it is missing, but never chmod it:
    # in the grading sandbox it is root-owned and merely writable, so
    # chmodding it raises PermissionError and fails the entry.
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write atomically: a temp file in the same directory, made
    # world-readable (tempfile defaults to 0600, which the grader,
    # collecting outputs as another user, could not read), then moved
    # into place, so a reader never sees a half-written note.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(NOTE + "\n")
        # The grader collects outputs as another user, so the entry
        # file must be world-readable.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    # os.replace keeps the temp file's mode, but make sure the final
    # file is 0644 even if the platform ever changes that.
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
