"""Fail when a released `## [x.y.z]` changelog heading DISAPPEARS.

A released section is a historical record: once a version is tagged and
published, its changelog heading describes something that already shipped and
can never legitimately stop having happened. Nothing verified that, and on
03-08-2026 it stopped being true in Uprava:

  * `10f3d731` added its own `[Unreleased]` entry off a base predating
    `2fff8f27` and, in the same commit, deleted the whole `## [0.190.8]`
    heading and its bullet -- **after** v0.190.8 had been tagged and released.
    The repo was left publishing a release its own changelog did not document.

The sibling guard (`changelog_duplicate_bullets.py`) could not see this: it
checks a single file state for repeated entries, and a file with a section
missing reads as perfectly consistent. The dangling-`[Unreleased]` release
check could not see it either -- it asks whether new content is waiting to
ship, not whether shipped content is still there. A deletion is only visible
against HISTORY, which is why this check compares two revisions.

  python scripts/changelog_released_headings.py            # working tree vs HEAD
  python scripts/changelog_released_headings.py --staged   # staged blob vs HEAD
  python scripts/changelog_released_headings.py --base <rev>
  python scripts/changelog_released_headings.py --json

THE UNIT OF COMPARISON IS THE VERSION, AS A SET

Set semantics, not counts, and deliberately so: a legitimate repair sometimes
removes ONE of several identical headings. Uprava's H2184 fixed a duplicate
`## [0.74.0]` by renumbering the second to `[0.74.1]` -- the multiset changed,
the set did not, and flagging that would punish the fix for the defect. Only a
version that vanishes ENTIRELY is reported.

`[Unreleased]` is exempt: it is not a released heading, it is the staging area
above them, and it legitimately empties every time a release is cut.

WHAT COUNTS AS A RELEASED HEADING

`## [1.2.3] - 2026-08-03`, `## [1.2.3]`, `## 1.2.3`, `## v1.2.3` all count; the
token must contain a digit, so prose headings (`## Changelog`, `## Format`) are
never mistaken for versions. A heading whose DATE or prose changes is not
reported -- only the disappearance of the version identity itself, which is the
one property that is always wrong.

A MOVING BASE IS COMPARED AT ITS FORK POINT

`--base <branch>` and the pull-request default (`origin/$GITHUB_BASE_REF`)
name a branch that keeps moving. The comparison runs against
`git merge-base <base> HEAD` instead -- for a PR merge commit that is its
first parent, the base GitHub actually merged onto; for a local branch it is
where you branched. Otherwise a release cut on main after the PR's merge ref
was built reads as a heading the PR deleted (Uprava PR #2603, 11-09-2026).
A changelog byte-identical to that base passes at once. The push path
(`CHANGELOG_GUARD_BASE`, a fixed pre-push sha) is compared literally, so a
force-push that drops a released section is still caught.

FAIL-OPEN ON MISSING HISTORY, LOUDLY

A shallow clone, an initial commit, or a changelog that does not exist in the
base revision all mean "nothing to compare", not "nothing was deleted". Those
exit 0 with a printed reason rather than blocking unrelated work -- a guard
that blocks every fresh clone gets switched off within a week, and a disabled
guard measures nothing. What it will not do is stay silent about why it
skipped.

Escape hatches, for the rare genuine removal (a version cut in error, an
entire changelog restructure):

  * a repo-root `.changelog-heading-remove-allow` file -- one version per line,
    `#` comments ignored;
  * `ALLOW_CHANGELOG_HEADING_REMOVAL=1` in the environment, for one run.

There is deliberately no `--fix`. Restoring a deleted section means recovering
its exact prose from history, and which revision holds the good copy is a
judgment call the report hands you the recipe for:

    git log --oneline -- CHANGELOG.md      # find the commit before the deletion
    git show <sha>:CHANGELOG.md            # read the section back out
"""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

CHANGELOG_NAMES = ('CHANGELOG.md', 'changelog.md', 'Changelog.md')
ALLOW_FILE = '.changelog-heading-remove-allow'
ALLOW_ENV = 'ALLOW_CHANGELOG_HEADING_REMOVAL'

