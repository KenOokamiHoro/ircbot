import asyncio

from .common import Get
from .tool import html, addstyle

# html parse


@asyncio.coroutine
def arxiv(arg, send):
    print('arxiv')

    arg.update({
        'n': arg['n'] or '5',
        'url': 'http://arxiv.org/search',
        'xpath': '//*[@id="dlpage"]/dl/dt',
    })
    params = {'query': arg['query'], 'searchtype': 'all'}
    field = [
        ('./span/a[1]', 'text', '{}'),
        ('./following-sibling::dd[1]/div/div[1]/span', 'tail', '{}'),
    ]
    def format(l):
        return map(lambda e: '[\\x0302{0}\\x0f] {1}'.format(e[0][6:], e[1]), l)

    return (yield from html(arg, [], send, params=params, field=field, format=format))


@asyncio.coroutine
def zhihu(arg, send):
    print('zhihu')

    def image(e):
        for ns in e.xpath('.//noscript'):
            ns.getparent().remove(ns)
        for img in e.xpath('.//img'):
            src = img.attrib.get('data-actualsrc')
            if src:
                img.tail = ' [\\x0302 {0} \\x0f] '.format(src) + (img.tail or '')
        return e

    arg.update({
        'n': '1',
        'xpath': '//*[@id="zh-question-answer-wrap"]/div/div[3]/div',
    })
    get = lambda e, f: addstyle(image(e)).xpath('string()')

    return (yield from html(arg, [], send, get=get))


@asyncio.coroutine
def pm25(arg, send):
    print('pm25')

    city = {
        '北京': '1',
        '成都': '2',
        '广州': '3',
        '上海': '4',
        '沈阳': '5',
    }

    try:
        location = city[arg['city']]
    except:
        send('只有如下城市: ' + ', '.join(city.keys()))
        return

    arg.update({
        'n': '1',
        'url': 'http://www.stateair.net/web/post/1/{0}.html'.format(location),
        'xpath': '//*[@id="content"]/div[2]/div[1]/div/div[3]/table/tbody',
    })
    field = [('./' + x, '', '{}') for x in ['tr[3]/td', 'tr[2]/td', 'tr[5]//span', 'tr[1]//span']]
    def format(l):
        e = list(l)[0]
        return [', '.join(e).replace('\n', '')]

    return (yield from html(arg, [], send, field=field, format=format))


@asyncio.coroutine
def btdigg(arg, send):
    print('btdigg')

    arg.update({
        'n': str(int(arg['n'] or '1') * 2),
        'url': 'http://btdigg.org/search',
        'xpath': '//*[@id="search_res"]/table/tbody/tr',
    })
    params = {'info_hash': '', 'q': arg['query']}
    #field = [('./td/table[1]//a', 'text_content', '\\x0304{}\\x0f'), ('./td/table[2]//td[not(@class)]', 'text_content', '{}'), ('./td/table[2]//td[1]/a', 'href', '[\\x0302 {} \\x0f]')]
    # magnet link
    field = [
        ('./td/table[1]//a', '', '\\x0300{}\\x0f'),
        ('./td/table[2]//td[not(@class)]', '', '{}'),
        ('./td/table[2]//td[1]/a', 'href', '\\x0302{}\\x0f'),
    ]

    def format(l):
        line = []
        for e in l:
            line.append(' '.join(e[:2]))
            line.append(e[2])
        return line

    return (yield from html(arg, [], send, params=params, field=field, format=format))


@asyncio.coroutine
def man(arg, send):
    print('man')

    section = arg['section'].lower() if arg['section'] else arg['section']
    name = arg['name'].lower()

    url = 'http://linux.die.net/man/'
    if not section:
        a = {
            'n': '1',
            'url': url + '{0}.html'.format(name[0] if 'a' <= name[0] and name[0] <= 'z' else 'other'),
            'xpath': '//*[@id="content"]/dl/dt/a[starts-with(text(), "{0}")]'.format(name),
        }
        print(a)
        f = [('.', 'href', '{}')]
        get = Get()
        yield from html(a, [], get, field=f)
        path = get.line[0]
    else:
        path = '{0}/{1}'.format(section, name)

    arg.update({
        'n': '1',
        'url': url + path,
        'xpath': '//head',
    })
    field = [
        ('./title', '', '{}'),
        ('./base', 'href', '[\\x0302 {} \\x0f]'),
        ('./meta[@name = "description"]', 'content', '{}'),
    ]

    return (yield from html(arg, [], send, field=field))


@asyncio.coroutine
def gauss(arg, send):
    print('gauss')

    arg.update({
        'n': arg['n'] or '1',
        'url': 'http://www.gaussfacts.com/random',
        'xpath': '//*[@id="wrapper"]/div/p/a[@class="oldlink"]',
    })

    return (yield from html(arg, [], send))

func = [
    (zhihu          , r"zhihu\s+(?P<url>http\S+)"),
    (pm25           , r"pm2.5\s+(?P<city>.+)"),
    (btdigg         , r"btdigg\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (man            , r"man(\s+(?P<section>[1-8ln]))?\s+(?P<name>.+)"),
    (gauss          , r"gauss(\s+#(?P<n>\d+))?"),
    (arxiv          , r"arxiv\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
]
