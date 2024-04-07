#### Managing scripts from arguments
Some scripts should only be run from time to time, not for every build (like an archive script). We can manually override `enabled_scripts` configuration with arguments:

* `--enable-scripts` - comma seperated list of scripts names that will be appended to ones read from config
* `--disable-scripts` - comma seperated list of scripts names that will be removed from ones read from config
* `--force-scripts` - comma seperated list of scripts names that will override ones from config

## Issues
### Tests
There are no tests in place. I don't believe in unit testing...nah, I'm just a bit lazy. They'll come in time.
### Usability
Code and features flexibility is a bit iffy from UX standpoint. This should be resolved over time, as I use the system
and expand on it more.
### Performance
There are areas in code where unnecessary work is done. Some parts of it can be optimized by simply having a better architecture.

## Contributions
I'm very open to contributions for anything: features, enhancements or refactors.
If some code seems ~~stupid~~ like it use an improvement please don't hesitate to add a new issue
or pull request yourself if you will.

