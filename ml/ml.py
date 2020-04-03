import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle

from exams.models import Exam

def create_model(predict):
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


def get_best_model(predict, percentage):
    model = 0
    best = 0
    while (best * 100 < percentage):
        model, acc = create_model(predict)
        if acc > best:
            best =  acc
    
    return model


def add_new_data(x, y, model_name):
    model = get_model(model_name)
    new_y = (y/100)*20
    model.fit([x], [new_y])
    save_model(model, model_name)


def get_exam_prediction(exam_number, course_id, study_hours):
    if(exam_number > 2):
        exam_number = 3

    # Get the model
    model = get_model_by_exam_number(exam_number)

    previous_exams_score = []

    exams_to_get = exam_number - 1

    prev_exams = Exam.objects.filter(course_id=course_id, is_hidden=False).order_by('-exam_number')
    for i in range(0, exams_to_get):
        exam = prev_exams[i]

        # If exam hasn't be graded, return
        if exam.final_score == 0:
            return -1

        score = (exam.final_score / 100) * 20
        previous_exams_score.insert(0, score)

    if exam_number > 2:
        return (model.predict(np.array( [ [previous_exams_score[0], previous_exams_score[1], -(study_hours)] ] ))[0])/20 * 100
    elif exam_number == 2:
        return (model.predict(np.array( [ [previous_exams_score[0], study_hours] ] ))[0])/20 * 100
    else:
        return (model.predict(np.array( [ [ study_hours ] ] ))[0])/20 * 100
     
def get_hours_prediction(exam_number, course_id, predicted_score):
    # Get the model
    model = get_model_by_exam_number(exam_number)

    best_hours = 1
    best_difference = 0
    for x in range(0, 100):
        exam_score = get_exam_prediction(exam_number, course_id, x)

        # If exam hasn't be graded, return
        if exam_score == -1:
            return exam_score

        diff = predicted_score - exam_score 
        if x == 0:
            best_difference = diff
        elif diff < best_difference and diff >= 0:
            best_difference = diff
            best_hours = x
            
        if diff < 0:
            break

    return best_hours

def get_model_by_exam_number(exam_number):
    if exam_number==1:
        return get_model("exam1.bi")
    elif exam_number==2:
        return get_model("exam2.bi")
    elif exam_number==3:
        return get_model("exam3.bi")
    else:
        return None

"""
# Import data
math = pd.read_csv("ml/data/student-mat.csv", sep=";")
por = pd.read_csv("ml/data/student-por.csv", sep=";")

# Merge data
data = math.append(por)

# data to predict
predict = "G3"
# predict = "G2"
# predict = "G1"

data = data[["G1", "G2", "G3", "studytime"]]
# data = data[["G1", "G2", "studytime"]]
# data = data[["G1", "studytime"]]

# data = data[["G1", "G2", "G3", "studytime", "failures", "absences", "sex"]]
# data["sex"].replace({"F": "0", "M": "1"}, inplace=True)
"""

"""
model = get_best_model(predict, 15)
# save_model(model, "exam3.bi")
# save_model(model, "exam2.bi")
# save_model(model, "exam1.bi")
"""

"""
model = get_model("exam3.bi")
# model = get_model("exam2.bi")
# model = get_model("exam1.bi")
"""

"""
x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

# Predict the test data
predictions = model.predict(x_test)

# Print results
print('\nPredictions:')
for x in range(len(predictions)):
  # Print prediction, input data, actual value
  print(predictions[x], x_test[x], y_test[x])
"""


"""
# print_coefficient_and_intercept(model)

# print("prediction: ", model.predict(np.array( [ [11, 13, 2, 0, 4, 1] ] ) ) )

# print("prediction: ", model.predict(np.array( [ [11, 13, 2] ] ) ) )

# print("prediction: ", model.predict(np.array( [ [11, 13, 0] ] ) )/20 * 100 )

# print("prediction method: ", get_exam_prediction(3, [11, 13, -1] ) )

# add_new_data([10, 12, 2, 0, 0], 11, "study.bi")

# print (get_prediction("exam3.bi", [10, 12, 2, 0, 0]))
"""