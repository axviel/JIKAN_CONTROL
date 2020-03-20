import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle


def create_model(predict, data_to_use):
    data = pd.read_csv("data/student-mat.csv", sep=";")

    # data that we are going to use
    data = data[data_to_use]

    data["sex"].replace({"F": "0", "M": "1"}, inplace=True)

    # remove the prediction data
    x = np.array(data.drop([predict], 1))
    y = np.array(data[predict])

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    accuracy = linear.score(x_test, y_test)
    print("model accuracy: ", accuracy * 100)
    return linear, accuracy


def save_model(model, name):
    with open("ml/ml_models/" + name, "wb") as f:
        pickle.dump(model, f)


def get_model(name):
    save = open("ml/ml_models/" + name, "rb")
    return pickle.load(save)


def print_coefficient_and_intercept(model):
    print("Co: \n", model.coef_)
    print("Int: \n", model.intercept_)


def get_best_model(predict, data, percentage):
    model = 0
    best = 0
    while (best * 100 < percentage):
        model, acc = create_model(predict, data)
        if acc > best:
            best =  acc
    
    return model


def add_new_data(x, y, model_name):
    model = get_model(model_name)
    new_y = (y/100)*20
    model.fit([x], [new_y])
    save_model(model, model_name)


def get_exam_prediction(exam_number, data):
    model = None
    if exam_number==1:
        model = get_model("exam1.bi")
        # only for testing
        if data == None:
            data = [3, 1, 2]
    elif exam_number==2:
        model = get_model("exam2.bi")
        # only for testing
        if data == None:
            data = [15, 3, 0, 2]
    elif exam_number==3:
        model = get_model("exam3.bi")
        # only for testing
        if data == None:
            data = [15, 11, 1, 0, 4]
    else:
        return None
    ans = (model.predict([data])[0])/20 * 100
    return ans


# data to predict
# predict = "G3"

# data = ["G1", "G2", "G3", "studytime", "failures", "absences", "sex"]

# model = get_best_model(predict, data, 97)
# save_model(model, "study.bi")

# model = get_model("study.bi")

# print_coefficient_and_intercept(model)

# print("prediction: ", model.predict([[10, 12, 2, 0, 0, 0]])[0])

# add_new_data([10, 12, 2, 0, 0], 11, "study.bi")

# print (get_prediction("exam3.bi", [10, 12, 2, 0, 0]))
