# Elections Scraper

## Popis programu
Tento program slouží k získávání dat z voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017. Data jsou získávána z webových stránek [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a ukládána do souboru ve formátu `.csv`. Pro spuštění programu je potřeba vybrat konkrétní volební obvod (například: [https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103) pro obvod Prostějov) a zadat název výstupního souboru (například: `vysledky_voleb_prostejov.csv`).

## Instalace potřebných knihoven
Program vyžaduje několik knihoven, které jsou uvedeny v souboru `requirements.txt`. 

## Výstupy programu
Výstupem programu je soubor `.csv`, který obsahuje získaná data z voleb. Tento soubor je uložen ve složce projektu pod názvem zadaným jako druhý argument při spuštění programu. 

## Spuštění programu
Program se spouští s použitím dvou argumentů:
1. Odkaz na webovou stránku s volebními výsledky.
2. Název výstupního souboru `.csv`.

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_voleb_prostejov.csv"
