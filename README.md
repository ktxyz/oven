# oven
Yet another static site generator powered by markdown, because I didn't like the other stuff

It tries to follow the [K.I.S.S](https://en.wikipedia.org/wiki/KISS_principle) principle.

## Installation

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
Specifies subdirectory inside `build_dir` that will contain all the static assets. Also, possible are subdirectories: `static_dir_css`, `static_dir_img`, `static_dir_js` and `static_dir_misc`
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
##### `scripts_dir`
Specifies directory with custom scripts (see below).

#### Page configuration
Every page can be additionally configured by providing `config.json` file in its directory.
##### `template_name`
Overrides template file used for the page
##### `output_name`
Overrides output directory of the page (by default it will be the same as source).

### Templates

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
### Translations
### Custom Filters
Custom jinja2 filters can be defined in the `filters_dir` folder. Every filter should be a separate python file
that defines the filter function named `custom_filter` and a variable containing the name of the filter named `FILTER_NAME`.

##### Example
This is an example custom filter from `example/filters/curent_time.py` file.

```python

```

### Scripts
You can define scripts in the `script_dir` folder, that will be automatically detected.
For now, they are executed after the site is generated, but I have an idea of creating markings for different
pipeline stages that scripts could register themselves in.

#### Example
This is an example script in the ```example/scripts/sitemap.py``` file. It generates `sitemap.xml` file after the
site has been generated.

```python

```

## Issues
### Usability
Code and features flexibility is a bit iffy from UX standpoint. This should be resolved over time, as I use the system
and expand on it more.
### Performance
There are areas in code where unnecessary work is done. Some parts of it can be optimized by simply having a better architecture.

## Contributions
I'm very open to contributions for anything: features, enhancements or refactors.
If some code seems ~~stupid~~ like it use an improvement please don't hesitate to add a new issue
or pull request yourself if you will.

