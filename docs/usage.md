# Usage
## Library
**TODO**

### Logging
**TODO**

## Shortcuts
The following shortcuts are available:

| Shortcut   |                  |
|------------|------------------|
| `Ctrl`+`Q` | Exit as failure  |
| `Ctrl`+`P` | Exit as pass     |
| `+`        | Increase timeout |

!!! Note

    The `Esc` key is disabled in order to prevent accidentally dismissing the dialog.

## Executable
This section applies to both the executable app and the CLI script after pip installing the package.

**TODO**

### Exit codes
| Exit code |                                                    |
|:---------:|----------------------------------------------------|
|    `0`    | Pass                                               |
|    `1`    | Fail. The _Fail_ button was clicked.               |
|    `2`    | Fail. App was exited in the `X` button.            |
|    `3`    | Fail. Timeout and input `timeout_pass` is `False`. |

