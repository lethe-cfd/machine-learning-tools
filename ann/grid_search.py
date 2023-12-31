# ============================================================================
# Grid search with cross validation to find the hyperparameters of the model.
# Author : Valérie Bibeau, Polytechnique Montréal, H4ck4th0n 2023
# ============================================================================

# ---------------------------------------------------------------------------
# Imports
from ann import *
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
from sklearn.model_selection import GridSearchCV
import pandas as pd
# Seed
np.random.seed(7)
# ---------------------------------------------------------------------------

# Read the data
file_path = '../database/mixer_database.csv'
X, Y = read_data(file_path)

# Set the features and the target values for the training and testing set
X_train, X_test, y_train, y_test, scaler_X, scaler_y = initial_setup(X, Y,
                                                                     test_size=0.3,
                                                                     random_state=42)
# Grid search
def create_model(units=1, layers=1, activation='tanh', optimizer='adamax'):
    model = Sequential()
    layer = 0
    while layer < layers:
        model.add(Dense(units, input_dim=7, kernel_initializer=keras.initializers.GlorotUniform(), activation=activation))
        layer += 1
    model.add(Dense(1, kernel_initializer=keras.initializers.GlorotUniform(), activation='linear'))
    model.compile(loss='mse', optimizer=optimizer, metrics=['mse'])
    return model

model = keras.wrappers.scikit_learn.KerasRegressor(build_fn=create_model, verbose=0)
epochs = [5000]
batch_size = [200]
units = [20,30,40]
layers = [2,3]
param_grid = dict(epochs=epochs,
                  batch_size=batch_size,
                  units=units,
                  layers=layers)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3, scoring='neg_mean_squared_error')
grid_result = grid.fit(X_train, y_train)

# Summarize results
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for i in range(len(params)):
    params[i]['mean'] = means[i]
    params[i]['std'] = stds[i]
df = pd.DataFrame(params)
df.to_excel('grid_search.xlsx')
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))