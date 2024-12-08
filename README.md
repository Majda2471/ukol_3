Elections Scraper
Popis programu
Tento program slouží k získávání dat z voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017. Data jsou získávána z webových stránek volby.cz a ukládána do souboru ve formátu .csv. Pro spuštění programu je potřeba vybrat konkrétní volební obvod (například: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 pro obvod Prostějov) a zadat název výstupního souboru (například: vysledky_voleb_prostejov.csv).

Instalace potřebných knihoven
Program vyžaduje několik knihoven, které jsou uvedeny v souboru requirements.txt. Tyto knihovny lze nainstalovat pomocí příkazového řádku následujícím příkazem:

bash
Zkopírovat kód
pip install -r requirements.txt
Spuštění programu
Pro spuštění programu je třeba zadat dva argumenty:

Odkaz na webovou stránku s volebními výsledky.
Název výstupního souboru .csv.
Příklad spuštění programu:

bash
Zkopírovat kód
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_voleb_prostejov.csv"
Výstup programu
Výstupem programu je soubor .csv s volebními výsledky, který se uloží do složky projektu. Například výše uvedený příkaz vytvoří soubor vysledky_voleb_prostejov.csv, který lze následně otevřít a analyzovat.
