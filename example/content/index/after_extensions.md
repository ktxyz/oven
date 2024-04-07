### Scripts
You can define scripts in the `script_dir` folder, that will be automatically detected.
For now, they are executed before/after the site is generated, but I have an idea of creating markings for different
pipeline stages that scripts could register themselves in.

In config file you can specify custom script configuration, that will be passed to `execute_script` function as `**kwargs`:
```json
{
  "scripts_config": {
    "robots.txt": {
      "output_file": "robots.txt"
    },
    "sitemap.xml": {
      "ignore_paths": [
        "_archive"
      ]
    },
    "clean": {
      "ignore_paths": [
        "_archive"
      ]
    },
    "archive": {
      "ignore_paths": [
        "_archive"
      ],
      "generate_zip": true,
      "zip_dir": "_archive",
      "generate_raw": true,
      "raw_dir": "_archive"
    },
    "assets": {
      "ignore_paths": [
        "build"
      ],
      "types": [
        ".css",
        ".js",
        ".png",
        ".otf",
        ".pdf",
        ".svg"
      ]
    }
  }
}
```

List of internally shipped extensions:
* `archive` - script that creates archives of built page, either as .zip files or as accessible in `build_dir` raw copies.
* `assets` - scripts that gathers and copies static files into the `build_dir`.
* `clean` - script that performs cleaning before building the site.
* `robots.txt` - script creates `robots.txt` file after build is complete.
* `sitemap.xml` - script creates `sitemap.xml` file after build is complete.

#### Example
This is an example script in the ```oven/internal_scripts/sitemap.py``` file. It generates `sitemap.xml` file after the
site has been generated.

