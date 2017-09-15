import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

'''def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_+b = tf.matmul(inputs,Weights) + biases
    
    
    l1 = add_layers(xs, 1,10,activation_function=tf.nn.relu)
    prediction = add_layer( l1,10,1,ac = none)
    return outputs
'''
x_data = np.linspace(-1, 1, 300)
x_data = x_data[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data)-0.5 + noise

##plt.scatter(x_data, y_data)
##plt.show()

xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32,[None, 1])
Weights = tf.Variable(tf.random_normal([1, 10]))
biases = tf.Variable(tf.zeros([1,10]) + 0.1)
Wx_plus_b = tf.matmul(Weights,xs) + biases

l1 = tf.nn.relu(Wx_plus_b)
Weights1 = tf.Variable(tf.random_normal([10, 1]))
biases1 = tf.Variable(tf.zeros([1,1]) + 0.1)
prediction = tf.matmul(Weights1,l1) + biases1

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),reduction_indices=[1]))
train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for _ in range(1000):
        sess.run(train, feed_dict={xs: x_data, ys:y_data})
        if _ % 50 == 0:
            print(_,sess.run(loss, feed_dict={xs: x_data, ys:y_data}))