# `## [1.2.3] - date`, `## [1.2.3]`, `## 1.2.3`, `## v1.2.3`. The bracket is
# optional because several repos in this org omit it.
HEADING_RE = re.compile(r'^##[ \t]+\[?([^\]\s]+)\]?')
UNRELEASED = 'unreleased'


def is_version(token):
    """A released-version token: contains a digit and is not `Unreleased`.

    The digit test is what keeps prose headings (`## Format`, `## Changelog`)
    out of the comparison; without it every restructured prose section would
    read as a deleted release.
    """
    if not token or token.strip().lower() == UNRELEASED:
        return False
    return any(ch.isdigit() for ch in token)


def normalise_version(token):
    """`v1.2.3` and `1.2.3` are the same release."""
    t = token.strip()
    return t[1:] if t[:1] in ('v', 'V') and t[1:2].isdigit() else t


def released_versions(text):
    """-> {version: first_line_number} for every released heading in `text`."""
    out = {}
    for n, line in enumerate(text.splitlines(), 1):
        m = HEADING_RE.match(line)
        if not m or not is_version(m.group(1)):
            continue
        out.setdefault(normalise_version(m.group(1)), n)
    return out


def load_allowlist(repo_root):
    path = os.path.join(repo_root, ALLOW_FILE)
    if not os.path.isfile(path):
        return set()
    out = set()
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith('#'):
                out.add(normalise_version(line))
    return out


def git_show(repo_root, spec):
    """Content of `spec` (e.g. `HEAD:CHANGELOG.md`), or None if unavailable."""
    try:
        res = subprocess.run(['git', 'show', spec], cwd=repo_root,
                             capture_output=True, text=True, encoding='utf-8',
                             errors='replace', timeout=30)
    except Exception:
        return None
    return res.stdout if res.returncode == 0 else None


def find_removed(base_text, head_text, allowlist=()):
    """-> sorted [(version, base_lineno)] present in base but gone from head."""
    base, head = released_versions(base_text), released_versions(head_text)
    allow = set(allowlist)
    removed = [(v, n) for v, n in base.items()
               if v not in head and v not in allow]
    return sorted(removed, key=lambda vn: vn[1])


def repo_root_of(start):
    try:
        res = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=start,
                             capture_output=True, text=True, encoding='utf-8',
                             errors='replace', timeout=30)
    except Exception:
        return None
    return res.stdout.strip() if res.returncode == 0 else None


def fork_point(repo_root, base):
    """-> `git merge-base <base> HEAD`, or None when it cannot be resolved.

    A branch base (`origin/main`) MOVES; the commit HEAD actually grew from
    does not. On a pull request the checkout is GitHub's merge commit, built
    on whatever main was when the merge ref was computed; `origin/main` is
    fetched later, and on a busy repo a release is cut in between. Comparing
    against the moved tip reports the new `## [x.y.z]` as GONE on a PR that
    never touched the changelog (Uprava PR #2603 run 34591997041, 11-09-2026:
    merge 080b67348fb built on v0.195.481 while origin/main was already at
    v0.195.483). The merge-base of the moved tip and HEAD is exactly the
    merge commit's first parent -- the base GitHub really merged onto -- and
    for a local branch it is the fork point, so a heading released on main
    after you branched is not something your change removed.
    """
    try:
        res = subprocess.run(['git', 'merge-base', base, 'HEAD'], cwd=repo_root,
                             capture_output=True, text=True, encoding='utf-8',
                             errors='replace', timeout=30)
    except Exception:
        return None
    out = res.stdout.strip()
    return out if res.returncode == 0 and out else None


