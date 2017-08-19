import numpy as np
import pandas
from ggplot import *
import scipy
import matplotlib.pyplot as plt
import sys
import statsmodels.api as sm


"""
In this question, you need to:
1) implement the compute_cost() and gradient_descent() procedures
2) Select features (in the predictions procedure) and make predictions.

"""


def normalize_features(df):
    """
    Normalize the features in the data set.
    """
    mu = df.mean()
    sigma = df.std()

    if (sigma == 0).any():
        raise Exception("One or more features had the same value for all samples, and thus could " + \
                        "not be normalized. Please do not include features with only a single value " + \
                        "in your model.")
    df_normalized = (df - df.mean()) / df.std()

    return df_normalized, mu, sigma


def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values,
    and the values for our thetas.
    """
    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2 * m)

    return cost


def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.

    """

    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        prediction_values = np.dot(features, theta)
        theta = theta - alpha / m * np.dot((prediction_values - values), features)
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)

    return theta, pandas.Series(cost_history)
def plot_cost_history(alpha, cost_history):
    """This function is for viewing the plot of your cost history.
       # You can run it by uncommenting this

       #     plot_cost_history(alpha, cost_history)

       # call in predictions.

      #  If you want to run this locally, you should print the return value
      #  from this function.
       """

    cost_df = pandas.DataFrame({'Cost_History': cost_history,
                                'Iteration': range(len(cost_history)) })



    return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
          geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha)


def predictions_gradient(filename):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.

    Your prediction should have a R^2 value of 0.40 or better.
    You need to experiment using various input features contained in the dataframe.
    We recommend that you don't use the EXITSn_hourly feature as an input to the
    linear model because we cannot use it as a predictor: we cannot use exits
    counts as a way to predict entry counts.

    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~15%) of the data contained in
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with
    this computer on your own computer, locally.


    If you'd like to view a plot of your cost history, uncomment the call to
    plot_cost_history below. The slowdown from plotting is significant, so if you
    are timing out, the first thing to do is to comment out the plot command again.

    If you receive a "server has encountered an error" message, that means you are
    hitting the 30-second limit that's placed on running your program. Try using a
    smaller number for num_iterations if that's the case.

    If you are using your own algorithm/models, see if you can optimize your code so
    that it runs faster.
    '''
    dataframe = pandas.read_csv(filename)
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]


    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit') # converts categorical variable to indicator matrix

    features = features.join(dummy_units)


    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m)  # Add a column of 1s (y intercept)


    # Convert features and values to numpy arrays
    features_array = np.array(features)
    #print features_array
    values_array = np.array(values)


    # Set values for alpha, number of iterations.
    alpha = 0.1  # please feel free to change this value
    num_iterations = 75  # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array,
                                                            values_array,
                                                            theta_gradient_descent,
                                                            alpha,
                                                            num_iterations)

    #plot = None
    # -------------------------------------------------
    # Uncomment the next line to see your cost history
    # -------------------------------------------------
    #plot = plot_cost_history(alpha, cost_history)

    # Please note, there is a possibility that plotting
    # this in addition to your calculation will exceed
    # the 30 second limit on the compute servers.

    predictions = np.dot(features_array, theta_gradient_descent)
    return predictions,dataframe
#--------------------------------------------------------------
def predictions_least_squares(dataframe):
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'],
                                     prefix='unit')  # converts categorical variable to indicator matrix

    features = features.join(dummy_units)

    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    # features, mu, sigma = normalize_features(features)
    # features['ones'] = np.ones(m)  # Add a column of 1s (y intercept)


    # Convert features and values to numpy arrays
    features_array = np.array(features)
    # print features_array
    values_array = np.array(values)

    x = sm.add_constant(features_array)

    model = sm.OLS(values_array, x)
    results = model.fit()
    coef = results.params
    prediction_2 = results.predict(coef)


def compute_r_squared(data,predictions):
    #the sum of squares of residuals
    SSres = np.square(data - predictions).sum()
    #the total sum of squares,propotional to the variance of the data
    SStot = np.square(data - np.mean(data)).sum()
    r_squared = 1 - SSres / SStot
    return r_squared

predictions,turnstile_weather = predictions_gradient(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\turnstile_data_master_with_weather.csv')
print predictions_least_squares(turnstile_weather)
print predictions
#plt.figure()
#(turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins = 100)
#plt.show()

#print compute_r_squared(turnstile_weather['ENTRIESn_hourly'],predictions)




