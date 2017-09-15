import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

w = tf.Variable(.3, dtype=tf.float32)
b = tf.Variable(-.3, dtype=tf.float32)

x = tf.placeholder(tf.float32)

linear_model = w*x + b
y = tf.placeholder(tf.float32)

loss = tf.reduce_sum(tf.square(linear_model - y))

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

x_train = [1,2,3,4]
y_train = [0,-1,-2,-3]

init = tf.global_variables_initializer()
sess = tf.Session()

sess.run(init)
for i in range(1000):
    sess.run(train, {x:x_train , y:y_train})

curr_w , curr_b, curr_loss = sess.run([w,b,loss], {x:x_train, y:y_train})

print("W: %s b: %s loss: %s"%(curr_w, curr_b, curr_loss))
sess.close()