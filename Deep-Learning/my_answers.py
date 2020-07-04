import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights: random on initialization
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate
        
        #### TODO: Set self.activation_function to your implemented sigmoid function ####
        
        # Note: in Python, you can define a function with a lambda expression,
        # as shown below.
        # FC Comment: note that the activation function is a sigmoid
        self.activation_function = lambda x : 1 / (1 + np.exp(-x)) 
                    

    def train(self, features, targets):
        ''' Train the network on batch of features and targets. 
        
            Arguments
            ---------
            
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):
            
            # Implement the forward pass function below
            final_outputs, hidden_outputs = self.forward_pass_train(X)
            # Implement the backproagation function below
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):
        ''' Implement forward pass here 
         
            Arguments
            ---------
            X: features batch

        '''
        #### Implement the forward pass here ####
        ### Forward pass ###
        
        # TODO: Hidden layer - Replace these values with your calculations.
        # FC Comment: inputs are the features and the weights...
        # FC Comment: outputs are result of the activation function...

        # inputs will be a combination of values and weights
        hidden_inputs = np.dot(X, self.weights_input_to_hidden)
        hidden_outputs = self.activation_function(hidden_inputs)
        # outputs are a result of inputs fed into an activation function

        # TODO: Output layer - Replace these values with your calculations.
        # FC Comment: do I need a 'final' activation function?
        # FC Comment: Remember, inputs are a combination of values and weights...
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output)
        # the activation function for final output is y = x... so just the final inputs
        final_outputs = final_inputs
        
        return final_outputs, hidden_outputs


    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation
         
            Arguments
            ---------
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        #### Implement the backward pass here ####
        ### Backward pass ###

        # TODO: Output error - Replace this value with your calculations.
        error = y - final_outputs # Output layer error is the difference between desired target and actual output.
        # FC Comment: Remember, this is the error of the node value
        # Q: Why don't we use the error_formula that we used in logistic regression?
        # A: Because in linear regression the activation function of the output is y=x, whose derivative is 1. 
        # There's also other output activation functions (relu commonly used in multi-lable classification).

        # TODO: Backpropagated error terms - Replace these values with your calculations.
        output_error_term = error

        # TODO: Calculate the hidden layer's contribution to the error
        # is this is the error connected to the weights?
        # if so, are these the weights in the hidden_error_term?
        hidden_error = np.dot(output_error_term, self.weights_hidden_to_output.T)
        # I think this is the error of the hidden nodes. 
        # if so, the hidden error should be 2 values. True!!!
        
        # FC Comment: in the video this was something like W * derivative of sigmoid of h
        # FC Comment: sigmoid of h is hidden outputs
        # FC Comment: so the second part of this is hidden_outputs * (1-hidden_outputs)
        hidden_error_term = hidden_error * hidden_outputs * (1-hidden_outputs)
        # FC Comment: this is where you are finding the error of the hidden outputs...
        # FC Comment: the hidden outputs are determined by the inputs and the input to hidden weights

        # SIDEBAR: for testing a single instance of the function
        # for x in X:
        #     delta_weights_i_h += hidden_error_term * x[:,None]
        # for h in hidden_outputs:
        #     print("change in weights:", output_error_term * h[:,None])
        #     delta_weights_h_o += output_error_term * h[:,None]        

        # Weight step (input to hidden)
        delta_weights_i_h += hidden_error_term * X[:,None]
        # Weight step (hidden to output)
        delta_weights_h_o +=  output_error_term * hidden_outputs[:,None]
        return delta_weights_i_h, delta_weights_h_o


    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step
         
            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        # update hidden-to-output weights with gradient descent step
        self.weights_hidden_to_output += self.lr * delta_weights_h_o / n_records
        # update input-to-hidden weights with gradient descent step
        self.weights_input_to_hidden += self.lr * delta_weights_i_h / n_records


    def run(self, features):
        ''' Run a forward pass through the network with input features. 
            Nearly identical to the forward_pass_train function (but different initial inputs)
            Use this function to make predictions after the model has been trained.
        
            Arguments
            ---------
            features: 1D array of feature values
        '''
        
        #### Implement the forward pass here ####
        # TODO: Hidden layer - replace these values with the appropriate calculations.
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer
        
        # TODO: Output layer - Replace these values with the appropriate calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        final_outputs = final_inputs # signals from final output layer 
        return final_outputs


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 2500
learning_rate = 0.75
hidden_nodes = 10
output_nodes = 1
