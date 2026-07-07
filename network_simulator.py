import logging
import time
import numpy as np
from Security_init import Datamanager

class TrafficSimulator:
    def __init__(self):
        self.db = Datamanager()
        self.db.crea_log_traffico()
        self.ip_aziendali = ["192.168.1.10", "192.168.1.25", "192.168.1.50"]
        self.ip_esterni = ["8.8.8.8", "142.250.184.14", "23.45.67.89"]
        self.porte_rete = [80, 443, 22, 3389]

    def run_simulation(self):
        while True:
            tempo = time.time()
            dado: int = np.random.randint(100)

            if dado <= 85:
                print(dado)
                ip_sorgente = np.random.choice(self.ip_aziendali)
                ip_destinazione = np.random.choice(self.ip_esterni)
                byte_trasmessi = np.random.randint(100, 500000)
                porta = np.random.choice(self.porte_rete)
            else:
                ip_sorgente = "185.220.101.5"
                ip_destinazione = "192.168.1.10"
                porta = 80
                byte_trasmessi = np.random.randint(2000000, 5000000)
                logging.warning("Attention please, data are under attack!!!!!!!")

            self.db.inserisci_log_traffico(tempo, ip_sorgente, ip_destinazione, porta, byte_trasmessi)

            time.sleep(2)
            print('The file was created correct')

if __name__ == "__main__":
    simulator = TrafficSimulator()
    simulator.run_simulation()