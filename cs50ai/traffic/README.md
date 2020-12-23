***Traffic***


For my convolutional neural network, I tried out various different specifications to end up with 
the current one. After the first convolution layer, I tried out different sizes of max-pooling and 
found the 3x3 pooling to be the best with respect to accuracy. After flattening the resulting data,
I tried to include one and two hidden layers with different numbers of nodes. Various dropout 
rates did not result in an improvement, so I stayed at a 0% dropout rate. For the output layer, 
I found that it was crucial to use the softmax activation function to achieve a reasonable 
accuracy in the model. 