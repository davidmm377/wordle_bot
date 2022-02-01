from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from pyshadow.main import Shadow
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException as ENIE
from selenium.common.exceptions import WebDriverException as WDE
import logging
class Web(object):
    def __init__(self,show=False):
        service = ChromeService(executable_path=ChromeDriverManager(log_level=logging.FATAL).install())
        options = webdriver.ChromeOptions()
        if not show:
            options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            self._driver = webdriver.Chrome(service=service,options=options)
        except WDE:
            print("Sorry, webdriver-manager isn't working!\nTry minmax.py directly.")
            exit(-1)
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
    def try_close_popup(self,retry=0):
        try:
            close = self._shadow.find_elements("game-icon")[4]
            close.click()
        except ENIE: 
            if retry < 10: self.try_close_popup(retry+1)
    def do_word(self, word : str,retry=0):
        #? check valid
        self._actions.send_keys(word + Keys.RETURN)
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
        from minmax import MinMax as mm
        self._player = mm(start_guess)
        print(f"{self._player.auto(self.do_word)}/6")
    def run(self):
        while 1:
            guess = input('guess: ')
            res = self.do_word(guess)
            print(guess, res)
if __name__ == "__main__":
    w = Web(show=False)
    w.mm()