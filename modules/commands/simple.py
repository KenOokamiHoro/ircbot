import asyncio
import time
import random
import math


@asyncio.coroutine
def echo(arg, send):
    #send(arg[0])
    send(arg['content'], raw=True)

@asyncio.coroutine
def say(arg, send):
    send(arg['content'])

@asyncio.coroutine
def ping(arg, send):
    send("ping!")
    #send("\\x0305ping!\\x0f")

@asyncio.coroutine
def pong(arg, send):
    send("pong!")

class ping2c():
    def __init__(self):
        self.i = 3
        self.tt = time.time()

    @asyncio.coroutine
    def __call__(self, arg, send):
       print(self.i)
       t = time.time()
       if t - self.tt > 20:
          self.tt = t
          self.i = 3
       elif self.i <= 0:
          send('好累啊...')
       if self.i == 1:
          send("\\x0304ping!!!!!!!!!\\x0f")
          self.i = self.i - 1
       elif self.i > 0:
          send("\\x0304ping!\\x0f")
          self.i = self.i - 1

ping2 = ping2c()

@asyncio.coroutine
def pia(arg, send):
    content = arg['content'] or ''

    face = [
        '°Д°',
        '・ω・',
        '・∀・',
        '‵-′',
        '￣▽￣',
        '・_・',
        '>∧<',
        '´∀`',
        '°_°',
        'ˊ_>ˋ',
    ]
    icon = '(╯{0})╯ ┻━┻ '.format(random.choice(face))
    if 'varia' not in content:
        send(icon + content)
    else:
        send(icon + '不要 pia 我!')

@asyncio.coroutine
def mua(arg, send):
    content = arg['content'] or ''

    if 'varia' not in content:
        send('o(*￣3￣)o ' + content)
    else:
        send('o(*￣3￣)o ' + '谢谢啦~')

@asyncio.coroutine
def color(arg, send):
    #c = [
    #    ('00', 'white'),
    #    ('01', 'black'),
    #    ('02', 'blue'),
    #    ('03', 'green'),
    #    ('04', 'red'),
    #    ('05', 'brown'),
    #    ('06', 'purple'),
    #    ('07', 'orange'),
    #    ('08', 'yellow'),
    #    ('09', 'light green'),
    #    ('10', 'teal'),
    #    ('11', 'light cyan'),
    #    ('12', 'light blue'),
    #    ('13', 'pink'),
    #    ('14', 'grey'),
    #    ('15', 'light grey'),
    #]
    c = [
        ('00', 'white'),
        ('01', 'black'),
        ('02', 'blue'),
        ('03', 'green'),
        ('04', 'light red'),
        ('05', 'red'),
        ('06', 'magenta'),
        ('07', 'orange'),
        ('08', 'yellow'),
        ('09', 'light green'),
        ('10', 'cyan'),
        ('11', 'light cyan'),
        ('12', 'light blue'),
        ('13', 'light magenta'),
        ('14', 'grey'),
        ('15', 'light grey'),
    ]
    send('\\x02bold\\x02 \\x1ditalic\\x1d \\x1funderline\\x1f \\x06blink\\x06 \\x16reverse\\x16')
    #send('\\x07bell\\x07 \\x1bansi color\\x1b')
    send(' '.join(map(lambda x: '\\x03{0}{0} {1}\\x0f'.format(*x), c[:8])))
    send(' '.join(map(lambda x: '\\x03{0}{0} {1}\\x0f'.format(*x), c[8:])))

