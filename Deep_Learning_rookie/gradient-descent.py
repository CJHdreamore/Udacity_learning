#coding: utf-8

#vanilla gradient descent

while True:
    weights_grad = evalutae_gradient(loss_fun,data,weights)
    weights += -step_size * weights_grad  #perform parameter update

# vanilla Minibatch Gradient Descent

while True:
    data_batch =sample_training_data(data,256) # sample 256 examples
    weights_grad = evaluate_gradient(loss_fuc,data,weights)
    weights += - step_size * weights_grad  #perform parameter update