# Yesss Bill Downloader

A Scrapy-based tool to download your monthly bills from yesss.at.

This script uses a KeePass database to securely store and retrieve the login credentials for your yesss.at account(s).

The files are stored under /tmp/yesss (could be change by a commandline option or a PATH variable) in the following structure

```
/tmp/
  -- yesss/
     -- <username>
        -- <year>
           -- <date>-rechnung.pdf
           -- <date>-einzelgesprächsnachweis.pdf
```

## Prerequisites

*   **Python 3.12+**
*   **direnv** (recommended for automatic environment management).
*   A **KeePass (`.kdbx`) database file**. The script searches for entries with the following properties:
    *   **URL:** `https://www.yesss.at/kontomanager.php`
    *   The **Username** field should contain your yesss.at phone number.
    *   The **Password** field should contain your yesss.at password.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd yesss-bill-downloader
    ```

2.  **Set up the environment:**
    This project uses direnv to automatically manage the Python virtual environment.

    Once you have `direnv` installed, run the following command in the project directory:
    ```bash
    direnv allow
    ```
    This will create and activate the virtual environment for you.

    If you do not use `direnv`, you can create and activate the virtual environment manually:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the project in editable mode:**
    This will install all the required dependencies and make the `yesss-downloader` command available in your environment.
    ```bash
    pip install -e .
    ```

## Usage

Once installed, you can run the downloader from your terminal. The script will prompt for your KeePass password if you don't provide it as an argument.

```bash
yesss-downloader
```

### Command-line Options

| Argument | Description | Default |
|---|---|---|
| `--keyfile <path>` | Path to your KeePass (`.kdbx`) file. | `~/keys.kdbx` |
| `--output <dir>` | The directory where the downloaded bills will be saved. | `/tmp/yesss` |
| `-p`, `--password <pass>` | The password for your KeePass file. If not provided, you will be prompted to enter it securely. | `None` |
| `-v`, `--verbose` | Enable verbose (DEBUG level) logging. | `False` |

### Example

```bash
yesss-downloader --keyfile /secure/my_keys.kdbx --output ~/Documents/Bills/Yesss
```
