import os
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Turn off TensorFlow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load train data set from csv file
train_data_df = pd.read_csv('sales_data_train.csv', dtype=float)

Y_keys = ['total_earnings', 'critic_rating']

# Pull out columns for X (data to train with) and Y (value to predict)
X_train = train_data_df.drop(Y_keys, axis=1).values
Y_train = train_data_df[Y_keys].values


# Load test data set from csv file
test_data_df = pd.read_csv('sales_data_test.csv', dtype=float)

# Pull out columns for X (data to train with) and Y (value to predict)
X_test = test_data_df.drop(Y_keys, axis=1).values
Y_test = test_data_df[Y_keys].values



# All data needs to be scaled to a small range like 0 to 1 for the neural network to work well. Create scalers for the inputs and outputs.
X_scaler = MinMaxScaler(feature_range=(0, 1))
Y_scaler = MinMaxScaler(feature_range=(0, 1))

# Scale both the train inputs and outputs
X_scaled_train = X_scaler.fit_transform(X_train)
Y_scaled_train = Y_scaler.fit_transform(Y_train)

# Scale both the train inputs and outputs
X_scaled_test = X_scaler.transform(X_test)
Y_scaled_test = Y_scaler.transform(Y_test)

print(X_scaled_test.shape)
print(Y_scaled_test.shape)

print('Note: Y values were scaled by multiplying by {:.10f} and adding {:.4f}'.format(Y_scaler.scale_[0], Y_scaler.min_[0]))


# Define modle parameters
learning_rate = 0.001
training_epochs = 100
display_step = 5

# Define how many inputs and outputs are in our neural network
number_of_inputs = 8
number_of_outputs = 2

# Define how many neurons we want in each layer of our neural network
layer_nodes = [20,20,20,20,20]

RUN_NAME = 'Run with {}'.format(learning_rate)
for nodes in layer_nodes:
	RUN_NAME += '_' + str(nodes)

# Define the layers of the neural network itself

# Input Layer
with tf.variable_scope('input'):
	X = tf.placeholder(tf.float32, shape=(None, number_of_inputs))

# Layer i
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
	summary = tf.summary.merge_all()

saver = tf.train.Saver()

with tf.Session() as session:

	# Run the global variable initializer to initialize all variables and layers
	session.run(tf.global_variables_initializer())

	training_writer = tf.summary.FileWriter('./logs/{}/training'.format(RUN_NAME), session.graph)
	testing_writer = tf.summary.FileWriter('./logs/{}/testing'.format(RUN_NAME), session.graph)

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

	save_path = saver.save(session, 'logs/{}/trained_model.ckpt'.format(RUN_NAME))
	print('Model saved: {}'.format(save_path))