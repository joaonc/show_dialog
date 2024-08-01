# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.7.2
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x01-\
/\
*\x0d\x0aDefault style\
.\x0d\x0a */\x0d\x0a\x0d\x0aQLabel\
#title_label {\x0d\x0a\
    color: blue;\
\x0d\x0a}\x0d\x0a\x0d\x0aQLabel#de\
scription_label \
{\x0d\x0a    color: rg\
b(0, 0, 50);\x0d\x0a}\x0d\
\x0a\x0d\x0aQPushButton#p\
ass_button {\x0d\x0a  \
  color : green;\
\x0d\x0a    /*backgrou\
nd-color : gray;\
*/\x0d\x0a}\x0d\x0a\x0d\x0aQPushBu\
tton#fail_button\
 {\x0d\x0a    color : \
red;\x0d\x0a    /*back\
ground-color : g\
reen;*/\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x0b\
\x0ck<\xf3\
\x00s\
\x00t\x00y\x00l\x00e\x00s\x00h\x00e\x00e\x00t\x00s\
\x00\x0c\
\x0dlO\xc3\
\x00s\
\x00t\x00y\x00l\x00e\x00_\x000\x001\x00.\x00c\x00s\x00s\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x91\x05\xee\xb9\xc6\
"


def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)


def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)


qInitResources()
