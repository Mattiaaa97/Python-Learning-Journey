import joblib
import matplotlib.pyplot as plt
import pandas as pd
import Security_init
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.model_selection import train_test_split


class SecurityModelTrainer:
    def __init__(self):
        self.db = Security_init.Datamanager()
        self.model = RandomForestClassifier(n_estimators=100, random_state=0, max_depth=5)

    def prepare_data(self):
        file = pd.read_sql('SELECT * FROM traffico', con=self.db.connessione)

        file['LABEL'] = (file['BYTE_TRASMESSI'] > 1000000).astype(int)

        X_byte = pd.to_numeric(file['BYTE_TRASMESSI'], errors='coerce')
        X_porta = pd.to_numeric(file['PORTA'], errors='coerce')

        X = pd.DataFrame({'BYTE_TRASMESSI': X_byte, 'PORTA': X_porta})
        y = file['LABEL'].astype(int)

        return X, y

    def train_and_evaluate(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        print(f'The prediction is -> {y_pred}')

        accuracy = accuracy_score(y_test, y_pred)
        print(f'The result of accuracy -> {accuracy}')

        f1 = f1_score(y_test, y_pred)
        print(f'The result of f1 -> {f1}')

        precision = precision_score(y_test, y_pred)
        print(f'The result of precision -> {precision}')

        recall = recall_score(y_test, y_pred)
        print(f'The result of recall -> {recall}')

        matrice = confusion_matrix(y_test, y_pred)
        print(f'The result of matrix -> {matrice}')

        self.save_plot(matrice)

        joblib.dump(self.model, 'security_model.pkl')
        print("Model saved successfully as 'security_model.pkl'!")

    def save_plot(self, matrice):
        plt.figure(figsize=(6, 5))
        plt.imshow(matrice, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion Matrix - ML Security Model")
        plt.colorbar()
        plt.xlabel("Predicted Labels")
        plt.ylabel("True Labels")

        plt.show()

        plt.savefig('confusion_matrix_report.png', bbox_inches='tight')
        plt.close()
        print("The graph explains what the analysis involves")


if __name__ == "__main__":
    trainer = SecurityModelTrainer()
    X, y = trainer.prepare_data()
    trainer.train_and_evaluate(X, y)
