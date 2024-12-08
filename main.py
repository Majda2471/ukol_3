"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Magdalena Kreckova
email: kreckova.majda@gmail.com
discord: Majda_247
"""

import csv
import sys

import requests
import bs4
from bs4 import BeautifulSoup


def kontrola_vstupu(url: str, soubor: str):
    """
    Kontroluje správnost url a zároveň správnost typu souboru. 
    """
    print(f"Zadaná URL: '{url}'")
    print(f"Zadaný soubor: '{soubor}'")
    print(f"Kontrola URL: {url.startswith('https://www.volby.cz/pls/ps2017nss')}")
    print(f"Kontrola souboru: {soubor.endswith('.csv')}")

    if not url.startswith("https://www.volby.cz/pls/ps2017nss") or not soubor.endswith(".csv"):
        print(f"URL neobsahuje požadovaný formát: {url} \
              nebo požadovaný výstup není typu CSV: {soubor}. Ukončuji program")
        exit()
    else:
        print("Program se spouští!")


def prevod_html(url: str) -> BeautifulSoup:
    """
    Funkce vrací text HTML ze stránky.
    """
    odp_serveru = requests.get(url) # zapisuje url jako string 
    return BeautifulSoup(odp_serveru.text, 'html.parser') # převede HTML na text


def vyber_informaci_obec(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Funkce získává informace o obci (kód obce a jméno obce)
    """
    ## získá text - kód obce [0] a jméno obce [1]
    return [
        tr_tag[0].getText(),    # číslo obce
        tr_tag[1].getText()     # jméno obce
    ]


def atributy_volici(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Vybere informace z tabulky voličů.
    """
    ## ze všech tr získáme text - počet voličů [3], vydané obálky [4] a platné hlasy [7]
    ## texty jsou upraveny tak, aby číslo bylo jednotné (rozdělovač tisíců)
    return[
        tr_tag[3].getText(),    # počet voličů
        tr_tag[4].getText(),    # vydané obálky
        tr_tag[7].getText()     # platné hlasy
    ]


def atributy_strany(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Funkce získává informace o politické straně a počtu hlasů.
    """
    ## ze všech tr získáme - název strany [1] a počet hlasů [2]
    ## texty jsou upraveny tak, aby číslo bylo jednotné (rozdělovač tisíců)
    return[
        tr_tag[1].getText(),    # název politické strany
        tr_tag[2].getText()     # počet hlasů
    ]


def ziskani_odkazu(soup) -> list:
    """
    Funkce získává všechny odkazy z tabulky, které obsahují kódy obcí.
    """
    table = soup.find("div", {"id":"inner"})
    vsechny_radky = table.find_all("tr")
    odkazy_seznam = []

    for prvek in vsechny_radky[2:]:    # odstranění hlavičky [2:0]
        a_tag = prvek.find("a")     # najde první <a> v řádku
        if a_tag and a_tag.get('href'):
            cely_odkaz = f"https://volby.cz/pls/ps2017nss/{a_tag['href']}"
            odkazy_seznam.append(cely_odkaz)
    return odkazy_seznam


def ziskani_dat_obce(vsechny_radky) -> list:
    """
    Funkce získá data o obcích.
    """
    vysledky_obci = []
    for radek in vsechny_radky[2:]:
        bunky_v_radku = radek.find_all("td")
        if bunky_v_radku:
            data_obce = vyber_informaci_obec(bunky_v_radku)
            vysledky_obci.append(data_obce)
    #získá kód obce a jméno obce
    return vysledky_obci


def ziskani_vysledky_strany(vsechny_radky) -> tuple:
    """
    Fuknce získá výsledky jednotlivých stran. 
    """
    vysledky_strany = []
    nazvy_stran = set()

    for radek in vsechny_radky:
        obecni_vysledky = {}
        for jeden_radek in radek:
            bunky_radku = jeden_radek.find_all("td")
            if bunky_radku and bunky_radku[1].getText() != "-":
                data_strany = atributy_strany(bunky_radku)
                nazev_strany = data_strany[0]
                hlasy = data_strany[1]
                nazvy_stran.add(nazev_strany)
                obecni_vysledky[nazev_strany] = hlasy
            vysledky_strany.append(obecni_vysledky)
    #Vrací hlasi jednotlivých stran a seznam všech stran
    return vysledky_strany, nazvy_stran 


def ziskani_vysledky_volici(vsechny_radky) -> list:
    """
    Funkce získá výsledky voličů.
    """
    vysledky_volicu = []
    for radek in vsechny_radky[2:]:
        for jeden_radek in radek:
            bunky_radku = jeden_radek.find_all("td")
            if bunky_radku:
                vysledky_volicu.append(atributy_volici(bunky_radku))
    #vrátí data k voličům z funkce atributy_volici
    return vysledky_volicu


def odstraneni_znaku(data) -> list:
    """
    Funkce odstraní nevhodné znaky z dat.
    """
    opraveny_seznam = []
    for polozky in data:
        podseznam = [polozka.replace('\xa0', '') for polozka in polozky]
        opraveny_seznam.append(podseznam)
    return opraveny_seznam


def vytvoreni_csv(vystupni_soubor, hlavicka, data):
    """
    Funkce zapíše data do CSV souboru. 
    """
    with open(vystupni_soubor, mode="w", newline='', encoding='utf-8') as nove_csv:
       zapisovac = csv.writer(nove_csv)
       zapisovac.writerow(hlavicka)     #zapíše hlavičku tabulky
       for row in data:
        zapisovac.writerow(row)         #zapíše ostatní data


def hlavni_funkce(url, vystupni_soubor):
    kontrola_vstupu(url, vystupni_soubor)
    soup = prevod_html(url)
    vsechny_radky = soup.find("div", {"id": "inner"}).find_all("tr")

    vysledky_obce = ziskani_dat_obce(vsechny_radky)
    odkazy = ziskani_odkazu(soup)

    vsechny_radky_strany = []
    vsechny_radky_volici = []
    for moc_url in odkazy:
        soup_2 = prevod_html(moc_url)
        vsechny_radky_strany.append(soup_2.find("div", {"id": "inner"}).find_all("tr"))
        vsechny_radky_volici.append(soup_2.find("table", {"class": "table"}).find_all("tr"))
    
    vysledky_strany, nazvy_stran = ziskani_vysledky_strany(vsechny_radky_strany)
    vysledky_volici = ziskani_vysledky_volici(vsechny_radky_volici)
    opraveny_volici = odstraneni_znaku(vysledky_volici)

    hlavicka = ["kod obce", "jmeno obce", "pocet volicu", "vydane obalky",\
         "platne hlasy"] + list(nazvy_stran)
    data = []
    for obec, volici_data, vysledky_obce in zip(vysledky_obce, opraveny_volici,\
         vysledky_strany):
         row = obec + volici_data
         for nazev_strany in nazvy_stran:
            row.append(vysledky_obce.get(nazev_strany, 0))
         data.append(row)
    
    vytvoreni_csv(vystupni_soubor, hlavicka, data)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití skriptu: python main.py <url> <vystupni_soubor>")
        sys.exit(1)
    
    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    hlavni_funkce(url, vystupni_soubor)