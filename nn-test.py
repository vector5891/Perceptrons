## nn-test -- using scikit-neuralnetwork

## Had a problem with "cannot import downsample"
## The solution was to make sure we have version 0.8.2 of Theano,
## rather than version 0.9.0. You can ensure this with:

##     pip install scikit-neuralnetwork
##     pip uninstall Theano
##     pip install Theano==0.8.2


from sknn.mlp import Regressor, Layer
import numpy as np
import sys
import logging

logging.basicConfig(
            format="%(message)s",
            level=logging.DEBUG,
            stream=sys.stdout)

# Suppose we learn 4 inputs: i0, i1, i2, i3
# And the output value should be 1.4*i1 + 0.5*i3 + 1.1*i2
def correct_formula(inputs):
    return (1.4 * inputs[1] +
            0.5 * inputs[3] +
            1.1 * inputs[2])

NUM_INPUTS = 4
NUM_EXAMPLES = 200
X_train = np.random.rand(NUM_EXAMPLES, NUM_INPUTS)
#print X_train
y_train = np.apply_along_axis( correct_formula, axis=1, arr=X_train )
#print y_train

nn = Regressor(
    layers=[
        Layer("Sigmoid", units=NUM_INPUTS),
        Layer("Linear")],
    learning_rate=0.02,
    n_iter=200)
nn.fit(X_train, y_train)

# Now let's try a few predictions --
NUM_TESTS = 5
x_test = np.random.rand(NUM_TESTS, NUM_INPUTS)
y_target = np.apply_along_axis( correct_formula, axis=1, arr=x_test )
y_test = nn.predict(x_test).T
print y_target
print y_test

# TODO: compute the average squared error between
# the test results and the target.
print "Average sq error:", np.square(y_target - y_test).sum() / NUM_TESTS
