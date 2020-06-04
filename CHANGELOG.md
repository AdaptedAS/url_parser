### Changelog:

##### v3.0.0
* A lot of cleanup.
* Added list from https://publicsuffix.org/ to find top domains more correct.
* Breaking change: Signature of `parse_url(item)` now changed to `parse_url(url: str) -> dict`.
* Breaking change: Signature of `get_url(item)` now changed to `def get_url(url: str) -> UrlObject:`.

##### v2.1.1
* Small fix for readme and Github actions.

##### v2.1.0
* Added function to get url back as Object. Also added a function to get the basics of a url returned.

##### v2.0.0
* Added new regex and support for foreign languages.

##### v1.0.0
* Small bugfixes and optimisation for stable release.

##### v0.9.9
* Bugfixes on the readme file.

##### v0.9.8
* Added support for args.

##### v0.9.7
* Changed setup.py and readme for PyPi optimisation.

##### v0.9.6 
* Added support for secondary top domain (like: co.uk, .parliament.uk, .gov.au).
