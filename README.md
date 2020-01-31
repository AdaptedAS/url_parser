# URL Parser
![PyPI - Format](https://img.shields.io/pypi/format/url-parser)
![PyPI - Status](https://img.shields.io/pypi/status/url-parser)
![Downloads](https://pepy.tech/badge/url-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/url-parser)

A small yet nice package to help you parse all types of URL's and return the parsed URL in groups.
### Installation
```
pip install url-parser
```

### Usage

```python
from url_parser import parse_url


url = parse_url('https://open.prospecta.app/my_user_login?user=url-parser&password=H3ll0')

print(url)

# Outputs: {'protocol': 'https', 'www': None, 'sub_domain': 'open', 'domain': 'prospecta', 'top_domain': 'app', 'dir': None, 'file': 'my_user_login', 'fragment': None, 'query': {'user': 'url-parser', 'password': 'H3ll0'}, 'path': '/my_user_login'}
```

### Keywords

When using the `parse_url` function, you get a dict back with different parts of the URL.

The different parts can be accessed by keywords like this: `result['top_domain]`

Here is a list of all the available keywords:

| Keyword | Desription | Value when not present in URL
| ------ | ------ | ------ |
| protocol | The protocol, e.g. **https** or **ftp** | `None`
| www | Returns **www** if www is used in the URL | None
| sub_domain | The sub domain, e.g. **my.subdomain** in **my.subdomain.example.com**. Note that the sub domain also includes www. | None
| domain | The domain, e.g. **example** in **example.com** | Is always present
| top_domain | The domain, e.g. **com** in **example.com** | Is always present
| dir | The directory, e.g. **/my/directory/** in **example.com/my/directory/** | None
| file | The file, e.g. **my_file.js** in **example.com/home/my_file.js** | None
| path | The full path, e.g. **/home/my_file.js** in **example.com/home/my_file.js** | None
| fragment | The URL fragment, e.g. **my_link** in **example.com#my_link** | None
| query | The URL query, e.g. **my_parameter=1&foo=bar** in **example.com?my_parameter=1&foo=bar** | None

#### Usage with keywords

Here is an example of using keywords.

```python
from url_parser import parse_url


url = parse_url('https://open.prospecta.app/my_user_login?user=url-parser&password=H3ll0')

print(url)
# Outputs: {'protocol': 'https', 'www': None, 'sub_domain': 'open', 'domain': 'prospecta', 'top_domain': 'app', 'dir': None, 'file': 'my_user_login', 'fragment': None, 'query': {'user': 'url-parser', 'password': 'H3ll0'}, 'path': '/my_user_login'}

protocol = url['protocol']
sub_domain = url['sub_domain']
domain = url['domain']
top_domain = url['top_domain']
file = url['file']
query = url['query']

print(protocol)
# Outputs: https

print(sub_domain)
# Outputs: open

print(domain)
# Outputs: prospecta

print(top_domain)
# Outputs: app

print(file)
# Outputs: 'my_user_login'

print(query)
# Outputs: {'user': 'url-parser', 'password': 'H3ll0'}
```

### Testing

Use the following command to run tests.

```bash
python -m unittest url_parser.tests.test_url_parser.TestUrlParser
```


#### Versions:
v 2.0.0 | Added new regex and support for foreign languages  
v 1.0.0 | Small bugfixes and optimisation for stable release  
v 0.9.9 | Bugfixes on the readme file.  
v 0.9.8 | Added support for args.  
v 0.9.7 | Changed setup.py and readme for PyPi optimisation.  
v 0.9.6 | Added support for secondary top domain (like: co.uk, .parliament.uk, .gov.au).
