import re
import warnings
from collections import namedtuple

from url_parser.public_suffix_list import PublicSuffixList

UrlObject = namedtuple(
    'UrlObject', [
        'protocol',
        'www',
        'sub_domain',
        'domain',
        'top_domain',
        'path',
        'dir',
        'file',
        'fragment',
        'query'
    ])


def _split_query_group(query_groups: list) -> dict:
    result = dict()

    for query_group in query_groups:
        query = query_group.split('=')

        if len(query) == 1:
            result[query[0]] = None
            continue

        result[query[0]] = query[1]

    return result


def _parse_url_with_top_domain(url, top_domain):
    regex = r"^(?:(?P<protocol>[\w\d]+)(?:\:\/\/))?" \
                  r"(?P<sub_domain>" \
                  r"(?P<www>(?:www)?)(?:\.?)" \
                  r"(?:(?:[\w\d-]+|\.)*?)?" \
                  r")(?:\.?)" \
                  r"(?P<domain>[^./]+(?=\.))\." \
                  r"(?P<top_domain>" + re.escape(top_domain) + r"(?![^/?#]))" \
                  r"(?P<path>" \
                  r"(?P<dir>\/(?:[^/\r\n]+(?:/))+)?" \
                  r"(?:\/?)(?P<file>[^?#\r\n]+)?" \
                  r")?" \
                  r"(?:\#(?P<fragment>[^#?\r\n]*))?" \
                  r"(?:\?(?P<query>.*(?=$)))*$"

    dict_data = {
        'protocol': None,
        'www': None,
        'sub_domain': None,
        'domain': None,
        'top_domain': None,
        'path': None,
        'dir': None,
        'file': None,
        'fragment': None,
        'query': None,
    }

    match = re.search(regex, url)

    dict_data['protocol'] = match.group('protocol') if match.group('protocol') else None
    dict_data['www'] = match.group('www') if match.group('www') else None
    dict_data['sub_domain'] = match.group('sub_domain') if match.group('sub_domain') else None
    dict_data['domain'] = match.group('domain')
    dict_data['top_domain'] = top_domain
    dict_data['path'] = match.group('path') if match.group('path') else None
    dict_data['dir'] = match.group('dir') if match.group('dir') else None
    dict_data['file'] = match.group('file') if match.group('file') else None
    dict_data['fragment'] = match.group('fragment') if match.group('fragment') else None

    query = match.group('query') if match.group('query') else None

    if query is not None:
        query_groups = query.split('&')
        query = _split_query_group(query_groups)
        dict_data['query'] = query

    return dict_data


def _parse_url_with_public_suffix(url):
    public_suffix = PublicSuffixList.get_list()
    public_suffix.sort()

    domain_regex = r"(?:^|\/)(?P<domain>[^:/#?]+)(?:[/#?]|$)"
    match = re.search(domain_regex, url)
    domain = match.group('domain')
    domain_parts = domain.split('.')

    top_domain = None

    for i in range(len(domain_parts)):
        tail_gram = domain_parts[i:len(domain_parts)]
        tail_gram = '.'.join(tail_gram)

        if tail_gram in public_suffix:
            top_domain = tail_gram
            break

    data = _parse_url_with_top_domain(url, top_domain)

    return data


def get_base_url(url: str) -> str:
    url = get_url(url)
    protocol = str(url.protocol) + '://' if url.protocol is not None else 'http://'
    www = 'www.' if url.www is not None else ''
    sub_domain = str(url.sub_domain) + '.' if url.sub_domain is not None and url.sub_domain != 'www.' else ''
    return protocol + www + sub_domain + url.domain + '.' + url.top_domain


def get_url(url: str) -> UrlObject:
    data = _parse_url_with_public_suffix(url)

    object_data = UrlObject(
        protocol=data['protocol'],
        www=data['www'],
        sub_domain=data['sub_domain'],
        domain=data['domain'],
        top_domain=data['top_domain'],
        path=data['path'],
        dir=data['dir'],
        file=data['file'],
        fragment=data['fragment'],
        query=data['query'],
    )

    return object_data


def parse_url(url: str) -> dict:
    warnings.warn(
        "parse_url is deprecated, use get_url instead",
        DeprecationWarning
    )

    data = get_url(url)
    return data._asdict()
