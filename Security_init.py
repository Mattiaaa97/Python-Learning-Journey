import logging
import sqlite3 as sql
import numpy as np

logging.basicConfig(
    filename='warn_secure.log',
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Datamanager:
    def __init__(self):

        try:
            self.connessione = sql.connect("cyber_security.db")
            self.cursor = self.connessione.cursor()

        except sql.Error as e:
            print('The file cyber_security.db was not found')
        else:
            print('The connection was created successfully, ready for use!')

    def crea_tab_attacchi(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS attacchi ("
                            "ID_ATTACCO INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "NOME_ATTACCO TEXT NOT NULL,"
                            "CODICE_CVE INTEGER NOT NULL,"
                            "PERICOLOSITA TEXT NOT NULL) ")

    def crea_log_traffico(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS traffico ("
                            "ID_LOG INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "TIME_STAMP FLOAT NOT NULL,"
                            "IP_SORGENTE TEXT NOT NULL,"
                            "IP_DESTINAZIONE TEXT NOT NULL,"
                            "PORTA INTEGER NOT NULL,"
                            "BYTE_TRASMESSI INTEGER NOT NULL ) ")

    def crea_allarmi(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS allarmi ("
                            "ID_ALLARMI INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "ID_LOG INTEGER NOT NULL,"
                            "ID_ATTACCO INTEGER NOT NULL, "
                            "SCORE_CONFIDENZA FLOAT NOT NULL,"
                            "STATO TEXT NOT NULL, "
                            "FOREIGN KEY(ID_LOG) REFERENCES traffico(ID_LOG), "
                            "FOREIGN KEY(ID_ATTACCO) REFERENCES attacchi(ID_ATTACCO) ) ")

    def popola_attacchi_base(self):

        nome_attacco : list[str] = np.random.choice(["Ransomware", "DDoS", "SQL Injection", "Phishing"])
        if not nome_attacco:
            logging.warn("The name isn't in the list")

        codice_cve: int = np.random.randint(1000, 9999)
        if codice_cve > 9999 or codice_cve < 1000:
            logging.warn("The length of the CVE code is incorrect")


        pericolosita : list[str] = np.random.choice(["Little", "Medium", "Big"])
        if not pericolosita:
            logging.warn("The danger level was not selected")

        attacco : tuple[list[str], int, list[str]] = (nome_attacco, codice_cve, pericolosita)

        self.cursor.execute(
            "INSERT INTO attacchi (NOME_ATTACCO, CODICE_CVE, PERICOLOSITA) VALUES (?, ?, ?)", attacco )
        self.connessione.commit()


    def inserisci_log_traffico(self, time_stamp, ip_sorgente, ip_destinazione, porta, byte_trasmessi):
        log : tuple = (time_stamp, ip_sorgente, ip_destinazione, porta, byte_trasmessi)

        self.cursor.execute("INSERT INTO traffico (TIME_STAMP, IP_SORGENTE, IP_DESTINAZIONE, PORTA, BYTE_TRASMESSI) VALUES (?, ?, ?, ?, ?)", log)

        self.connessione.commit()

    def inserisci_allarme(self, id_log, id_attacco, score_confidenza, stato):
        data : tuple = (id_log, id_attacco, score_confidenza, stato)

        self.cursor.execute("INSERT INTO allarmi (ID_LOG, ID_ATTACCO, SCORE_CONFIDENZA, STATO) VALUES (?, ?, ?, ?)", data)

        self.connessione.commit()


print("The file structure was created correctly ✅")






