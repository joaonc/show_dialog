# `src/ui/forms` folder
The files in this folder are created with PySide tools and should not be edited manually or with
linters.

## `ui_*.py` files
Generated from the `.ui` files under `/assets/ui`.

Uses the tool `pyside6-uic` and generated with the command
```
inv ui.py -f <filename>

# Ex
inv ui.py -f show_dialog
```

`inv --help ui.py` for more details.

## `resources_rc.py` file
Resources added in the UI builder.

Generated from the `.qrc` files under `/assets`.

Uses the tool `pyside6-rcc` and generated with the command
```
inv ui.rc
```
