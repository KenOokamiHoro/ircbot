import asyncio
from urllib.parse  import quote_plus

from .common import Get
from .tool import html, xml, addstyle, htmlparse
#from .tool import fetch, htmltostr, html, xml, addstyle, jsonparse, htmlparse

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
            ns.text = ''
        for img in e.xpath('.//img'):
            src = img.attrib.get('data-actualsrc')
            if src:
                if src[:2] == '//':
                    img.tail = ' [\\x0302 http:{0} \\x0f] '.format(src) + (img.tail or '')
                else:
                    img.tail = ' [\\x0302 {0} \\x0f] '.format(src) + (img.tail or '')
        return e

    arg.update({
        'n': '1',
        'xpath': '//*[@id="zh-question-answer-wrap"]//div[contains(@class, "zm-editable-content")]',
    })
    preget = lambda e: image(e)

    return (yield from html(arg, [], send, preget=preget))


@asyncio.coroutine
def bihu(arg, send):
    print('bihu')

    def image(e):
        for ns in e.xpath('.//noscript'):
            ns.text = ''
        for img in e.xpath('.//img'):
            img.tail = ' <img> ' + (img.tail or '')
        return e
    def bio(e):
        for t in e.xpath('.//*[@class="zu-question-my-bio"]'):
            t.text = ''
        for t in e.xpath('.//*[@class="zm-item-link-avatar"]/*'):
            t.getparent().remove(t)
        return e

    arg.update({
        'xpath': '//*[@id="zh-question-answer-wrap"]/div',
    })
    field = [
        #('./div[1]/button[1]/span[2]', 'text', '{}'),
        ('./div[1]/button[1]/span[1]', 'text', '{}'),
        #('./div[2]/div[1]/h3', '', '{}'),
        #('./div[2]/div[1]/*[contains(@class, "author-link") or contains(@class, "name")]', '', '{}'),
        ('.//span[contains(@class, "author-link-line")]/*[contains(@class, "author-link") or contains(@class, "name")]', '', '{}'),
        #('./div[3]/div', '', '{}'),
        ('./div[3]/div[contains(@class, "zm-editable-content")]', '', '{}'),
        ('./div[4]/div/span[1]/a', 'href', '{}'),
        ('./a[1]', 'name', '{}'),
    ]
    preget = lambda e: image(bio(e))
    def format(l):
        for e in l:
           vote = e[0]
           name = e[1].strip().strip('，')
           digest = e[2].strip()
           length = 70
           #if len(digest) > length:
           #    digest = digest[:length] + '...'
           digest = digest[:length] + '\\x0f...'
           digest = digest.replace('\n', ' ')
           link = '/' + e[3].split('/', 3)[-1]
           anchor = '#' + e[4]
           #yield '[\\x0304{0}\\x0f] \\x0300{1}:\\x0f {2} \\x0302{3}\\x0f \\x0302{4}\\x0f'.format(vote, name, digest, link, anchor)
           yield '[\\x0304{0}\\x0f] \\x16{1}:\\x0f {2} \\x0302{3}\\x0f \\x0302{4}\\x0f'.format(vote, name, digest, link, anchor)

    return (yield from html(arg, [], send, field=field, preget=preget, format=format))


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


@asyncio.coroutine
def foldoc(arg, send):
    print('foldoc')

    def clean(e):
        for s in e.xpath('.//script | .//style'):
            #s.getparent().remove(s)
            # don't remove tail
            s.text = ''
        for span in e.xpath('.//span[@class="mw-editsection"]'):
            span.getparent().remove(span)
        return e

    arg.update({
        'n': arg['n'] or '1',
        'url': 'http://foldoc.org/' + quote_plus(arg['query']),
        'xpath': '//*[@id="content"]/p',
    })

    get = lambda e, f: addstyle(clean(e)).xpath('string()')

    return (yield from html(arg, [], send, get=get))


