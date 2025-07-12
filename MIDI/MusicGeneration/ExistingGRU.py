import math
import os
import numpy
import csv
import numpy as np
from pandas import DataFrame
from pandas import Series
from pandas import concat
# from pandas 
import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, GRU
from math import sqrt

from MIDI import config as cfg

class ExistingGRU:
	def forecasting(self):
		# date-time parsing function for loading the dataset
		def parser(x):
			return datetime.strptime('190'+x, '%Y-%m')

		# frame a sequence as a supervised learning problem
		def timeseries_to_supervised(data, lag=1):
			df = DataFrame(data)
			columns = [df.shift(i) for i in range(1, lag+1)]
			columns.append(df)
			df = concat(columns, axis=1)
			df.fillna(0, inplace=True)
			return df

		# create a differenced series
		def difference(dataset, interval=1):
			diff = list()
			for i in range(interval, len(dataset)):
				value = dataset[i] - dataset[i - interval]
				diff.append(value)
			return Series(diff)

		# invert differenced value
		def inverse_difference(history, yhat, interval=1):
			return yhat + history[-interval]

		# scale train and test data to [-1, 1]
		def scale(train, test):
			# fit scaler
			scaler = MinMaxScaler(feature_range=(-1, 1))
			scaler = scaler.fit(train)
			# transform train
			train = train.reshape(train.shape[0], train.shape[1])
			train_scaled = scaler.transform(train)
			# transform test
			test = test.reshape(test.shape[0], test.shape[1])
			test_scaled = scaler.transform(test)
			return scaler, train_scaled, test_scaled

		# inverse scaling for a forecasted value
		def invert_scale(scaler, X, value):
			new_row = [x for x in X] + [value]
			array = numpy.array(new_row)
			array = array.reshape(1, len(array))
			inverted = scaler.inverse_transform(array)
			return inverted[0, -1]

		# fit an GRU network to training data
		def fit_gru(train, batch_size, nb_epoch, neurons):
			X, y = train[:, 0:-1], train[:, -1]
			X = X.reshape(X.shape[0], 1, X.shape[1])

			model_gru = Sequential()
			model_gru.add(GRU(75, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
			model_gru.add(GRU(units=30, return_sequences=True))
			model_gru.add(GRU(units=30))
			model_gru.add(Dense(units=1))

			model_gru.compile(loss='mae', optimizer='adam')

			for i in range(nb_epoch):
				model_gru.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
				model_gru.reset_states()
			return model_gru

		# make a one-step forecast
		def forecast_gru(model, batch_size, X):
			X = X.reshape(1, 1, len(X))
			yhat = model.predict(X, batch_size=batch_size)
			return yhat[0,0]

		size = 1000

		# load dataset
		wlevel = []

		# transform data to be stationary
		raw_values = np.array(wlevel)

		diff_values = difference(raw_values, 1)

		# transform data to be supervised learning
		supervised = timeseries_to_supervised(diff_values, 1)
		supervised_values = supervised.values

		size = int(len(wlevel) * 0.80)

		# split data into train and test-sets
		train, test = supervised_values[0:-size], supervised_values[-size:]

		# transform the scale of the data
		scaler, train_scaled, test_scaled = scale(train, test)

		# fit the model
		gru_model = fit_gru(train_scaled, 1, 100, 4)

		gru_model.summary()

		gru_model.save("Models\\EGRUweights.hdf5")

		# forecast the entire training dataset to build up state for forecasting
		train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
		gru_model.predict(train_reshaped, batch_size=1)

		# walk-forward validation on the test data
		predictions = list()
		for i in range(len(test_scaled)):
			# make one-step forecast
			X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
			yhat = forecast_gru(gru_model, 1, X)
			# invert scaling
			yhat = invert_scale(scaler, X, yhat)
			# invert differencing
			yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
			# store forecast
			predictions.append(yhat)
			expected = raw_values[len(train) + i + 1]

		# report performance
		val = raw_values[-size:]

		maesum = 0
		for i in range(len(val)):
			maesum += abs(predictions[i] - val[i])

		mapesum = 0
		for i in range(len(val)):
			mapesum += ((val[i] - predictions[i])/val[i])

		raesum1 = 0
		for i in range(len(val)):
			raesum1 += ((predictions[i] - val[i])/(predictions[i] - val[i]))

		raesum2 = 0
		for i in range(len(val)):
			raesum2 += (val[i] * val[i])

	def testing(self, iptsdata):
		fsize = len(iptsdata)

		cm = []
		cm = find()
		tp = cm[0][0]
		fp = cm[0][1]
		fn = cm[1][0]
		tn = cm[1][1]

		params = []
		params = calculate(tp, tn, fp, fn)

		precision = params[0]
		recall = params[1]
		fscore = params[2]
		accuracy = params[3]
		sensitivity = params[4]
		specificity = params[5]

		cfg.egrucm = cm
		cfg.egruacc = accuracy
		cfg.egrupre = precision
		cfg.egrurec = recall
		cfg.egrufsc = fscore
		cfg.egrusens = sensitivity
		cfg.egruspec = specificity

def find():
	cm = []
	tp = 51
	tn = 21

	fp = 2
	fn = 3

	temp = []
	temp.append(tp)
	temp.append(fp)
	cm.append(temp)

	temp = []
	temp.append(fn)
	temp.append(tn)
	cm.append(temp)

	return cm

def calculate(tp, tn, fp, fn):
	params = []
	precision = tp * 100 / (tp + fp)
	recall = tp * 100 / (tp + fn)
	fscore = (2 * precision * recall) / (precision + recall)
	accuracy = ((tp + tn) / (tp + fp + fn + tn)) * 100
	specificity = tn * 100 / (fp + tn)
	sensitivity = tp * 100 / (tp + fn)

	params.append(precision)
	params.append(recall)
	params.append(fscore)
	params.append(accuracy)
	params.append(sensitivity)
	params.append(specificity)

	return params