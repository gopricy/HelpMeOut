import os
import tensorflow as tf
from tensorflow.contrib import rnn
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Turn off TensorFlow warning message in program output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# configurations

# training and test files
trainning_data_file = "affective_training.csv"
test_data_file = "affective_test.csv"

# column numbers for input and output data
x_start=0
x_end=7
y_start=8
y_end=9

# input and output range
x_range=(0, 1)
y_range=(0, 1)

#model parameters
#learning rate
lr = 1e-4
training_epochs = 100
log_step = 20
time_steps = 1
# hidden LSTM units
num_units = 128
# input size
n_input = x_end - x_start + 1
# learning rate for adam
learning_rate = 1e-3
# output size
n_output = y_end - y_start + 1
# size of batch
batch_size = 1000
# LSTM layers
layer_num = 2


# Load training data set from CSV file
training_data_df = pd.read_csv(trainning_data_file, dtype=float)
# Load testing data set from CSV file
test_data_df = pd.read_csv(test_data_file, dtype=float)

# Pull out columns for X (data to train with) and Y (value to predict)
X_training = training_data_df.values[:,x_start:x_end+1]
Y_training = training_data_df.values[:,y_start:y_end+1]
X_test = test_data_df.values[:,x_start:x_end+1]
Y_test = test_data_df.values[:,y_start:y_end+1]

# All data needs to be scaled to a small range like 0 to 1 for the neural
# network to work well. Create scalers for the inputs and outputs.
X_scaler = MinMaxScaler(feature_range=x_range)
Y_scaler = MinMaxScaler(feature_range=y_range)

# Scale both the training inputs and outputs
X_scaled_training = X_scaler.fit_transform(X_training)
Y_scaled_training = Y_scaler.fit_transform(Y_training)

# It's very important that the training and test data are scaled with the same scaler.
X_scaled_test = X_scaler.transform(X_test)
Y_scaled_test = Y_scaler.transform(Y_test)



X = tf.placeholder(tf.float32, [None, time_steps, n_input])
y = tf.placeholder(tf.float32, [None, n_output])
keep_prob = tf.placeholder(tf.float32)


def lstm_cell(size, keep_prob):
	lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(size, forget_bias=0.0, state_is_tuple=True)
	lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=keep_prob)
	return lstm_cell


# call MultiRNNCell to get multilayer LSTM
mlstm_cell = rnn.MultiRNNCell(
	[lstm_cell(num_units, keep_prob) for _ in range(layer_num)], 
	state_is_tuple=True)

# initialize the stat with all 0
init_state = mlstm_cell.zero_state(batch_size, dtype=tf.float32)


# unfold the calculation in time order
outputs = list()
state = init_state
with tf.variable_scope('RNN'):
	for timestep in range(time_steps):
		if timestep > 0:
			tf.get_variable_scope().reuse_variables()
		# state saves the status fo each LSTM layer
		(cell_output, state) = mlstm_cell(X[:, timestep, :], state)
		outputs.append(cell_output)
h_state = outputs[-1]


# set variables
#weight
W = tf.Variable(tf.truncated_normal([num_units, n_output], stddev=0.1), dtype=tf.float32, name="Weight")
#bias
b = tf.Variable(tf.constant(0.1, shape=[n_output]), dtype=tf.float32, name="Bias")
y_pre = tf.nn.softmax(tf.matmul(h_state, W) + b)

# loss and evaluation
with tf.variable_scope('train'):
	#loss = tf.reduce_mean(tf.squared_difference(y_pre, y))
	loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_pre, labels=y))
	train_op = tf.train.AdamOptimizer(lr).minimize(loss)

	correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(y, 1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


sess = tf.Session()


with tf.variable_scope('logging'):
	tf.summary.scalar('current_cost', loss)
	summary=tf.summary.merge_all()





# Use a saver to save the variables
saver = tf.train.Saver(max_to_keep = 5)# if not set, by default this is 5

training_writer = tf.summary.FileWriter("./logs/training", sess.graph)



sess.run(tf.global_variables_initializer())
for i in range(training_epochs):
	# batch_x=X_scaled_training[(i%10)*batch_size:(i+1)%10*batch_size]
	# batch_y=Y_scaled_training[(i%10)*batch_size:(i+1)%10*batch_size]
	# if batch_x.size == 0:
	# 	batch_x=X_scaled_training[900:]
	# if batch_y.size == 0:
		# batch_y=Y_scaled_training[900:]
	batch_x=X_scaled_training
	batch_y=Y_scaled_training
	batch_x=batch_x.reshape(batch_size, time_steps, n_input)
	#_batch_size = 128
	#batch = mnist.train.next_batch(_batch_size)
	#batch=???????????????????????????????????????????????????
	if (i+1)%log_step == 0:
		train_accuracy, training_summary = sess.run([accuracy, summary], feed_dict={
			#X: batch[0], y: batch[1], keep_prob: 1.0, batch_size: _batch_size})
			X: batch_x, y: batch_y, keep_prob: 1.0})
		print "Step %d, training accuracy %g" % ((i+1), train_accuracy)
		los=sess.run(loss, feed_dict={X: batch_x, y: batch_y, keep_prob: 1.0})
		print "Loss %d" % los
		save_path = "./logs/modules/%04d.ckpt" % i
		saver.save(sess, save_path)
		training_writer.add_summary(training_summary, i)
	#sess.run(train_op, feed_dict={X: batch[0], y: batch[1], keep_prob: 0.5, batch_size: _batch_size})
	sess.run(train_op, feed_dict={X: batch_x, y: batch_y, keep_prob: 0.5})

# print "test accuracy %g" % sess.run(accuracy, feed_dict={
# 	#X: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0, batch_size: mnist.test.images.shape[0]})
# 	X: X_scaled_test, y: Y_scaled_test, keep_prob: 1.0})
