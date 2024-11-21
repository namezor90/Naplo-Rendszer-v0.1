import json

class IskolaiNaplo:
    def __init__(self):
        # Alap adatok betöltése
        try:
            with open('naplo_adatok.json', 'r', encoding='utf-8') as file:
                self.adatok = json.load(file)
        except FileNotFoundError:
            self.adatok = {
                "diakok": {},
                "tanarok": {},
                "osztalyok": {},
                "tantargyak": ["matematika", "magyar", "történelem", "angol"],
                "jegyek": {}
            }

    def mentes(self):
        # Adatok mentése JSON fájlba
        with open('naplo_adatok.json', 'w', encoding='utf-8') as file:
            json.dump(self.adatok, file, indent=2, ensure_ascii=False)

    def uj_diak(self):
        print("\nÚj diák felvétele")
        print("-" * 20)
        
        nev = input("Diák neve: ")
        osztaly = input("Osztály: ")
        
        # Egyszerű ellenőrzés
        if not nev or not osztaly:
            print("A név és osztály megadása kötelező!")
            return
            
        uj_id = f"D{len(self.adatok['diakok']) + 1}"
        
        # Diák adatainak összeállítása
        self.adatok['diakok'][uj_id] = {
            "nev": nev,
            "osztaly": osztaly,
            "hianyzasok": {"igazolt": 0, "igazolatlan": 0}
        }
        
        print(f"Diák sikeresen felvéve! (ID: {uj_id})")
        self.mentes()

    def diakok_listazasa(self):
        print("\nDiákok listája")
        print("-" * 20)
        
        if not self.adatok['diakok']:
            print("Nincs még diák felvéve!")
            return
            
        for id, diak in self.adatok['diakok'].items():
            print(f"ID: {id}")
            print(f"Név: {diak['nev']}")
            print(f"Osztály: {diak['osztaly']}")
            print(f"Hiányzások: {diak['hianyzasok']['igazolt']} igazolt, "
                  f"{diak['hianyzasok']['igazolatlan']} igazolatlan")
            
            # Jegyek kiírása
            diak_jegyei = [jegy for jegy in self.adatok['jegyek'].values() 
                          if jegy['diak_id'] == id]
            if diak_jegyei:
                print("Jegyek:")
                for jegy in diak_jegyei:
                    print(f"  {jegy['tantargy']}: {jegy['ertek']} ({jegy['datum']})")
            print("-" * 20)

    def jegy_beiras(self):
        print("\nJegy beírása")
        print("-" * 20)
        
        if not self.adatok['diakok']:
            print("Nincs még diák felvéve!")
            return
            
        # Diákok listázása
        print("Diákok:")
        for id, diak in self.adatok['diakok'].items():
            print(f"{id}: {diak['nev']} ({diak['osztaly']})")
            
        diak_id = input("\nVálassz diákot (ID): ")
        if diak_id not in self.adatok['diakok']:
            print("Nincs ilyen diák!")
            return
            
        # Tantárgyak listázása
        print("\nTantárgyak:")
        for i, tantargy in enumerate(self.adatok['tantargyak'], 1):
            print(f"{i}. {tantargy}")
            
        try:
            tantargy_index = int(input("\nVálassz tantárgyat (szám): ")) - 1
            tantargy = self.adatok['tantargyak'][tantargy_index]
        except (ValueError, IndexError):
            print("Érvénytelen választás!")
            return
            
        try:
            jegy = int(input("Add meg a jegyet (1-5): "))
            if jegy not in range(1, 6):
                print("Érvénytelen jegy!")
                return
        except ValueError:
            print("Érvénytelen érték!")
            return
            
        datum = input("Add meg a dátumot (ÉÉÉÉ-HH-NN): ")
        
        # Jegy hozzáadása
        jegy_id = f"J{len(self.adatok['jegyek']) + 1}"
        self.adatok['jegyek'][jegy_id] = {
            "diak_id": diak_id,
            "tantargy": tantargy,
            "ertek": jegy,
            "datum": datum
        }
        
        print("Jegy sikeresen beírva!")
        self.mentes()

    def hianyzas_beiras(self):
        print("\nHiányzás beírása")
        print("-" * 20)
        
        if not self.adatok['diakok']:
            print("Nincs még diák felvéve!")
            return
            
        # Diákok listázása
        print("Diákok:")
        for id, diak in self.adatok['diakok'].items():
            print(f"{id}: {diak['nev']} ({diak['osztaly']})")
            
        diak_id = input("\nVálassz diákot (ID): ")
        if diak_id not in self.adatok['diakok']:
            print("Nincs ilyen diák!")
            return
            
        print("\nHiányzás típusa:")
        print("1. Igazolt")
        print("2. Igazolatlan")
        
        try:
            tipus = int(input("Válassz típust: "))
            if tipus not in [1, 2]:
                print("Érvénytelen választás!")
                return
        except ValueError:
            print("Érvénytelen érték!")
            return
            
        try:
            napok = int(input("Add meg a napok számát: "))
            if napok < 1:
                print("Érvénytelen érték!")
                return
        except ValueError:
            print("Érvénytelen érték!")
            return
            
        # Hiányzás rögzítése
        if tipus == 1:
            self.adatok['diakok'][diak_id]['hianyzasok']['igazolt'] += napok
        else:
            self.adatok['diakok'][diak_id]['hianyzasok']['igazolatlan'] += napok
            
        print("Hiányzás sikeresen rögzítve!")
        self.mentes()

    def diak_kereses(self):
        print("\nDiák keresése")
        print("-" * 20)
        
        if not self.adatok['diakok']:
            print("Nincs még diák felvéve!")
            return
            
        nev_toredek = input("Add meg a diák nevének egy részét: ").lower()
        
        talalatok = []
        for id, diak in self.adatok['diakok'].items():
            if nev_toredek in diak['nev'].lower():
                talalatok.append((id, diak))
                
        if not talalatok:
            print("Nincs találat!")
            return
            
        print("\nTalálatok:")
        for id, diak in talalatok:
            print(f"\nID: {id}")
            print(f"Név: {diak['nev']}")
            print(f"Osztály: {diak['osztaly']}")
            print(f"Hiányzások: {diak['hianyzasok']['igazolt']} igazolt, "
                  f"{diak['hianyzasok']['igazolatlan']} igazolatlan")

    def menu(self):
        while True:
            print("\nIskolai Napló Program")
            print("-" * 20)
            print("1. Új diák felvétele")
            print("2. Diákok listázása")
            print("3. Jegy beírása")
            print("4. Hiányzás beírása")
            print("5. Diák keresése")
            print("6. Kilépés")
            
            valasztas = input("\nVálassz egy menüpontot: ")
            
            if valasztas == "1":
                self.uj_diak()
            elif valasztas == "2":
                self.diakok_listazasa()
            elif valasztas == "3":
                self.jegy_beiras()
            elif valasztas == "4":
                self.hianyzas_beiras()
            elif valasztas == "5":
                self.diak_kereses()
            elif valasztas == "6":
                print("\nViszlát!")
                break
            else:
                print("Érvénytelen választás!")


# Program indítása
naplo = IskolaiNaplo()
naplo.menu()
