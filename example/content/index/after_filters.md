### Extensions
You can define custom markdown extensions in the `extensions_dir` folder. Additional extension names, not found by the oven system, will be passed directly.

List of internally shipped extensions:
* `oven_urls` - Extension replaces non-absolute urls with jinja2 filter `get_url` that handles resolving them.

#### Example
This is an example extension in the ```oven/internal_extensions/oven_urls.py``` file that changes urls into custom resolved ones.
