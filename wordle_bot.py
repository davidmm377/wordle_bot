import logging, argparse
from minmax import MinMax as mm
class Web(object):
    def __init__(self,show=False):
        self._show = show
    def setup(self):
        from selenium.webdriver.common.action_chains import ActionChains
        self.ActionChains = ActionChains
        from selenium.webdriver.common.keys import Keys
        self.Keys = Keys
        from selenium import webdriver
        self.webdriver = webdriver
        from pyshadow.main import Shadow
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.common.exceptions import ElementNotInteractableException as ENIE
        from selenium.common.exceptions import WebDriverException as WDE
        self.WDE, self.ENIE = WDE, ENIE
        service = ChromeService(executable_path=ChromeDriverManager(log_level=logging.FATAL).install())
        options = webdriver.ChromeOptions()
        if not self._show:
            options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.try_make_web(service, options): return 1
        self._driver.get('https://www.powerlanguage.co.uk/wordle/')
        self._shadow = Shadow(self._driver)
        self._curtile = 0
        self._actions =ActionChains(self._driver)
        self._evals = None
        self._emap = {'absent': 'x',
                      'present': 'y',
                      'correct': 'g',
                      None:'.'}
        self.try_close_popup()
        return 0
    def try_make_web(self, service, options):
        try:
            self._driver = self.webdriver.Chrome(service=service,options=options)
        except self.WDE: 
            return 1
            # print("Sorry, webdriver-manager isn't working!\nTry minmax.py directly.")
            # exit(-1)
        return 0
            
    def try_close_popup(self,retry=0):
        try:
            close = self._shadow.find_elements("game-icon")[4]
            close.click()
        except self.ENIE: 
            if retry < 10: self.try_close_popup(retry+1)
    def do_word(self, word : str,retry=0):
        #? check valid
        self._actions.send_keys(word + self.Keys.RETURN)
        self._actions.perform()
        self._tiles = self._shadow.find_elements("game-tile")[:30]
        evals = [e for e in [t.get_attribute('evaluation') for t in self._tiles] if e is not None]
        if evals == self._evals:
            if retry > 10: return '?????'
            return self.do_word(word,retry=retry+1)
        self._evals = evals
        word_evals = self._evals[-5:]
        return ''.join(self._emap[e] if e in self._emap else 'z' for e in word_evals)
    def mm(self,start_guess : str = 'arise'):
        self._player = mm(start_guess)
        print(f"{self._player.auto(self.do_word)}/6")
    def run(self):
        while 1:
            guess = input('guess: ')
            res = self.do_word(guess)
            print(guess, res)
def auto(start,show):
    w = Web(show)
    if w.setup(): return manual(start)
    w.mm(start)
def manual(start):
    p = mm(start)
    p.play()
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Wordle Bot by jsearcy1 (with auto mode by davidmm377.)')
    p.add_argument('--show',action='store_true',default=False,dest='show',required=False,help="opens wordle in the browser for you to watch it play!")
    p.add_argument('--minmax',action='store_true',default=False,dest='minmax',required=False,help="manual interactive mode by jsearcy1")
    p.add_argument('--start',action='store',type=str,dest='start',help='starting word (default: arise)',default='arise',required=False)
    args = p.parse_args()
    if args.minmax:
        manual(args.start)
    else:
        auto(args.start,show=args.show)