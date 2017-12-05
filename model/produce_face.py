import os
import tensorflow as tf
import pickle
from sklearn.preprocessing import MinMaxScaler
import argparse

pair = {
"sadness":0,
"contempt":1,
"disgust":2,
"anger":3,
"surprise":4,
"fear":5,
"happiness":6
}

parser = argparse.ArgumentParser()
parser.add_argument("--sadness", help="set the degree of sadness", default=0,
                    type=float)
parser.add_argument("--contempt", help="set the degree of contempt", default=0,
                    type=float)
parser.add_argument("--disgust", help="set the degree of disgust", default=0,
                    type=float)
parser.add_argument("--anger", help="set the degree of contempt", default=0,
                    type=float)
parser.add_argument("--surprise", help="set the degree of surprise", default=0,
                    type=float)
parser.add_argument("--fear", help="set the degree of fear", default=0,
                    type=float)
parser.add_argument("--happiness", help="set the degree of happiness", default=0,
                    type=float)

args = parser.parse_args()

class MLnetwork:
	def __init__(self, modleFile):
		with open('scalerX.pkl', 'rb') as f:
			self.X_scaler = pickle.load(f)
		with open('scalerY.pkl', 'rb') as f:
			self.Y_scaler = pickle.load(f)

		# Define how many inputs and outputs are in our neural network
		number_of_inputs = 7
		number_of_outputs = 16

		# Define how many neurons we want in each layer of our neural network
		layer_nodes = [100,100]

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

ml = MLnetwork('logs/Run 1 with 0.001(_100_100)/trained_model2000.ckpt')

# fear 0.35
# print ml.run([[0.01,0.005,0.005,0.005,0.005,0.35,0.0005]])
# fear 0.7
# print ml.run([[0.01,0.005,0.005,0.005,0.005,0.7,0.0005]])
# anger 0.35
# print ml.run([[0.,0.,0.,0.05,0.,0.,0.]])
# anger 0.7
# print ml.run([[0.,0.,0.,0.1,0.,0.,0.]])
# sup 0.7
# print ml.run([[0.01,0.005,0.005,0.005,0.7,0.005,0.0005]])
# sup 0.35 sad 0.35
# print ml.run([[0.35,0.005,0.005,0.005,0.35,0.005,0.0005]])
# cont 0.15 happy 0.35
# print ml.run([[0.,0.15,0.001,0.001,0.0,0.001,0.35]])
# cont 0.15
# print ml.run([[0.,0.15,0.,0.,0.0,0.0,0.0]])
# happy 0.35 fear 0.15
res = ml.run([[args.sadness * 0.6, args.contempt * 0.15, args.disgust * 0.0085, args.anger * 0.085, \
args.surprise * 0.7, args.fear * 0.18, args.happiness * 0.6]])

new_name = ""
args = vars(args)
for i in args:
    if args[i] > 0:
        if new_name:
            new_name += " | "
        new_name += i + "_" + str(args[i])

template_file = open('template.py','r')
new_file = open('{}.py'.format(new_name), 'w')
new_file.write(template_file.read())
new_file.write("chrName = 'ChrRachel'\n")

template_file.close()
aus = '<face type="facs" au="1_left" amount="{}"/><face type="facs" au="1_right" amount="{}"/>\
<face type="facs" au="2_left" amount="{}"/><face type="facs" au="2_right" amount="{}"/>\
<face type="facs" au="4_left" amount="{}"/><face type="facs" au="4_right" amount="{}"/>\
<face type="facs" au="5" amount="{}"/><face type="facs" au="6" amount="{}"/>\
<face type="facs" au="7" amount="{}"/><face type="facs" au="10" amount="{}"/>\
<face type="facs" au="12_left" amount="{}"/><face type="facs" au="12_right" amount="{}"/>\
<face type="facs" au="25" amount="{}"/><face type="facs" au="26" amount="{}"/>\
<face type="facs" au="45_left" amount="{}"/><face type="facs" au="45_right" amount="{}"/>'.format(*res[0])

new_file.write("def nextFace():\n")
new_file.write("    randSeq = [random.randint(0, 20) / 20.0 for i in range(16)]\n")
new_file.write("    global curFace\n")
new_file.write("    print 'Playing next face'\n")
new_file.write("    bml.execBML(chrName, '{}')\n".format(aus))
new_file.write("    # Increment index, reset when hit max\n")
new_file.write("    curFace = curFace + 1\n")
new_file.write("    if curFace >= faceAmt:\n")
new_file.write("    	curFace = 0\n")

# Run the update script
new_file.write("scene.removeScript('facialmovementdemo')\nfacialmovementdemo = FacialMovementDemo()\n\
scene.addScript('facialmovementdemo', facialmovementdemo)\n")

new_file.close()

print 'au:1_left\tamount:{:.2f}\nau:1_right\tamount:{:.2f}\n\
au:2_left\tamount:{:.2f}\nau:2_right\tamount:{:.2f}\n\
au:4_left\tamount:{:.2f}\nau:4_right\tamount:{:.2f}\n\
au:5\t\tamount:{:.2f}\nau:6\t\tamount:{:.2f}\n\
au:7\t\tamount:{:.2f}\nau:10\t\tamount:{:.2f}\n\
au:12_left\tamount:{:.2f}\nau:12_right\tamount:{:.2f}\n\
au:25\t\tamount:{:.2f}\nau:26\t\tamount:{:.2f}\n\
au:45_left\tamount:{:.2f}\nau:45_right\tamount:{:.2f}\n'.format(*res[0])