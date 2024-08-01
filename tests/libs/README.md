# Test libraries
Python modules with functionality used only by test cases.

## Resources file
The file `resources_rc.py` is a Qt
[resource](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QResource.html)
file, generated from `tests/assets/resources.qrc` (more info on `.qrc` files
[here](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html)).

If the `.qrc` file is updated, this file can be regenerated with the command below:
```
pyside6-rcc tests/assets/resources.qrc -o tests/libs/resources_rc.py
```
