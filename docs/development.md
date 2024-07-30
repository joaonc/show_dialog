# Development
Uses [Qt 6](https://www.qt.io) and [Qt for Python](https://wiki.qt.io/Qt_for_Python), aka _PySide_,
which includes _Qt Designer_, a WYSIWYG UI editor.

Docstrings are in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

## Contributing
**TODO**

### Linting and Tests
Linting and unit tests are done as actions in GitHub, but should be executed locally with the
following commands:
```
inv lint.all
```
```
inv test.unit
```
If using an IDE such as PyCharm or VS Code, the tests can be executed from within the IDE.

Note that pytest options are in `pyproject.toml`, in the `[tool.pytest.ini_options]` section and
linting options are also in `pyproject.toml` and `setup.cfg`.

## Publish to Pypi

## Releases in GitHub
In addition to publishing as a package in Pypi, a release is also created in GitHub with executable
files that can be downloaded and executed with no dependencies (including not needing Python).

Releases are published in GitHub, under the
[Releases](https://github.com/joaonc/show_dialog/releases) page.

At the time of this writing, releasing binaries is not yet an automated process with GitHub actions,
so the steps below will need to be done manually.

### GH CLI
This project uses [GitHub CLI](https://cli.github.com/) ([docs](https://cli.github.com/manual/))
to manage releases.

You'll need to install and authenticate `gh` in order to perform the release tasks.

To install, download the file in the link above and follow the instructions.

Authenticate with this command:
```
gh auth login
```

??? Note "Sample output"

    Sample output from login with the `HTTPS` protocol and via web browser.
    ```
    gh auth login
    ? What account do you want to log into? GitHub.com
    ? What is your preferred protocol for Git operations on this host? HTTPS
    ? Authenticate Git with your GitHub credentials? Yes
    ? How would you like to authenticate GitHub CLI? Login with a web browser

    ! First copy your one-time code: 9999-9999
    Press Enter to open github.com in your browser... 
    ✓ Authentication complete.
    - gh config set -h github.com git_protocol https
    ✓ Configured git protocol
    ✓ Logged in as <GH username>
    ```

You can authenticate in other ways, see
[docs](https://cli.github.com/manual/gh_auth_login) for more info.

### Create release
1. Update (increase) the app version in `assets/app.yaml`.
2. Create and merge a new PR called _"Preparing for v1.2.3"_ release.  
   This merges the new version, which will be used to create the release and set it to the right
   commit hash.
3. Run `inv build.release`
   Use the `--notes` or `--notes-file` to add more details to the release.  

!!! Note "Recommended command"

    Create the file `release_notes.md` and _don't_ add it to the project.

    ```
    inv build.release --notes-file release_notes.md
    ```

See sections below for beta and draft releases.

#### Beta
**TODO**

#### Draft
**TODO**

### Upload artifacts
**TODO**

## More info
[Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
