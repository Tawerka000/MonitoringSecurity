import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
import keras
selected_features = pd.read_csv('D:\Python\MonitoringSecurityProject\Datasets\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
selected_features = selected_features[[" Total Fwd Packets", " Total Backward Packets", " Fwd Packet Length Min",
                                       " Fwd Packet Length Mean", " Fwd Packet Length Std", " Bwd Packet Length Min",
                                       " Fwd Header Length", " Bwd Header Length", " Min Packet Length", " Packet Length Mean",
                                       " PSH Flag Count", " ACK Flag Count", " URG Flag Count", " Down/Up Ratio",
                                       " Average Packet Size", " Avg Fwd Segment Size", " Subflow Bwd Packets",
                                       " act_data_pkt_fwd", " min_seg_size_forward", " Label"]]
# Разделение на признаки и целевую переменную
X = {}
X = selected_features.drop(columns=[" Label"]).copy()
y = selected_features[" Label"].map(lambda x: False if x == 'BENIGN' else True)
X = pd.DataFrame({key: value.astype("float32") for key, value in X.items()})

# Разделение на тренировочный и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

import keras
from sklearn.base import BaseEstimator, ClassifierMixin

class KerasClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, layers=(64,), activation='relu'):
        self.layers = layers
        self.activation = activation
        self.model = self._build_model()

    def _build_model(self):
        model = keras.models.Sequential()
        for i, nodes in enumerate(self.layers):
            if i == 0:
                model.add(keras.layers.Dense(nodes, input_dim=X_train.shape[1], activation=self.activation))
            else:
                model.add(keras.layers.Dense(nodes, activation=self.activation))
        model.add(keras.layers.Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def fit(self, X, y):
        self.model.fit(X, y, epochs=10, batch_size=32)

    def predict(self, X):
        return (self.model.predict(X) > 0.5).astype(int)

# Определяем параметры для поиска по сетке (можете изменять диапазоны)
param_grid = {
    'layers': [(64,), (128,), (64, 32), (128, 64)],
    'activation': ['relu', 'tanh', 'sigmoid']
}

model = KerasClassifier()
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)

# Результаты поиска по сетке
print(f"Лучший результат: {grid_result.best_score_} при параметрах: {grid_result.best_params_}")