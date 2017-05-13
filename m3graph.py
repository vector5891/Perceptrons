# m3graph

import tensorflow as tf

x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

z = 3*y*y + 2*x*y + 5*x*x - 6
#z = 3*tf.pow(y,2) + 2*x*y + 5*tf.pow(x,2) - 6

s = tf.Session()
wr = tf.train.SummaryWriter(".", s.graph) # Keep logs in current directory

# Instead of running scalar inputs through one at a time, we can send
# vectors of inputs.
print(s.run(z, {x: [3.2, 4.4],
                y: [9.1, 10.2]}))

# Flush and close the log files
wr.close()
