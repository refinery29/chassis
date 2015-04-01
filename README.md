# Chassis
### Opinionated REST Framework.

Chassis is Refinery29's framework layer on top of Tornado for rapidly building
performant, self-documenting JSON-based REST APIs.

# Developing

## Git Flow
This project follows the [Git Flow model](http://nvie.com/posts/a-successful-git-branching-model/) with slashes ('/') separating tokens in branch names.

 * master is for tagged releases
 * develop has all the changes for the next releases
 * feature/____ branches are branched off of develop and merged back into develop
 * release/#.#.# branches are branched off of develop and merged into master
 * hotfix/____ branches are branched off of master and merged into both master and develop
 * experimental/____ branches are branched off of develop. These can ONLY be merged into feature branches.

## Tools

Install the development dependencies:

```bash
cd chassis
pip install -r development.txt
```

### Linter

Your code must pass the linter with no errors.

 ```bash
 cd chassis
 python tools/lint.py
```

### Tests

You can run the test with

```bash
cd chassis
nosetests
```

Or use sniffer to watch for changes and run the tests automatically

```bash
cd chassis
sniffer
```
