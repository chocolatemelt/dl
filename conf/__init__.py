import json
import os

from core import Conf

ELEMENTS = ('flame', 'water', 'wind', 'light', 'shadow')
WEAPON_TYPES = ('sword', 'blade', 'dagger', 'axe', 'lance', 'bow', 'wand', 'staff', 'gun')
TRIBE_TYPES = ('thaumian', 'physian', 'demihuman', 'therion', 'undead', 'demon', 'human', 'dragon')
DURATIONS = (60, 120, 180)

ROOT_DIR = os.getenv('ROOT_DIR', os.path.realpath(os.path.join(__file__, '../..')))

def save_json(fn, data, indent=None):
    froot = os.path.join(ROOT_DIR, 'conf')
    fpath = os.path.join(froot, fn)
    with open(fpath, 'w', encoding='utf8') as f:
        return json.dump(data, f, ensure_ascii=False, indent=indent)

def load_json(fn):
    froot = os.path.join(ROOT_DIR, 'conf')
    fpath = os.path.join(froot, fn)
    with open(fpath, 'r', encoding='utf8') as f:
        return json.load(f, parse_float=float, parse_int=int)

coability = load_json('chains.json')
skillshare = load_json('skillshare.json')
wyrmprints = load_json('wyrmprints.json')
# weapons = load_json('weapons.json')

baseconfs = {}
weapons = {}
for wep in WEAPON_TYPES:
    baseconfs[wep] = load_json(f'base/{wep}.json')
    weapons[wep] = load_json(f'wep/{wep}.json')

dragons = {}
for ele in ELEMENTS:
    dragons[ele] = load_json(f'drg/{ele}.json')

alias = {}
for target, alst in load_json('alias.json').items():
    for a in alst:
        alias[a] = target

elecoabs = {}
for ele in ELEMENTS:
    elecoabs[ele] = {**coability['any'], **coability['generic'], **coability[ele]}

mono_elecoabs = {}
for ele in ELEMENTS:
    mono_elecoabs[ele] = {**coability['generic'], **coability[ele]}

advconfs = {}
def load_adv_json(adv):
    try:
        return advconfs[adv]
    except KeyError:
        aconf = load_json(f'adv/{adv}.json')
        advconfs[adv] = aconf
        return aconf

advequip = {}
def load_equip_json(adv):
    try:
        return advequip[adv]
    except KeyError:
        try:
            equip = load_json(f'equip/{adv}.json')
        except:
            equip = {}
        advequip[adv] = equip
        return equip

def load_all_equip_json():
    froot = os.path.join(ROOT_DIR, 'conf', 'equip')
    for root, _, files in os.walk(froot):
        for fn in files:
            load_equip_json(os.path.splitext(fn)[0])
    return advequip

def save_equip_json(adv, equip):
    advequip[adv] = equip
    save_json(f'equip/{adv}.json', equip, indent=2)

def get_icon(adv):
    try:
        return load_adv_json(adv)['c']['icon']
    except (FileNotFoundError, KeyError):
        return ''

def get_fullname(adv):
    try:
        return load_adv_json(adv)['c']['name']
    except (FileNotFoundError, KeyError):
        return adv

def get_adv(name):
    conf = Conf(load_adv_json(name))

    wt = conf.c.wt
    base = baseconfs[wt]
    baseconf = Conf(base)

    if bool(conf.c.spiral):
        baseconf.update(baseconf.lv2)
    del baseconf['lv2']

    if wt == 'gun' and len(conf.c.gun) == 1:
        # move gun[n] to base combo
        target = conf.c.gun[0]
        for xn, xconf in list(baseconf.find(r'^(x\d|fsf?)_gun\d$')):
            if int(xn[-1]) == target:
                baseconf[xn.split('_')[0]] = xconf
            del baseconf[xn]

    conf.update(baseconf, rebase=True)

    return conf

def all_subclasses(cl):
    return set(cl.__subclasses__()).union([s for c in cl.__subclasses__() for s in all_subclasses(c)])

def subclass_dict(cl):
    return {sub_class.__name__: sub_class for sub_class in all_subclasses(cl)}

def list_advs():
    for fn in sorted(os.listdir(os.path.join(ROOT_DIR, 'conf', 'adv'))):
        fn, ext = os.path.splitext(fn)
        if ext != '.json':
            continue
        yield fn
