import torch
import torch.nn as nn

# Define the input size and output size for the linear layer
input_size = 5
output_size = 3

# Create an instance of the nn.Linear module
linear_layer = nn.Linear(input_size, output_size)

# Create some random input data
input_data = torch.randn(2, input_size)  # 2 samples, each with 'input_size' features

# Pass the input data through the linear layer
output = linear_layer(input_data)

# Print the input and output shapes
print("Input data shape:", input_data.shape)
print("Output shape:", output.shape)