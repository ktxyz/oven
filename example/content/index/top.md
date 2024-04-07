# oven
Yet another static site generator powered by markdown, because I didn't like the other stuff

It tries to follow the [K.I.S.S](https://en.wikipedia.org/wiki/KISS_principle) principle.

## Installation
For now there is no python package that can be installed. Use repository instead.

## Usage
### Config
#### Site configuration
Oven loads configuration from `oven.json` file. All the options are optional. Config is provided to every jinja2 template as `config` object.
Configured directories unless specified otherwise will be used relative to `CWD`.

##### `source_dir`
Specifies directory with site source files.
##### `build_dir`
Specifies directory of the built site output.
##### `static_dir`
Specifies subdirectory inside `build_dir` that will contain all the static assets.
##### `theme_dir`
Specifies directory with jinja2 templates.
##### `default_template_name`
Specifies default template used with pages that don't override this themselves.
##### `locales_dir`
Specifies directory with .po files containing translations.
##### `locales_main`
Specifies main (default) language for the site.
##### `locales_langs`
Specifies all languages in which the site should be translated (should include the main as well)
##### `filters_dir`
Specifies directory with custom filters (see below).
##### `enabled_filters`
Specifies enabled filters. If empty all found filters will be enabled.
##### `scripts_dir`
Specifies directory with custom scripts (see below).
##### `enabled_scripts`
Specifies enabled scripts. If empty all found scripts will be enabled.
##### `extensions_dir`
Specifies directory with custom markdown extensions (see below).
##### `enabled_extensions`
Specifies enabled extensions. If empty all found extensions will be enabled.
##### `site_url`
Specifies url for the site.
##### `site_timezone`
Specifies timezone used for the site.

#### Page configuration
Every page can be additionally configured by providing `config.json` file in its directory.
##### `template_name`
Overrides template file used for the page
##### `output_name`
Overrides output directory of the page (by default it will be the same as source).

### Gathering
```bash
python -m oven gather
```

### Building
```bash
python -m oven build
```

## Features
### Generating
Oven iterates over directories in `source_dir`. Every page should have its own, separate folder containing `.md` files and optional `context.json` and `config.json` files.

Each `.md` file will be passed to template as a context variable, named like the file.

### Translations
Oven has built-in translation features. It uses `.po` files. You can update them with `gather`, which gathers texts from .md files and all templates.

For now there is no support for localized assets.

### Filters
Custom jinja2 filters can be defined in the `filters_dir` folder. Every filter should be a separate python file
that defines the filter function named `custom_filter` and a variable containing the name of the filter named `FILTER_NAME`.

List of internally shipped filters:
* `get_text` - provides integration with oven translation both during gather and build.
* `get_url` - provides integration with resolving urls for oven pages and static files.

##### Example
This is an example custom filter from `oven/internal_scripts/curent_time.py` file.

