#!/usr/bin/env python3
"""Validate pinned inputs and materialize the owned physical product skill packages.

No dependency installation, symlink traversal, or implicit source repinning. Edit the
canonical files and explicitly review/update runtime-source-policy.json first.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import stat
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit

NAMES = ("phoenix-writing", "maintaining-writing-skills", "creating-vitepress-post", "managing-article-publication")
RUNTIMES = (".agents", ".claude")
POLICY = "maintenance/harness-adoption/runtime-source-policy.json"
MANIFEST = "maintenance/harness-adoption/generated-writing-manifest.json"
ALIASES = (
    ("skills/phoenix-writing/reference", "../../maintenance/writing-skills/legacy/phoenix-writing/reference", "maintenance/writing-skills/legacy/phoenix-writing/reference", "phoenix-writing/reference"),
    ("skills/phoenix-writing/scripts", "../maintaining-writing-skills/legacy-validator", "skills/maintaining-writing-skills/legacy-validator", "phoenix-writing/scripts"),
)
CLAUDE_KEYS = {"disable-model-invocation", "user-invocable", "allowed-tools", "context", "agent", "model", "argument-hint", "hooks"}


class Invalid(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def safe_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise Invalid("invalid relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(x in ("", ".", "..") for x in value.split("/")):
        raise Invalid("path escape or noncanonical path: " + value)
    return value


def checked_path(root, relative, *, allow_leaf_link=False, missing=False):
    """lstat every component before any read or write; never resolve a link."""
    safe_relative(relative)
    current = root
    parts = PurePosixPath(relative).parts
    for i, component in enumerate(parts):
        current = current / component
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if missing:
                return current.joinpath(*parts[i + 1:])
            raise Invalid("missing path: " + relative) from None
        if stat.S_ISLNK(mode) and not (allow_leaf_link and i == len(parts) - 1):
            raise Invalid("symlink component rejected: " + current.relative_to(root).as_posix())
        if i < len(parts) - 1 and not stat.S_ISDIR(mode):
            raise Invalid("non-directory parent: " + relative)
    return current


def inventory(root, relative, allowed_links=()):
    """Walk directory entries without following any symlinks, including dirs."""
    base = checked_path(root, relative)
    if not base.is_dir():
        raise Invalid("expected directory: " + relative)
    files = set()
    links = {}
    def walk(directory):
        for entry in sorted(os.scandir(directory), key=lambda e: e.name):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISLNK(mode):
                if rel not in allowed_links:
                    raise Invalid("unknown/nested symlink: " + rel)
                links[rel] = os.readlink(path)
            elif stat.S_ISDIR(mode):
                walk(path)
            elif stat.S_ISREG(mode):
                files.add(rel)
            else:
                raise Invalid("non-regular input/output: " + rel)
    walk(base)
    return files, links


def load_inputs(root):
    policy_path = checked_path(root, POLICY)
    raw = policy_path.read_bytes()
    policy = json.loads(raw)
    if set(policy) != {"schema_version", "skills", "implicit", "inputs", "aliases"} or policy["schema_version"] != 1:
        raise Invalid("unsupported source policy schema")
    if policy["skills"] != list(NAMES) or policy["implicit"] != {n: True for n in NAMES}:
        raise Invalid("skill ownership or invocation policy changed")
    aliases = [{"path": p, "literal_target": t, "backing_root": b, "runtime_subpath": d, "literal_sha256": sha(t.encode())} for p, t, b, d in ALIASES]
    if policy["aliases"] != aliases:
        raise Invalid("alias mapping differs from the two approved literal exceptions")
    pinned = {}
    for entry in policy["inputs"]:
        if set(entry) != {"path", "sha256"}:
            raise Invalid("unexpected input policy fields")
        path = safe_relative(entry["path"])
        if path in pinned or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            raise Invalid("duplicate input or invalid pinned SHA: " + path)
        pinned[path] = entry["sha256"]
    actual = set()
    actual_links = {}
    for name in NAMES:
        files, links = inventory(root, "skills/" + name, {a[0] for a in ALIASES})
        actual |= files
        actual_links.update(links)
    for alias, target, backing, destination in ALIASES:
        path = checked_path(root, alias, allow_leaf_link=True)
        if not path.is_symlink() or actual_links.get(alias) != target or os.readlink(path) != target:
            raise Invalid("missing/changed alias literal: " + alias)
        # Independently validate the named regular backing tree, never via alias.
        files, unused = inventory(root, backing)
        actual |= files
    if set(pinned) != actual:
        raise Invalid("source inventory drift; missing=" + str(sorted(set(pinned) - actual)) + "; extra=" + str(sorted(actual - set(pinned))))
    contents = {}
    for path, expected in sorted(pinned.items()):
        if "/agents/" in path or path.endswith("/openai.yaml"):
            raise Invalid("foreign runtime metadata in canonical source: " + path)
        file = checked_path(root, path)
        if not stat.S_ISREG(file.lstat().st_mode):
            raise Invalid("non-regular source: " + path)
        data = file.read_bytes()
        if sha(data) != expected:
            raise Invalid("source SHA drift: " + path)
        contents[path] = data
    for name in NAMES:
        key = f"skills/{name}/SKILL.md"
        if key not in contents:
            raise Invalid("missing canonical SKILL: " + key)
        text = contents[key].decode("utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise Invalid("missing skill frontmatter: " + key)
        frontmatter = text.split("---\n", 2)[1]
        # This project uses the reviewed plain-key YAML subset. Refuse quoted,
        # complex/merge keys and directives rather than pretending this regex is
        # a general YAML parser or allowing a second runtime key spelling.
        for line in frontmatter.splitlines():
            if line.startswith("\t") or (line.strip() and not line.startswith((" ", "#"))
                                         and not re.match(r"^[A-Za-z][\w-]*:", line)):
                raise Invalid("foreign runtime frontmatter syntax: " + key)
        keys = re.findall(r"^([A-Za-z][\w-]*):", frontmatter, re.M)
        top_keys = set(keys)
        allowed_keys = {"name", "description", "license", "compatibility", "metadata"}
        names = re.findall(r"^name:[ \t]*([^\n]+)$", frontmatter, re.M)
        if (len(keys) != len(top_keys) or not top_keys <= allowed_keys
                or top_keys & CLAUDE_KEYS or len(names) != 1 or names[0].strip() != name):
            raise Invalid("foreign runtime frontmatter/name: " + key)
    return raw, contents


def logical_sources(contents):
    logical = {p: (p, data) for p, data in contents.items() if p.startswith("skills/")}
    for alias, target, backing, destination in ALIASES:
        for source, data in contents.items():
            if source.startswith(backing + "/"):
                name = alias + source[len(backing):]
                if name in logical:
                    raise Invalid("alias output collides with canonical input: " + name)
                logical[name] = (source, data)
    return logical


def project_target(target, logical_file, runtime_file, root, logical):
    if target.startswith("#"):
        return target
    parsed = urlsplit(target)
    if parsed.scheme:
        if parsed.scheme not in ("http", "https", "mailto"):
            raise Invalid("unknown URL/link scheme: " + target)
        return target
    if target.startswith("/") or parsed.netloc or parsed.query or "\\" in target or re.search(r"[\s<>]", target):
        raise Invalid("unknown/nonportable local link syntax: " + target)
    source_target = posixpath.normpath(posixpath.join(posixpath.dirname(logical_file), unquote(parsed.path)))
    safe_relative(source_target)
    if source_target in logical:
        runtime_root = runtime_file.split("/skills/", 1)[0] + "/skills/"
        destination = runtime_root + source_target[len("skills/"):]
    else:
        # Repository references stay in the repository. Unknown canonical skill
        # references must not escape into a second editing/discovery source.
        if source_target.startswith("skills/"):
            raise Invalid("missing/unknown canonical skill link: " + source_target)
        file = checked_path(root, source_target)
        if not (file.is_file() or file.is_dir()):
            raise Invalid("missing link target: " + source_target)
        destination = source_target
    projected = quote(posixpath.relpath(destination, posixpath.dirname(runtime_file)), safe="/-._~")
    if parsed.fragment:
        projected += "#" + parsed.fragment
    return projected


def project_markdown(data, logical_file, runtime_file, root, logical):
    # Fixtures are validator data, not navigable agent references. Their literal
    # invalid/missing links are intentional historical test cases.
    if "/tests/fixtures/" in logical_file:
        return data, []
    text = data.decode("utf-8")
    changes = []
    fence = None
    output = []
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            output.append(line)
            continue
        if fence is not None:
            output.append(line)
            continue
        # Ignore inline code, preserve every other byte around explicit links.
        segments = re.split(r"(`+[^`]*`+)", line)
        for i in range(0, len(segments), 2):
            segment = segments[i]
            if re.search(r"\[[^\]\n]+\]\[|^\s*\[[^\]]+\]:|<(?:a|img)\b|(?:^|\s)@(?:\./|\.\./)", segment, re.I):
                raise Invalid("unknown active Markdown reference syntax: " + logical_file)
            def replacement(match):
                target = match.group(2)
                new = project_target(target, logical_file, runtime_file, root, logical)
                if target != new:
                    changes.append({"from": target, "to": new})
                return match.group(1) + new + ")"
            projected = re.sub(r"(!?\[[^\]\n]*\]\()([^\)\n]+)\)", replacement, segment)
            if "](" in re.sub(r"!?\[[^\]\n]*\]\([^\)\n]+\)", "", segment):
                raise Invalid("unsupported active Markdown link syntax: " + logical_file)
            segments[i] = projected
        output.append("".join(segments))
    if fence:
        raise Invalid("unclosed Markdown code fence: " + logical_file)
    return "".join(output).encode(), changes


def render(root, raw_policy, contents):
    logical = logical_sources(contents)
    files = {}
    records = []
    for runtime in RUNTIMES:
        for logical_path, (source, data) in sorted(logical.items()):
            destination = runtime + "/skills/" + logical_path[len("skills/"):]
            projected, links = (project_markdown(data, logical_path, destination, root, logical)
                                if logical_path.endswith(".md") else (data, []))
            files[destination] = projected
            records.append({"path": destination, "source": source, "logical_source": logical_path,
                            "source_sha256": sha(data), "sha256": sha(projected), "links": links})
        if runtime == ".agents":
            for name in NAMES:
                destination = f"{runtime}/skills/{name}/agents/openai.yaml"
                metadata = (f'interface:\n  display_name: "{name}"\n'
                            'policy:\n  allow_implicit_invocation: true\n').encode()
                files[destination] = metadata
                records.append({"path": destination, "source": "generated:codex-metadata",
                                "sha256": sha(metadata)})
    manifest = {"schema_version": 1, "source_policy_sha256": sha(raw_policy),
                "generator_sha256": sha(Path(__file__).read_bytes()), "skills": list(NAMES),
                "files": sorted(records, key=lambda r: r["path"])}
    files[MANIFEST] = json_bytes(manifest)
    return files


def validate_runtime(root):
    allowed = {f"{runtime}/skills/{name}": f"../../skills/{name}" for runtime in RUNTIMES for name in NAMES}
    for runtime in RUNTIMES:
        path = checked_path(root, f"{runtime}/skills", missing=True)
        if not path.exists():
            continue
        files, links = inventory(root, f"{runtime}/skills", allowed)
        for alias, target in links.items():
            if target != allowed[alias]:
                raise Invalid("unknown existing runtime entry alias: " + alias)
    manifest = checked_path(root, MANIFEST, missing=True)
    if manifest.exists() and not stat.S_ISREG(manifest.lstat().st_mode):
        raise Invalid("manifest must be a regular file or absent")


def output_inventory(root):
    actual = {}
    for runtime in RUNTIMES:
        for name in NAMES:
            target = f"{runtime}/skills/{name}"
            if not (root / target).exists() or (root / target).is_symlink():
                raise Invalid("missing/nonphysical runtime package: " + target)
            files, links = inventory(root, target)
            for path in files:
                actual[path] = checked_path(root, path).read_bytes()
    actual[MANIFEST] = checked_path(root, MANIFEST).read_bytes()
    return actual


def stage_files(directory, files):
    for relative, data in files.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o644)


def install(root, stage, fail_after):
    targets = [f"{r}/skills/{n}" for r in RUNTIMES for n in NAMES] + [MANIFEST]
    installed = []
    backups = []
    backup_root = stage / "rollback"
    try:
        for index, target in enumerate(targets, 1):
            destination = checked_path(root, target, allow_leaf_link=True, missing=True)
            destination.parent.mkdir(parents=True, exist_ok=True)
            backup = backup_root / target
            if destination.exists() or destination.is_symlink():
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, backup)
                backups.append((destination, backup))
            os.replace(stage / target, destination)
            installed.append(destination)
            if fail_after == index:
                raise Invalid("injected partial-install failure after " + str(index))
    except BaseException:
        for destination in reversed(installed):
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        for destination, backup in reversed(backups):
            os.replace(backup, destination)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="recompute in temp and compare without repository writes")
    mode.add_argument("--write", action="store_true", help="explicitly replace the six owned package directories and manifest")
    parser.add_argument("--test-fail-after", type=int, choices=range(1, 8), help="exercise transactional rollback after this install step")
    args = parser.parse_args()
    root = args.root.absolute()
    # The checkout root itself and all its ancestors must be real directories.
    for parent in (root, *root.parents):
        if parent.is_symlink():
            raise Invalid("symlink checkout root/ancestor")
    if args.check and args.test_fail_after:
        raise Invalid("fault injection is only available with explicit --write")
    raw_policy, contents = load_inputs(root)
    validate_runtime(root)
    files = render(root, raw_policy, contents)
    # --check uses system temp only. --write stages on the checkout filesystem
    # so directory os.replace is atomic, without trusting a linked output root.
    with tempfile.TemporaryDirectory(prefix="writing-materializer-", dir=None if args.check else root) as temp:
        stage = Path(temp)
        stage_files(stage, files)
        for runtime in RUNTIMES:
            staged_files, links = inventory(stage, runtime + "/skills")
        if args.check:
            actual = output_inventory(root)
            if actual != files:
                drift = sorted(p for p in set(actual) | set(files) if actual.get(p) != files.get(p))
                raise Invalid("generated output drift: " + str(drift))
        else:
            install(root, stage, args.test_fail_after)
    print(json.dumps({"status": "pass", "mode": "check" if args.check else "write",
                      "source_files": len(contents), "generated_files": len(files) - 1,
                      "source_policy_sha256": sha(raw_policy)}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError, ValueError, UnicodeError, KeyError, TypeError) as error:
        print("MATERIALIZER: " + str(error), file=sys.stderr)
        sys.exit(1)
