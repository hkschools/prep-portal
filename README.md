# prep-portal

Test hosting portal for **HK-Schools.com**, served at **https://prep.hk-schools.com** via GitHub Pages.

## Folder convention

Every test is a self-contained `index.html` placed at a versioned path:

```
/<test-type>/<school>/stage<N>/v<V>/index.html
```

Example:

```
/idat-tests/cis/stage5/v1/index.html   →   https://prep.hk-schools.com/idat-tests/cis/stage5/v1/
```

Because each test folder has its own `index.html`, the trailing-slash URL serves it directly — no `.html` in the link.

## Test categories

| Folder        | Test type                          |
|---------------|------------------------------------|
| `idat-tests/` | IDAT (CIS, HKIS)                   |
| `cat4-tests/` | CAT4 (Harrow, FIS, Kellett, etc.) |
| `map-tests/`  | NWEA MAP (HKIS lower primary, etc.)|

## Adding a test

1. Create the path, e.g. `idat-tests/hkis/stage4/v2/`.
2. Drop the test's `index.html` inside it.
3. Commit to `main` — GitHub Pages redeploys automatically.

## Notes

- `CNAME` pins the custom domain (`prep.hk-schools.com`). Don't delete it.
- Tests are self-contained single files (inline SVG figures, no external assets).
- Grading is handled server-side by a separate Google Apps Script; answer keys never ship to the browser.
