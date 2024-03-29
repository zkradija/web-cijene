import os
import time
from datetime import datetime

import bih_konzum
import crna_gora_voli_trade
import hrvatska_dm
import hrvatska_jadranka
import hrvatska_kaufland
import hrvatska_konzum
import hrvatska_lidl
import hrvatska_metro
import hrvatska_njuskalo
import hrvatska_plodine
import hrvatska_ppk_bjelovar
import hrvatska_tommy
import makedonija_reptil
import slovenija_mercator
import slovenija_spar
import slovenija_tus
import srbija_cenoteka
import srbija_idea
import srbija_maxi
import srbija_univerexport


# removing all chrome instances, not used atm
def clean_chrome():
    os.system('taskkill /im chrome.exe /f')
    os.system('taskkill /im chromedriver.exe /f')


if __name__ == '__main__':
    
    start_time = time.perf_counter()
    print(f'main.py started: {datetime.now().strftime("%H:%M:%S")}')

    
    try:
        bih_konzum.main()
        crna_gora_voli_trade.main()
        hrvatska_dm.main()
        hrvatska_jadranka.main()
        hrvatska_kaufland.main()
        hrvatska_konzum.main()
        hrvatska_lidl.main()
        hrvatska_metro.main()
        hrvatska_njuskalo.main()
        hrvatska_plodine.main()
        hrvatska_ppk_bjelovar.main()
        hrvatska_tommy.main()
        makedonija_reptil.main()
        slovenija_mercator.main()
        slovenija_spar.main()
        slovenija_tus.main()
        srbija_cenoteka.main()
        srbija_idea.main()
        srbija_maxi.main()
        srbija_univerexport.main()

    except Exception as e:
        print(e)

    end_time = time.perf_counter()
    print(f'main.py ended: {datetime.now().strftime("%H:%M:%S")}')
    elapsed_time = end_time - start_time
    print(f'main.py elapsed time: {int(elapsed_time)} seconds')