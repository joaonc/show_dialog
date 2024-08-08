# Development
Uses [Qt 6](https://www.qt.io) and [Qt for Python](https://wiki.qt.io/Qt_for_Python), aka _PySide_,
which includes _Qt Designer_, a WYSIWYG UI editor.

Docstrings are in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

## Contributing
### Requirements
```
pip install -r requirements-dev.txt
```

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

### Running
Running the code from the CLI or from the IDE needs be done as a module.  
If trying to run as a script, the relative imports won't work.

#### CLI
With an inputs file and log level specified.
```
python -m src.show_dialog.main --inputs-file assets/inputs/inputs_07.yaml --log-level debug
```

#### IDE
This section has screenshots from PyCharm. VS Code and other IDEs should have similar options.

When running from the IDE, make sure you specify to run `main` as a module, not a script.

![Module](images/run_main_module.png)

Here are the full options, including parameters.  
The working directory should be the project root, not the directory where `main.py` is located.

![Main](images/run_main_config.png)

## Publishing
### Build app

### Create release in GitHub
In addition to publishing as a package in Pypi, a release is also created in GitHub with executable
files that can be downloaded and executed with no dependencies (including not needing Python).

Releases are published in GitHub, under the
[Releases](https://github.com/joaonc/show_dialog/releases) page.

At the time of this writing, releasing binaries is not yet an automated process with GitHub actions,
so the steps below will need to be done manually.

#### GH CLI
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

#### Create release
1. Update (increase) version with `inv build.version`.
2. Create and merge a new PR called _"Release 1.2.3"_.  
3. Run `inv build.release`
   Use the `--notes` or `--notes-file` to add more details to the release.  

!!! Note "Recommended command"

    Create the file `release_notes.md` and _don't_ add it to the project (it's in `.gitignore`, so
    you should be ok).

    ```
    inv build.release --notes-file release_notes.md
    ```

#### Upload artifacts
**TODO**

### Publish to Pypi
```
inv build.publish
```

!!! Note

    There's a similarly named project in Pypi called
    [`showdialog`](https://pypi.org/project/showdialog/), so the initially chosen names of
    `show-dialog` and `show_dialog` were not possible due to the similar name and Pypi didn't allow
    it, so ended up with the current `qt-show-dialog`.

## More info
[Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