@asyncio.coroutine
def wiki(arg, send):
    print('wiki')

    def clean(e):
        for s in e.xpath('.//script | .//style'):
            #s.getparent().remove(s)
            # don't remove tail
            s.text = ''
        for span in e.xpath('.//span[@class="mw-editsection"]'):
            span.getparent().remove(span)
        return e

    site = {
        # linux
        'arch': 'https://wiki.archlinux.org/',
        'gentoo': 'https://wiki.gentoo.org/',
        # wikipedia
        'zh': 'https://zh.wikipedia.org/w/',
        'classical': 'https://zh-classical.wikipedia.org/w/',
        'en': 'https://en.wikipedia.org/w/',
        'ja': 'https://ja.wikipedia.org/w/',
        # misc
        'poke': 'https://wiki.52poke.com/',
        #'pokemon': 'http://www.pokemon.name/w/',
    }

    try:
        url = site[arg['site'] or 'zh']
    except:
        raise Exception("Do you REALLY need this wiki?")

    arg.update({
        'n': arg['n'] or '1',
        'url': url + 'api.php',
        'xpath': '//page',
    })
    params = {
        'format': 'xml',
        'action': 'query',
        'generator': 'search',
        'gsrlimit': '1',
        'gsrwhat': 'nearmatch',
        'gsrsearch': arg['query'],
        'prop': 'revisions',
        'rvprop': 'content',
        'rvparse': '',
    }
    # don't select following nodes
    # script                 -> js
    # div and table          -> box, table and navbox
    # h2                     -> section title
    # preceding-sibling      -> nodes after navbox or MOEAttribute, usually external links
    def transform(l):
        if l:
            #pageid = l[0].get('pageid')
            return htmlparse(l[0].xpath('//rev')[0].text).xpath('//body/*['
                # filter script, style and section title
                #'not(self::script or self::style or self::h2)'
                #'not(self::div or self::table)'
                # or just select p and ul ?
                '(self::p or self::ul)'
                ' and '
                # select main part
                'not('
                'following-sibling::div[@class="infotemplatebox"]'
                ' or '
                'preceding-sibling::div[@class="MOEAttribute"]'
                ' or '
                'preceding-sibling::table[@class="navbox"]'
                ')'
                ']')
        else:
            raise Exception("oops...")

    get = lambda e, f: addstyle(clean(e)).xpath('string()')

    #return (yield from xml(arg, [], send, params=params, transform=transform, get=get))
    try:
        yield from xml(arg, [], send, params=params, transform=transform, get=get)
    except:
        params['gsrwhat'] = 'text'
        yield from xml(arg, [], send, params=params, transform=transform, get=get)


@asyncio.coroutine
def xkcd(arg, send):
    print('xkcd')

    # latest by default
    if arg['number'] == None:
        url = 'http://xkcd.com/'
    elif arg['number'] == 'random':
        url = 'http://c.xkcd.com/random/comic/'
    else:
        url = 'http://xkcd.com/{0}/'.format(arg['number'])

    arg.update({
        'n': '1',
        'url': url,
        'xpath': '//*[@id="comic"]//img',
    })
    field = [
        ('.', 'alt', '{}'),
        ('.', 'src', '[\\x0302 http:{} \\x0f]'),
        ('.', 'title', '{}'),
    ]

    return (yield from html(arg, [], send, field=field))


@asyncio.coroutine
def killteleboto(arg, send):
    print('killteleboto')

    return send('Avada Kedavra!\\x030', raw=True)


func = [
    (zhihu          , r"zhihu\s+(?P<url>http\S+)"),
    (bihu           , r"bihu\s+(?P<url>http\S+)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (pm25           , r"pm2.5\s+(?P<city>.+)"),
    #(btdigg         , r"btdigg\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (man            , r"man(\s+(?P<section>[1-8ln]))?\s+(?P<name>.+)"),
    (man            , r"woman(\s+(?P<section>[1-8ln]))?\s+(?P<name>.+)"),
    (gauss          , r"gauss(\s+#(?P<n>\d+))?"),
    (foldoc         , r"foldoc\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (arxiv          , r"arxiv\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (wiki           , r"wiki(?::(?P<site>\S+))?\s+(?P<query>.+?)(\s+(#(?P<n>\d+))?(\+(?P<offset>\d+))?)?"),
    (xkcd           , r"xkcd(\s+(?P<number>(\d+)|(random)))?"),
    (killteleboto   , r"killteleboto"),
]
