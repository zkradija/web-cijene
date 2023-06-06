import os
import time
from datetime import datetime

import bih_konzum
import crna_gora_voli_trade
import hrvatska_dm
import hrvatska_kaufland
import hrvatska_konzum
import hrvatska_njuskalo
import hrvatska_plodine
import makedonija_reptil
import slovenija_mercator
import slovenija_spar
import slovenija_tus
import srbija_cenoteka
import srbija_idea
import srbija_maxi
import srbija_univerexport


# removing all chrome instances
def clean_chrome():
    os.system('taskkill /im chrome.exe /f')
    os.system('taskkill /im chromedriver.exe /f')


if __name__ == '__main__':
    
    start_time = time.time()
    print(f'main.py started: {datetime.now().strftime("%H:%M:%S")}')

    clean_chrome()
    
    bih_konzum.main()
    crna_gora_voli_trade.main()
    hrvatska_dm.main()
    hrvatska_kaufland.main()
    hrvatska_konzum.main()
    hrvatska_njuskalo.main()
    hrvatska_plodine.main()
    makedonija_reptil.main()
    slovenija_mercator.main()
    slovenija_spar.main()
    slovenija_tus.main()
    srbija_cenoteka.main()
    srbija_idea.main()
    srbija_maxi.main()
    srbija_univerexport.main()

    end_time = time.time()
    print(f'main.py ended: {datetime.now().strftime("%H:%M:%S")}')
    elapsed_time = end_time - start_time
    print(f'main.py elapsed time: {int(elapsed_time)} seconds')