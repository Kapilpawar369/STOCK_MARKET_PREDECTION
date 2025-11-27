import pickle
from sklearn.linear_model import LinearRegression

def train_and_save_model(X, y):
    model = LinearRegression()
    model.fit(X, y)

    with open("app/ml/models/trained_model.pkl", "wb") as file:
        pickle.dump(model, file)

    return model
