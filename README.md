# Chassis

Chassis is Refinery29's framework layer on top of Tornado for rapidly building
performant, self-documenting JSON-based REST APIs.

## Contents
* [Developing](#developing)
 * [Git Flow](#developing-git-flow)
 * [Tools](#developing-tools)
 * [Linter](#developing-linter)
 * [Tests](#developing-tests)
* Services
 * [Dependency Resolver, Creation, and Injection](doc/dependency_injection_service_resolver.md)


# <a name="developing"></a>Developing

## <a name="developing-git-flow"></a>Git Flow
This project follows the [Git Flow model](http://nvie.com/posts/a-successful-git-branching-model/) with slashes ('/') separating tokens in branch names.

 * master is for tagged releases
 * develop has all the changes for the next releases
 * feature/____ branches are branched off of develop and merged back into develop
 * release/#.#.# branches are branched off of develop and merged into master
 * hotfix/____ branches are branched off of master and merged into both master and develop
 * experimental/____ branches are branched off of develop. These can ONLY be merged into feature branches.

## <a name="developing-tools"></a>Tools

Install the development dependencies:

```bash
cd chassis
pip install -r development.txt
```

### <a name="developing-linter"></a>Linter

Your code must pass the linter with no errors.

```bash
 cd chassis
 python tools/lint.py
```

### <a name="developing-tests"></a>Tests

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
