"""Path expansion of the * and ? globs for Windows OS."""

import glob
import os.path


def _expand(path, is_recursive=False):
    expanded_paths = [path]
    if ("*" in path) or ("?" in path):
        path = path.replace("[", "?")  # disable "[" glob
        path = path.replace("]", "?")  # disable "]" glob
        for p in glob.iglob(path):
            if is_recursive and os.path.isdir(p):
                expanded_paths.extend(
                    _expand(os.path.join(p, "*"), is_recursive)
                    )
            elif not os.path.isdir(p):
                expanded_paths.append(p)
        expanded_paths.pop(0)
    return expanded_paths


def expand(paths, is_recursive=False):
    """Path expansion with optional recursive expansion."""
    for path in paths[:]:
        paths.extend(_expand(path, is_recursive))
        paths.pop(0)
    return paths
