import logging
import pandas as pd
import time
import Security_init
import joblib


class SecurityAnalyzer:
    def __init__(self):
        self.db = Security_init.Datamanager()
        self.db.crea_allarmi()
        self.ultimo_id_analizzato = 0

        try:
            self.model = joblib.load('security_model.pkl')
            print("🧠 AI Brain loaded successfully! The predictive guardian is active.")
        except FileNotFoundError:
            logging.warning('The file security_model.pkl was not found.')
            self.model = None

    def run_analysis(self):
        if self.model is None:
            print("Cannot start analysis without a valid model file.")
            return

        while True:
            df = pd.read_sql(f'SELECT * FROM traffico WHERE ID_LOG > {self.ultimo_id_analizzato}',
                             con=self.db.connessione)

            if not df.empty:
                X_byte = pd.to_numeric(df['BYTE_TRASMESSI'], errors='coerce')
                X_porta = pd.to_numeric(df['PORTA'], errors='coerce')

                X = pd.DataFrame({'BYTE_TRASMESSI': X_byte, 'PORTA': X_porta})
                predizioni = self.model.predict(X)

                df['PREDICT'] = predizioni
                df_anomalie = df[df['PREDICT'] == 1]

                for index, row in df_anomalie.iterrows():
                    id_log = row['ID_LOG']
                    id_attacco: int = 2
                    score_confidenza: float = 0.95
                    stato: str = 'Attivo'

                    self.db.inserisci_allarme(id_log, id_attacco, score_confidenza, stato)
                    print(f"⚠️ ATTACK INTERCEPTED! Alarm triggered for log ID: {id_log}")

                self.ultimo_id_analizzato = df['ID_LOG'].iloc[-1]
                print(f"Round completed... analyzed up to Log ID: {self.ultimo_id_analizzato}")

            else:
                print("Round completed... no new traffic detected")

            time.sleep(1)


if __name__ == "__main__":
    analyzer = SecurityAnalyzer()
    analyzer.run_analysis()
