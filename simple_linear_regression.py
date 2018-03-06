import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt


def main():

    data_frame = pd.read_csv('PierceCricketData.csv')
    temp = data_frame['Temp']
    chirps = data_frame['Chirps']
    plt.plot(chirps,temp,'bx')
    plt.show()    

    y = tf.placeholder(tf.float32, shape=(temp.size))
    x = tf.placeholder(tf.float32, shape=(chirps.size))    

    a = tf.Variable(0.5)
    b = tf.Variable(5.3)

    nf = 1e-2

    
    
    y_pred = tf.add(tf.multiply(x,a),b)

    loss = tf.reduce_mean(tf.squared_difference(y,y_pred))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)

    train = optimizer.minimize(loss)
    
    init = tf.global_variables_initializer()

    with tf.Session() as sess:

        sess.run(init)
        a_ = b_ = x_ = y_ = 0
        for _ in range(9000):
            t_,loss_ ,a_,b_,x_,y_= sess.run([train,loss,a,b,x,y],feed_dict={x : chirps, y: temp})

            if _ % 10 == 0:
                print(loss_,a_,b_)

        plt.plot(chirps,a_*chirps + b_)
        plt.plot(chirps,temp,'bx')
        plt.show()
if __name__ == "__main__":
    main()
