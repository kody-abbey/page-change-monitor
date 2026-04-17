# Page Update Monitor

A simple CLI tool to monitor web page updates.

Register any web page and check whether it has changed since the last time you checked.
You can monitor the entire page or specific elements using CSS selectors.
---
- [Page Update Monitor](#page-update-monitor)
  - [You can monitor the entire page or specific elements using CSS selectors.](#you-can-monitor-the-entire-page-or-specific-elements-using-css-selectors)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
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
  - [Development](#development)

---

## Features

* Monitor full web pages for changes
* Monitor specific elements using CSS selectors
* Simple and intuitive CLI
* Lightweight (no browser required)
* Local JSON storage (no database needed)

---

## Installation

Install via pip:

```bash
pip install page-update-monitor
```

---
## Quick Start

```bash
pip install page-update-monitor
pum add
pum check
```

## Usage

```bash
pum [COMMAND]
```

Check version:

```bash
pum --version
pum -v
```

---

## Commands

### See help

```bash
pum --help
```

---

### Check for updates

```bash
pum check
```

Checks all registered websites and reports changes.

---

### Add a website

```bash
pum add
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
pum list
```

With details:

```bash
pum list -d
```

---

### Remove a website

```bash
pum remove [name]
```

Alias:

```bash
pum rm [name]
```

Example:

```bash
pum rm example-site
```

---

### Show version

```bash
pum version
```

Or:

```bash
pum --version
pum -v
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

Configuration files are stored in the user config directory:

* Linux: `~/.config/page-update-monitor/`
* macOS: `~/Library/Application Support/page-update-monitor/`
* Windows: `%APPDATA%/page-update-monitor/`

---

## Example Workflow

```bash
pum add
pum list
pum check
```

---

## Requirements

* Python 3.10+

---

## Dependencies

* typer
* requests
* beautifulsoup4
* rich

---

## Development

Clone the repository:

```bash
git clone https://github.com/yourname/page-update-monitor.git
cd page-update-monitor
pip install -e .
```
