# Python URL Parser
![PyPI - Format](https://img.shields.io/pypi/format/url-parser)
![PyPI - Status](https://img.shields.io/pypi/status/url-parser)
![Downloads](https://pepy.tech/badge/url-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/url-parser)

A nice package to help you parse all types of URL's in vanilla python and return the parsed URL in groups.<br />

To not brake the API `parse_url` (returns a dict) still works and we made `get_url` to get the url parts as as object instead.

In version 2.1 we also included `get_basic_url` a small yet neat function to get a the main url back from a string

### Installation
```
pip install url-parser
```

### Usage

```python
from url_parser import parse_url, get_url, get_base_url


url = parse_url('https://open.prospecta.app/my_user_login?user=url-parser&password=H3ll0') # returns url sections as a dict  
url_object = get_url('https://open.prospecta.app/my_user_login?user=url-parser&password=H3ll0') # Does the same, bur returns a object  
basic_url = get_base_url('https://open.prospecta.app/my_user_login?user=url-parser&password=H3ll0') # Returns just the main url  

print(url['domain']) # Outputs -> prospecta  
print(url_object.domain) # Outputs -> prospecta  
print(basic_url) # Outputs -> https://open.prospecta.app  
```

### Keywords `get_url` and `parse_url`

When using the `parse_url` and `get_url` function, you get a dict (parse_url) or object (get_url) back with different parts of the URL.

The different parts can be accessed by keywords:<br />
For `parse_url` use: `result['top_domain]`<br />
For `get_url` use: `result.top_domain`


Here is a list of all the available keywords:

| Keyword | Desription | Value when not present in URL
| ------ | ------ | ------ |
| protocol | The protocol, e.g. **https** or **ftp** | None
| www | Returns **www** if www is used in the URL | None
| sub_domain | The sub domain, e.g. **my.subdomain** in **my.subdomain.example.com**. Note that the sub domain also includes www. | None
| domain | The domain, e.g. **example** in **example.com** | Is always present
| top_domain | The domain, e.g. **com** in **example.com** | Is always present
| dir | The directory, e.g. **/my/directory/** in **example.com/my/directory/** | None
| file | The file, e.g. **my_file.js** in **example.com/home/my_file.js** | None
| path | The full path, e.g. **/home/my_file.js** in **example.com/home/my_file.js** | None
| fragment | The URL fragment, e.g. **my_link** in **example.com#my_link** | None
| query | The URL query, e.g. **my_parameter=1&foo=bar** in **example.com?my_parameter=1&foo=bar** | None

### Testing

Use the following command to run tests.

```bash
python -m unittest url_parser.tests.test_url_parser
```

### Changelog:

See CHANGELOG.md
