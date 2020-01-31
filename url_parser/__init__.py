import re


def _split_query_group(query_groups: list) -> dict:
    result = dict()

    for query_group in query_groups:
        query = query_group.split('=')

        if len(query) == 1:
            result[query[0]] = None
            continue

        result[query[0]] = query[1]

    return result


def parse_url(item):
    url_data = {
        'protocol': None,
        'www': None,
        'sub_domain': None,
        'domain': None,
        'top_domain': None,
        'dir': None,
        'file': None,
        'fragment': None,
        'query': None,
    }

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

    match = re.search(regex, item)

    url_data['domain'] = match.group('domain')
    url_data['top_domain'] = match.group('top_domain')

    url_data['protocol'] = match.group('protocol') if match.group('protocol') else None
    url_data['www'] = match.group('www') if match.group('www') else None
    url_data['sub_domain'] = match.group('sub_domain') if match.group('sub_domain') else None
    url_data['path'] = match.group('path') if match.group('path') else None
    url_data['dir'] = match.group('dir') if match.group('dir') else None
    url_data['file'] = match.group('file') if match.group('file') else None
    url_data['fragment'] = match.group('fragment') if match.group('fragment') else None

    query = match.group('query') if match.group('query') else None

    if query is not None:
        query_groups = query.split('&')
        queries = _split_query_group(query_groups)
        url_data['query'] = queries

    return url_data
