import os
import tensorflow as tf
import pickle
from sklearn.preprocessing import MinMaxScaler

class MLnetwork:
	def __init__(self, modleFile):
		with open('scalerX.pkl', 'rb') as f:
			self.X_scaler = pickle.load(f)
		with open('scalerY.pkl', 'rb') as f:
			self.Y_scaler = pickle.load(f)

		# Define how many inputs and outputs are in our neural network
		number_of_inputs = 8
		number_of_outputs = 16

		# Define how many neurons we want in each layer of our neural network
		layer_nodes = [150,150,150]

		# Define the layers of the neural network itself

		# Input Layer
		with tf.variable_scope('input'):
			self.X = tf.placeholder(tf.float32, shape=(None, number_of_inputs))

		# Hidden layers
		input_sizes = [number_of_inputs] + layer_nodes
		last_layer_output = self.X
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
			self.prediction = tf.nn.relu(tf.matmul(last_layer_output, weights) + biases)

		self.session = tf.Session()
		self.saver = tf.train.Saver()
		self.saver.restore(self.session, modleFile)


	def run(self, emotion):

		# Scale both the test inputs and outputs
		X_scaled_test = self.X_scaler.transform(emotion)


		# Now that the neural network is trained, let's use it to make predictions for our test data.
		# Pass in the X testing data and run the "prediciton" operation
		Y_predicted_scaled = self.session.run(self.prediction, feed_dict={self.X: X_scaled_test})

		# Unscale the data back to it's original units (dollars)
		Y_predicted = self.Y_scaler.inverse_transform(Y_predicted_scaled)

		predicted_earnings = Y_predicted

		return predicted_earnings



# Turn off TensorFlow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

ml = MLnetwork('logs/Run 2 with 0.0005(_150_150_150)/trained_model2000.ckpt')

# print ml.run([[0.95,0.01,0.005,0.005,0.005,0.005,0.005,0.005]])
print ml.run([[0.005,0.01,0.005,0.005,0.005,0.005,0.005,0.95]])
