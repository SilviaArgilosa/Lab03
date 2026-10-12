import csv
from operator import attrgetter

class Strumenti:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore
    def __str__(self):
        return(f"{self.codice} {self.tipo} {self.marca} {self.anno_acquisto} {self.valore}")

class Prestiti:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo
    def __str__(self):
        return (f"{self.id_prestito} {self.data} {self.id_strumento} {self.cognome_allievo}")

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        self.strumenti = []
        try:
            file = open(file_path, "r", encoding = "utf-8")
            righe = csv.reader(file)
            for riga in righe:
                codice = riga[0]
                tipo = riga[1]
                marca = riga[2]
                anno_acquisto = int(riga[3])
                valore = float(riga[4])

                nuovo_strumento = Strumenti(codice, tipo, marca, anno_acquisto, valore)
                self.strumenti.append(nuovo_strumento)
            file.close()
            return self.strumenti
        except FileNotFoundError:
            print("Attenzione, file non trovato!")
            return None

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        if len(self.strumenti) == 0:
            nuovo_codice = "S1"
            nuovo_strumento = Strumenti(nuovo_codice, tipo, marca, anno_acquisto, valore)
            self.strumenti.append(nuovo_strumento)
        else:
            ultimo_strumento = self.strumenti[-1]
            codice_ultimo_strumento = ultimo_strumento.codice
            numero_codice_ultimo_strumento = int(codice_ultimo_strumento[1:])
            nuovo_codice = f"S{numero_codice_ultimo_strumento+1}"
            nuovo_strumento = Strumenti(nuovo_codice, tipo, marca, anno_acquisto, valore)
            self.strumenti.append(nuovo_strumento)

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        strumenti_ordinati = sorted(self.strumenti, key = attrgetter("marca"))
        return strumenti_ordinati

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        trovato = False
        for strumento in self.strumenti:
            if strumento.codice == id_strumento:
                trovato = True
        if not trovato:
            raise Exception("Lo strumento non esiste!")

        for prestito in self.prestiti:
            if prestito.id_strumento == id_strumento:
                raise Exception("Lo strumento è già in prestito!")

        if len(self.prestiti) == 0:
            nuovo_codice = "P1"
            nuovo_prestito = Prestiti(nuovo_codice, data, id_strumento, cognome_allievo)
            self.prestiti.append(nuovo_prestito)
        else:
            ultimo_prestito = self.prestiti[-1]
            codice_ultimo_prestito = ultimo_prestito.id_prestito
            numero_codice_ultimo_prestito = int(codice_ultimo_prestito[1:])
            nuovo_codice = f"P{numero_codice_ultimo_prestito+1}"
            nuovo_prestito = Prestiti(nuovo_codice, data, id_strumento, cognome_allievo)
            self.prestiti.append(nuovo_prestito)
        return nuovo_prestito


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        trovato = False
        for prestito in self.prestiti:
            if prestito.id_prestito == id_prestito:
                trovato = True
                self.prestiti.remove(prestito)
        if not trovato:
            raise Exception("Il prestito non esiste!")

        return prestito
        
