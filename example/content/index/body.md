# oven

Yet another static site generator with markdown

## Why

I hate new-age web. Tons of JS, CSS frameworks and bloat bloated by bloated bloat. I like my web simple.

## Features

* Generation from .md files using Jinja2 templating
* Support for multi-lang site with .po files
* Support for custom:
    * Jinja filters
    * Markdown extension
    * Pre/Post build python scripts
* No bloat, Markdown transforms into HTML

## Usage

Please check out project's ```README.md``` [file](https://github.com/ktxyz/oven/blob/master/README.md) for more details about usage and configuration.

Using oven is very simple. 

To generate the site simply run
```bash
~ oven build
```
in the root directory of your site.

### Translations

Translations are automatically loaded from .po files in configured directory.

In order to generate/update those files with new translations simply run
```bash
~ oven gather
```
in the root directory of your site.