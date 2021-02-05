import os
import sys
import random
import pickle
import zipfile
import urllib.parse
import datetime as dt
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if getattr(sys, 'frozen', False):
    bundle_dir = os.path.dirname(sys.executable)
else:
    bundle_dir = os.path.dirname(os.path.realpath(__file__))

def load_accounts(path):
    accounts = []
    with open(path) as fd:
        for line in fd:
            account = line.strip()
            if not account:
                continue
            accounts.append(account)
    return accounts
    
def load_proxies(path):
    proxies = []
    with open(path) as fd:
        for line in fd:
            proxy = line.strip()
            if not proxy:
                continue
            proxies.append(proxy)
    return proxies
    
def load_tracks(path):
    tracks = []
    with open(path) as fd:
        for line in fd:
            track = line.strip()
            if not track:
                continue
            tracks.append(track)
    return tracks
            
def get_random_ua():
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (X11; Linux i686; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/72.0.3815.186',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/72.0.3815.186',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/72.0.3815.186',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36']
    return user_agents[random.randint(0,len(user_agents)-1)]

def log_js_console(driver):
    for entry in driver.get_log('browser'):
        print(entry['message'])
        
def url_to_utf8(url):
    url_utf8 = urllib.parse.quote(url, safe='')
    return 'https://app.napster.com/login?goto=%s' % url_utf8[29:]

def proxy_ext(cred):
    data = cred[1].strip().split(':')
    if len(data) <= 1:
        raise Exception('Your proxy %s is incomplete.' % cred[1])
    for i in range(4-len(data)):
        data.append('')
    http = [3128, 80, 8080, 8443, 25, 8123, 8118, 443, 4000, 81, 999, 83, 8182, 8181, 8087, 8095, 3838, 6000, 8686, 8000]
    socks = [1080, 8020, 4145, 9300, 1337, 1357, 8580, 7126, 1090, 5555, 9000, 9279, 4216, 9090, 6958, 4093, 9050, 4576, 8691, 1081, 6667, 7777, 9999, 2784, 3306, 3000, 8082, 5353, 7302, 8888]
    host = data[0]
    port = data[1]
    username = data[2]
    password = data[3]
    if int(port) in http:
        scheme = 'http'
    elif int(port) in socks:
        scheme = 'socks5'
    else:
        raise Exception('Your proxy port %s is not in our list.' % port)
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "%s",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """ % host
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "%s",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (scheme, host, port, username, password)
    pluginfile = 'extensions/%s.zip' % host
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return pluginfile

def incognito_ext():
    return 'extensions/incognito.zip'

def save(savefile, filename) :
    with open('%s/%s.pickle' % (bundle_dir, filename), 'wb') as handle:
        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load(filename) :
    with open('%s/%s.pickle' % (bundle_dir, filename), 'rb') as handle:
        return(pickle.load(handle))

def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start

def get_working_hours(mini, maxi, day): 
    hours = []
    run = 0
    pause = 0
    while sum(hours) < day:
        runval = randrange_float(3,5,0.25)
        if (sum(hours) + runval) > day:
            runval = day - sum(hours)
        if (run + runval) > maxi:
            run = maxi - runval
        run += runval
        hours.append(runval)
        pauseval = randrange_float(0.5,2,0.25)
        if (sum(hours) + pauseval) > day:
            pauseval = day - sum(hours)
        pause += pauseval
        hours.append(pauseval)
    return hours

def working(working_hours, starting_hour):
    hours = working_hours.copy()
    start = dt.timedelta(hours=starting_hour)
    for i in range(len(hours)):
        hours[i] = dt.timedelta(hours=hours[i])

    hours.insert(0, start)

    now = datetime.now().time()
    now = dt.timedelta(hours=now.hour, minutes=now.minute)
    pos = -2
    b = False
    current, end = dt.timedelta(hours=0), dt.timedelta(hours=0)
    res = []
    for i in range(0, len(hours)-1, 2):
        current = end + hours[i]
        if end < now < current:
            pos = i/2 - 1
        time = hours[i+1]
        end = current + time
        if current >= dt.timedelta(days=1):
            current -= dt.timedelta(days=1)
        if end >= dt.timedelta(days=1):
            end -= dt.timedelta(days=1)
        if current <= now <= end:
            pos = i/2
            b = True
        res.append('%s-%s' % (str(current).rsplit(':', 1)[0], str(end).rsplit(':', 1)[0]))
    return [res, pos, b]