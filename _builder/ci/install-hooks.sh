#!/usr/bin/env bash
# Run the page checks locally, before a push leaves this machine.
#
# GitHub Actions is the real gate, but adding a workflow needs a token with
# `workflow` scope and the CLI token here does not have one, so
# .github/workflows/check-ordering.yml cannot be pushed from this machine.
# Until someone runs `gh auth refresh -s workflow` and pushes that file, this
# hook is what stands between a broken item and prep.hk-schools.com.
#
#     bash _builder/ci/install-hooks.sh     # install
#     rm .git/hooks/pre-push                # remove
#
# Bypass once, if a push genuinely must go out: git push --no-verify

set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p .git/hooks

cat > .git/hooks/pre-push <<'HOOK'
#!/usr/bin/env bash
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
fail=0
for check in _builder/check_ordering_items.py _builder/lint_markup.py; do
    [ -f "$check" ] || continue
    printf '  %s ... ' "$(basename "$check")"
    if out=$(python3 "$check" 2>&1); then
        echo ok
    else
        echo FAILED
        echo "$out" | sed 's/^/    /'
        fail=1
    fi
done
if [ "$fail" -ne 0 ]; then
    echo
    echo "push blocked: fix the above, or 'git push --no-verify' to override."
    exit 1
fi
HOOK

chmod +x .git/hooks/pre-push
echo "installed .git/hooks/pre-push"