def main():
    argv = sys.argv[1:]
    as_json = '--json' in argv
    staged = '--staged' in argv
    base = 'HEAD'
    # A moving branch base is resolved to its fork point with HEAD (see
    # fork_point). The push path below is NOT: `github.event.before` is a fixed
    # sha, and after a force-push the merge-base would sit below the dropped
    # commits and hide exactly the deletion that path exists to catch.
    moving_base = False
    if '--base' in argv:
        i = argv.index('--base')
        if i + 1 >= len(argv):
            print('--base needs a revision', file=sys.stderr)
            return 2
        base = argv[i + 1]
        moving_base = True
    elif os.environ.get('GITHUB_BASE_REF'):
        # Pull request: compare against the branch being merged into.
        base = 'origin/' + os.environ['GITHUB_BASE_REF']
        moving_base = True
    elif os.environ.get('CHANGELOG_GUARD_BASE', '').strip('0 \t'):
        # Push: the workflow passes `github.event.before`, the tip BEFORE the
        # push, so a deletion buried in an earlier commit of a multi-commit push
        # is still caught. Comparing against HEAD^ would only ever see the last
        # commit; comparing against HEAD (the local default) would compare the
        # pushed state to itself and never fire at all. An all-zero sha (a
        # brand-new branch) is treated as absent and falls through.
        base = os.environ['CHANGELOG_GUARD_BASE'].strip()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = repo_root_of(here) or here
    name = next((n for n in CHANGELOG_NAMES
                 if os.path.isfile(os.path.join(repo, n))), None)
    if name is None:
        print('no changelog found in {0} — nothing to check'.format(repo))
        return 0

    if os.environ.get(ALLOW_ENV):
        print('{0}: skipped — {1} set'.format(name, ALLOW_ENV))
        return 0

    given = base
    if moving_base:
        fork = fork_point(repo, base)
        if fork:
            # Unresolvable (shallow clone, unrelated histories) keeps the
            # literal base: the pre-fix behaviour, never a silent skip.
            base = fork
    label = (given if base == given
             else '{0} (fork point {1})'.format(given, base[:12]))

    base_text = git_show(repo, '{0}:{1}'.format(base, name))
    if base_text is None:
        # Shallow clone, initial commit, or the changelog is new in this
        # revision. Nothing to compare is not the same as nothing deleted.
        msg = ('{0}: no base copy at {1} (shallow clone, initial commit, or '
               'newly added) — nothing to compare'.format(name, base))
        print(json.dumps({'file': name, 'base': base, 'skipped': msg},
                         ensure_ascii=False, indent=2) if as_json else msg)
        return 0

    if staged:
        head_text = git_show(repo, ':{0}'.format(name))
        if head_text is None:
            print('{0}: not staged — nothing to check'.format(name))
            return 0
    else:
        with open(os.path.join(repo, name), encoding='utf-8') as fh:
            head_text = fh.read()

    if head_text == base_text:
        # The change does not touch the changelog at all -- nothing can have
        # been removed, whatever has landed on the base branch since.
        if as_json:
            print(json.dumps({'file': name, 'base': label, 'staged': staged,
                              'unchanged': True, 'removed': []},
                             ensure_ascii=False, indent=2))
        else:
            print('{0}: unchanged vs {1} — no released heading removed'
                  .format(name, label))
        return 0

    removed = find_removed(base_text, head_text, load_allowlist(repo))

    if as_json:
        print(json.dumps(
            {'file': name, 'base': label, 'staged': staged,
             'removed': [{'version': v, 'base_line': n} for v, n in removed]},
            ensure_ascii=False, indent=2))
        return 1 if removed else 0

    if not removed:
        print('{0}: no released heading removed (vs {1})'.format(name, label))
        return 0

    print('')
    print('{0}: {1} released heading(s) present at {2} are GONE:'
          .format(name, len(removed), label))
    print('')
    for v, n in removed:
        print('  [{0}]   (was {1}:{2} line {3})'.format(v, base, name, n))
    print('')
    print('A released section is a historical record — once a version ships, its')
    print('entry can never legitimately stop having happened. The usual cause is')
    print('an edit written off a stale base that silently drops sections added')
    print('by a concurrent session (Uprava 10f3d731, 03-08-2026: deleted')
    print('## [0.190.8] after that version was already tagged and released).')
    print('')
    print('Recover the section rather than re-typing it:')
    print('    git log --oneline -- {0}      # the commit before the deletion'.format(name))
    print('    git show <sha>:{0}            # read the section back out'.format(name))
    print('')
    print('If the removal is genuinely intended (a version cut in error, a full')
    print('restructure), record it instead of silencing it:')
    print('    echo "<version>" >> {0}'.format(ALLOW_FILE))
    print('    {0}=1 <your command>'.format(ALLOW_ENV))
    print('')
    return 1


if __name__ == '__main__':
    sys.exit(main())
