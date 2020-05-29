import re
from collections import namedtuple

regex = r"(?:(?P<protocol>[\w\d]+)(?:\:\/\/))?" \
        r"(?P<sub_domain>" \
        r"(?P<www>(?:www)?)(?:\.?)" \
        r"(?:(?:[\w\d-]+|\.)*?)?" \
        r")(?:\.?)" \
        r"(?P<domain>[^./]+(?=\.))\." \
        r"(?P<top_domain>[^./]{2,3}(?:\.[^./]{2,3})?)(?=$|[/#?])" \
        r"(?P<path>" \
        r"(?P<dir>\/(?:[^/\r\n]+(?:/))+)?" \
        r"(?:\/?)(?P<file>[^?#\r\n]+)?" \
        r")?" \
        r"(?:\#(?P<fragment>[^#?\r\n]*))?" \
        r"(?:\?(?P<query>.*(?=$)))*"


def _split_query_group(query_groups: list) -> dict:
    result = dict()

    for query_group in query_groups:
        query = query_group.split('=')

        if len(query) == 1:
            result[query[0]] = None
            continue

        result[query[0]] = query[1]

    return result


def get_basic_url(item):
    url = get_url(item)
    protocol = str(url.protocol) + '://' if url.protocol is not None else 'http://'
    www = 'www.' if url.www is not None else ''
    sub_domain = str(url.sub_domain) + '.' if url.sub_domain is not None and url.sub_domain != 'www.' else ''
    return protocol + www + sub_domain + url.domain + '.' + url.top_domain


def get_url(item):
    Url_object = namedtuple(
        'Url_object', [
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

    match = re.search(regex, item)

    query = match.group('query') if match.group('query') else None

    if query is not None:
        query_groups = query.split('&')
        query = _split_query_group(query_groups)

    object_data = Url_object(
        protocol=match.group('protocol') if match.group('protocol') else None,
        www=match.group('www') if match.group('www') else None,
        sub_domain=match.group('sub_domain') if match.group('sub_domain') else None,
        domain=match.group('domain'),
        top_domain=match.group('top_domain'),
        path=match.group('path') if match.group('path') else None,
        dir=match.group('dir') if match.group('dir') else None,
        file=match.group('file') if match.group('file') else None,
        fragment=match.group('fragment') if match.group('fragment') else None,
        query=query
    )

    return object_data


def parse_url(item):
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

    match = re.search(regex, item)

    dict_data['domain'] = match.group('domain')
    dict_data['top_domain'] = match.group('top_domain')
    dict_data['protocol'] = match.group('protocol') if match.group('protocol') else None
    dict_data['www'] = match.group('www') if match.group('www') else None
    dict_data['sub_domain'] = match.group('sub_domain') if match.group('sub_domain') else None
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
