# Page Update Monitor

A simple CLI tool to monitor web page updates.

Register any web page and check whether it has changed since the last time you checked.
You can monitor the entire page or specific elements using CSS selectors.

- [Page Update Monitor](#page-update-monitor)
  - [Features](#features)
  - [Installation](#installation)
  - [Setup (Recommended)](#setup-recommended)
  - [Usage](#usage)
  - [Commands](#commands)
    - [See help](#see-help)
    - [Check for updates](#check-for-updates)
    - [Add a website](#add-a-website)
    - [List websites](#list-websites)
    - [Remove a website](#remove-a-website)
    - [Show version](#show-version)
  - [How It Works](#how-it-works)
  - [Data Storage](#data-storage)
  - [Example Workflow](#example-workflow)
  - [Requirements](#requirements)
  - [Dependencies](#dependencies)

---

## Features

* Monitor full web pages for changes
* Monitor specific elements using CSS selectors
* Simple and intuitive CLI
* Lightweight (no browser required)
* Local JSON storage (no database needed)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourname/page-update-monitor.git
cd page-update-monitor
```

---

## Setup (Recommended)

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

All commands are executed via:

```bash
python run.py [COMMAND]
```

You can also check the version globally:

```bash
python run.py --version
python run.py -v
```

---

## Commands

### See help
```bash
python run.py --help
```
--- 
### Check for updates

```bash
python run.py check
```

Checks all registered websites and reports changes.

---

### Add a website

```bash
python run.py add
```

You will be prompted to enter:

* Site name
* URL
* Mode:

  * `full` (default): monitor the entire page
  * `selector`: monitor a specific HTML element

If you choose selector mode, enter a CSS selector.

Examples:

```
#main
.content
```

The tool will validate the selector and show a preview:

```
[OK] #main -> <content preview>...
```

---

### List websites

```bash
python run.py list
```

With details:

```bash
python run.py list -d
```

---

### Remove a website

```bash
python run.py remove [name]
```

Alias:

```bash
python run.py rm [name]
```

Example:

```bash
python run.py rm example-site
```

---

### Show version

```bash
python run.py version
```

Or:

```bash
python run.py --version
python run.py -v
```

---

## How It Works

* Fetches HTML using `requests`
* Parses content with `BeautifulSoup`
* Stores previous results locally
* Compares current content with the last snapshot

If a difference is detected, it reports an update.

---

## Data Storage

Registered sites are stored in:

```
data/sites.json
```

---

## Example Workflow

```bash
python run.py add
python run.py list
python run.py check
```

---

## Requirements

* Python 3.10+
* See `requirements.txt` for full dependencies

---

## Dependencies

* typer
* requests
* beautifulsoup4
* rich