@asyncio.coroutine
def mode(arg, send):
    u = [
        ('D', 'deaf'),
        ('g', 'caller-id'),
        ('i', 'invisible'),
        ('Q', 'no forwarding'),
        ('R', 'block unidentified'),
        ('w', 'see wallops'),
        ('Z', 'connected via SSL'),
    ]
    c = [
        ('b', 'channel ban'),
        ('c', 'color filter'),
        ('C', 'block CTCPS'),
        ('e', 'ban exemption'),
        ('f', 'forward on uninvited'),
        ('F', 'enable forwarding'),
        ('g', 'allow anybody to invite'),
        ('i', 'invite-only'),
        ('I', 'invite-only exemption'),
        ('j', 'join throttling'),
        ('k', 'channel password'),
        ('l', 'join limit'),
        ('L', 'large ban/exempt/invex lists'),
        ('m', 'moderated'),
        ('n', 'prevent external send'),
        ('p', 'paranoid'),
        ('P', 'permanent channel'),
        ('q', 'quiet user'),
        ('Q', 'block forwarded users'),
        ('r', 'block unidentified'),
        ('s', 'secret channel'),
        ('S', 'SSL-only'),
        ('t', 'only ops can change topic'),
        ('z', 'reduced moderation'),
    ]
    print(len(c))
    send('\\x0304user\\x0f ' + ' '.join(map(lambda e: '\\x0300{0}\\x0f({1})'.format(*e), u)))
    send('\\x0304channel\\x0f ' + ' '.join(map(lambda e: '\\x0300{0}\\x0f({1})'.format(*e), c[:12])))
    send('\\x0304cont.\\x0f ' + ' '.join(map(lambda e: '\\x0300{0}\\x0f({1})'.format(*e), c[12:])))
    send('see [\\x0302https://freenode.net/using_the_network.shtml\\x0f] for more infomation')

def getrandom(show):
    # http://en.wikipedia.org/wiki/Mathematical_constant
    # http://pdg.lbl.gov/2014/reviews/rpp2014-rev-phys-constants.pdf
    const = [
        # math
        (0,                              'zero'),
        (1,                              'unity'),
        ('i',                            'imaginary unit'),
        (3.1415926535,                   'pi'),
        (2.7182818284,                   'e'),
        (1.4142135623,                   'Pythagoras constant'),
        (0.5772156649,                   'Euler-Mascheroni constant'),
        (1.6180339887,                   'golden ratio'),
        # physics
        (299792458,                      'speed of light in vacuum'),
        (6.62606957,                     'Planck constant'),
        (1.054571726,                    'Planck constant, reduced'),
        (6.58211928,                     'Planck constant, reduced'),
        (1.602176565,                    'electron charge magnitude'),
        (0.510998928,                    'electron mass'),
        (9.10938291,                     'electron mass'),
        (938.272046,                     'proton mass'),
        (1.672621777,                    'proton mass'),
        (1836.15267245,                  'proton mass'),
        (8.854187817,                    'permittivity of free space'),
        (12.566370614,                   'permeability of free space'),
        (7.2973525698,                   'fine-structure constant'),
        (137.035999074,                  'fine-structure constant'),
        (2.8179403267,                   'classical electron radius'),
        (3.8615926800,                   'electron Compton wavelength, reduced'),
        (6.67384,                        'gravitational constant'),
        (6.70837,                        'gravitational constant'),
        (6.02214129,                     'Avogadro constant'),
        (1.3806488,                      'Boltzmann constant'),
        (8.6173324,                      'Boltzmann constant'),
        (1.1663787,                      'Fermi coupling constant'),
        (0.23126,                        'weak-mixing angle'),
        (80.385,                         'W boson mass'),
        (91.1876,                        'Z boson mass'),
        (0.1185,                         'strong coupling constant'),
        # other
        (9,                              'Cirno'),
        (1024,                           'caoliu'),
        (1984,                           'Orwell'),
        (10086,                          'China Mobile'),
        (233,                            'LOL'),
        (2333,                           'LOL'),
        (23333,                          'LOL'),
    ]
    rand = [
        # random
        (random.randint(0, 9),           'random number'),
        (random.randint(10, 99),         'random number'),
        (random.randint(100, 999),       'random number'),
        (random.randint(1000, 9999),     'random number'),
        (random.randint(10000, 99999),   'random number'),
        #math.sqrt(random.randint(0, 100000)),
    ]

    if show:
        get = lambda e: '{0} -- {1}'.format(str(e[0]), e[1])
    else:
        get = lambda e: str(e[0])
    l = random.choice([const, rand])
    return get(random.choice(l))

