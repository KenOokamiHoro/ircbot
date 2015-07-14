import asyncio
import re
import json
from urllib.parse     import urlsplit

from .common import Get
from .tool import fetch, html, regex

@asyncio.coroutine
def getcode(url):
    site = {
        'codepad.org':         '/html/body/div/table/tbody/tr/td/div[1]/table/tbody/tr/td[2]/div/pre',
        'paste.ubuntu.com':    '//*[@id="contentColumn"]/div/div/div/table/tbody/tr/td[2]/div/pre',
        'cfp.vim-cn.com':      '.',
        'p.vim-cn.com':        '.',
        'www.fpaste.org':      '//*[@id="paste_form"]/div[1]/div/div[3]',
        'bpaste.net':          '//*[@id="paste"]/div/table/tbody/tr/td[2]/div',
        'pastebin.com':        '//*[@id="paste_code"]',
        'code.bulix.org':      '//*[@id="contents"]/pre',
        'ix.io':               '.',
        'dpaste.com':          '//*[@id="content"]/table/tbody/tr/td[2]/div/pre',
        'ideone.com':          '//*[@id="source"]/pre/ol/li/div',
        'pastebin.com':        '//*[@id="selectable"]/div/ol',
    }

    get = Get()
    u = urlsplit(url)
    xpath = site[u[1]]
    if xpath == '.':
        arg = {'url': url, 'regex': r'(.*)(?:\n|$)', 'n': '0'}
        yield from regex(arg, [], get)
    else:
        arg = {'url': url, 'xpath': xpath, 'n': '0'}
        yield from html(arg, [], get)

    return get.line

@asyncio.coroutine
def geturl(msg):
    reg = re.compile(r"(?P<method>GET|POST)\s+(?P<url>http\S+)(?:\s+(?P<params>\{.+?\}))?(?:\s+:(?P<content>\w+))?", re.IGNORECASE)
    arg = reg.fullmatch(msg)
    if arg:
        d = arg.groupdict()
        print(d)
        params = json.loads(d.get('params') or '{}')
        content = d.get('content')
        if content:
            r = yield from fetch(d['method'], d['url'], params=params, content='raw')
            #text = str(getattr(r, content.lower()) or '')
            text = str(getattr(r, content) or '')
        else:
            text = yield from fetch(d['method'], d['url'], params=params, content='text')
    else:
        raise Exception()

    return [text]

@asyncio.coroutine
def fetcher(msg):
    try:
        return (yield from getcode(msg))
    except:
        print('not paste bin')
        return (yield from geturl(msg))