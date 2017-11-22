import os
import tensorflow as tf
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler

# Turn off TensorFlow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

drop_keys = ['frame', 'name']
Y_keys = ['au_1_left','au_1_right','au_2_left','au_2_right','au_4_left','au_4_right','au_5','au_6','au_7','au_10','au_12_left','au_12_right','au_25','au_26','au_45_left','au_45_right']

# Load train data set from csv file
train_data_df = pd.read_csv('train.csv')

# Pull out columns for X (data to train with) and Y (value to predict)
X_train = train_data_df.drop(Y_keys+drop_keys, axis=1).values
Y_train = train_data_df[Y_keys].values

# Load test data set from csv file
test_data_df = pd.read_csv('test.csv')

X_test = test_data_df.drop(Y_keys+drop_keys, axis=1).values
Y_test = test_data_df[Y_keys].values


# All data needs to be scaled to a small range like 0 to 1 for the neural network to work well. Create scalers for the inputs and outputs.
X_scaler = MinMaxScaler(feature_range=(0, 1))
Y_scaler = MinMaxScaler(feature_range=(0, 1))

# Scale both the train inputs and outputs
X_scaled_train = X_scaler.fit_transform(X_train)
Y_scaled_train = Y_scaler.fit_transform(Y_train)

with open('scalerX.pkl', 'wb') as f:
	scaler_string = pickle.dump(X_scaler, f)
with open('scalerY.pkl', 'wb') as f:
	scaler_string = pickle.dump(Y_scaler, f)

# Scale both the test inputs and outputs
X_scaled_test = X_scaler.transform(X_test)
Y_scaled_test = Y_scaler.transform(Y_test)

print("x train shape: {}".format(X_scaled_train.shape))
print("y train shape: {}".format(Y_scaled_train.shape))

print("x test shape: {}".format(X_scaled_test.shape))
print("y test shape: {}".format(Y_scaled_test.shape))


# Define modle parameters
testNum = 1
learning_rate = 5e-4
training_epochs = 1000
last_training_epochs = 1000
display_step = 5

# Define how many inputs and outputs are in our neural network
number_of_inputs = len(train_data_df.keys()) - len(drop_keys) - len(Y_keys)
number_of_outputs = len(Y_keys)

# Define how many neurons we want in each layer of our neural network
layer_nodes = [150,150]

RUN_NAME = 'Run {} with {}('.format(testNum, learning_rate)
for nodes in layer_nodes:
	RUN_NAME += '_' + str(nodes)
RUN_NAME += ')' 

modelName = 'logs/{}/trained_model{}.ckpt'.format(RUN_NAME,last_training_epochs)

# Define the layers of the neural network itself

# Input Layer
with tf.variable_scope('input'):
	X = tf.placeholder(tf.float32, shape=(None, number_of_inputs))

# Hidden layers
input_sizes = [number_of_inputs] + layer_nodes
last_layer_output = X
for i in range(len(input_sizes)):
	if i == 0:
		continue

	with tf.variable_scope('layer_{}'.format(i)):
		weights = tf.get_variable(name='w{}'.format(i), shape=[input_sizes[i-1], input_sizes[i]], initializer=tf.contrib.layers.xavier_initializer())
		biases = tf.get_variable(name='b{}'.format(i), shape=[input_sizes[i]], initializer=tf.zeros_initializer())
		last_layer_output = tf.nn.relu(tf.matmul(last_layer_output, weights) + biases)

# Output Layer
with tf.variable_scope('output'):
	weights = tf.get_variable(name='w_out', shape=[input_sizes[-1], number_of_outputs], initializer=tf.contrib.layers.xavier_initializer())
	biases = tf.get_variable(name='b_out', shape=[number_of_outputs], initializer=tf.zeros_initializer())
	prediction = tf.nn.relu(tf.matmul(last_layer_output, weights) + biases)

# Define the cost function
with tf.variable_scope('cost'):
	Y = tf.placeholder(tf.float32, shape=(None, number_of_outputs))
	cost = tf.reduce_mean(tf.squared_difference(prediction, Y))

with tf.variable_scope('train'):
	optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# To log things for tensorboard
with tf.variable_scope('logging'):
	tf.summary.scalar('current_cost', cost)
	tf.summary.histogram('predicted_value', prediction)
	summary = tf.summary.merge_all()

saver = tf.train.Saver()

with tf.Session() as session:

	if(last_training_epochs == 0):
		# Run the global variable initializer to initialize all variables and layers
		session.run(tf.global_variables_initializer())
	else:
		saver.restore(session, modelName)

	training_writer = tf.summary.FileWriter('./logs/{}/training{}'.format(RUN_NAME, last_training_epochs+training_epochs), session.graph)
	testing_writer = tf.summary.FileWriter('./logs/{}/testing{}'.format(RUN_NAME, last_training_epochs+training_epochs), session.graph)

	for epoch in range(training_epochs):

		session.run(optimizer, feed_dict={X: X_scaled_train, Y: Y_scaled_train})

		if epoch % display_step == 0:
			training_cost, training_summary = session.run([cost, summary], feed_dict={X: X_scaled_train, Y: Y_scaled_train})
			testing_cost, testing_summary = session.run([cost, summary], feed_dict={X: X_scaled_test, Y: Y_scaled_test})
			print('Epoch: {}, Training Cost: {}, Testing Cost: {}'.format(epoch, training_cost, testing_cost))
			training_writer.add_summary(training_summary, epoch)
			testing_writer.add_summary(testing_summary, epoch)



	print('Training is complete!')

	final_training_cost = session.run(cost, feed_dict={X: X_scaled_train, Y: Y_scaled_train})
	final_testing_cost = session.run(cost, feed_dict={X: X_scaled_test, Y: Y_scaled_test})
	print('Final training cost: {}'.format(final_training_cost))
	print('Final testing cost: {}'.format(final_testing_cost))

	save_path = saver.save(session, 'logs/{}/trained_model{}.ckpt'.format(RUN_NAME, training_epochs+last_training_epochs))
	print('Model saved: {}'.format(save_path))