@asyncio.coroutine
def up(arg, send):
    send('+' + getrandom(arg['show']))

@asyncio.coroutine
def down(arg, send):
    send('-' + getrandom(arg['show']))

@asyncio.coroutine
def latex(arg, send):
    symbol = [
        (r'\alpha',       '\U0001d6fc'),
        (r'\pi',          '\U0001d6d1'),
        (r'\Alpha',       '\u0391'),
        (r'\Beta',        '\u0392'),
        (r'\Gamma',       '\u0393'),
        (r'\Delta',       '\u0394'),
        (r'\Epsilon',     '\u0395'),
        (r'\Zeta',        '\u0396'),
        (r'\Eta',         '\u0397'),
        (r'\Theta',       '\u0398'),
        (r'\Iota',        '\u0399'),
        (r'\Kappa',       '\u039a'),
        (r'\Lambda',      '\u039b'),
        (r'\Mu',          '\u039c'),
        (r'\Nu',          '\u039d'),
        (r'\Xi',          '\u039e'),
        (r'\Omicron',     '\u039f'),
        (r'\Pi',          '\u03a0'),
        (r'\Rho',         '\u03a1'),
        (r'\Sigma',       '\u03a3'),
        (r'\Tau',         '\u03a4'),
        (r'\Upsilon',     '\u03a5'),
        (r'\Phi',         '\u03a6'),
        (r'\Chi',         '\u03a7'),
        (r'\Psi',         '\u03a8'),
        (r'\Omega',       '\u03a9'),
        (r'\alpha',       '\u03b1'),
        (r'\beta',        '\u03b2'),
        (r'\gamma',       '\u03b3'),
        (r'\delta',       '\u03b4'),
        (r'\epsilon',     '\u03b5'),
        (r'\zeta',        '\u03b6'),
        (r'\eta',         '\u03b7'),
        (r'\theta',       '\u03b8'),
        (r'\iota',        '\u03b9'),
        (r'\kappa',       '\u03ba'),
        (r'\lambda',      '\u03bb'),
        (r'\mu',          '\u03bc'),
        (r'\nu',          '\u03bd'),
        (r'\xi',          '\u03be'),
        (r'\omicron',     '\u03bf'),
        (r'\pi',          '\u03c0'),
        (r'\rho',         '\u03c1'),
        (r'\sigma',       '\u03c3'),
        (r'\tau',         '\u03c4'),
        (r'\upsilon',     '\u03c5'),
        (r'\phi',         '\u03c6'),
        (r'\chi',         '\u03c7'),
        (r'\psi',         '\u03c8'),
        (r'\omega',       '\u03c9'),
    ]

    m = arg['content']
    for (t, s) in symbol:
        m = m.replace(t, s)
    send(m)

help = {
    'echo'           : 'echo <content> -- 我才不会自问自答呢!',
    'say'            : 'say <content>',
    'ping!'          : 'ping!',
    'pong!'          : 'pong!',
    'color'          : 'color -- let\'s puke \\x0304r\\x0307a\\x0308i\\x0303n\\x0310b\\x0302o\\x0306w\\x0fs!',
    'mode'           : 'mode -- \\x0300free\\x0f\\x0303node\\x0f is awesome!',
    'up'             : 'up [show] -- nice boat!',
    'down'           : 'down [show]',
}

func = [
    (echo,            r"echo (?P<content>.*)"),
    (say,             r"say (?P<content>.*)"),
    (pong,            r"ping!"),
    (ping,            r"pong!"),
    #(ping2,           r"(?:.*): pong!"),
    (color,           r"color"),
    (mode,            r"mode"),
    (up,              r"up(?:\s+(?P<show>show))?"),
    (down,            r"down(?:\s+(?P<show>show))?"),
    (pia,             r"pia( (?P<content>.*))?"),
    (mua,             r"mua( (?P<content>.*))?"),
    (latex,           r"latex\s+(?P<content>.*)"),
]