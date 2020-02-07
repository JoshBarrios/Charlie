# <h1>DarwinBot</h1>
 Training an LSTM to mimic the writing style of naturalist Charles Darwin.
 
 <h1>Installation</h1>
 
 This project was built in ubuntu 18.04.3 using Tensorflow 2.1. 
 This will require:
 <ul>
 <li>NVIDIA GPU drivers 418.x or higher</li> 
 <li>CUDA 10.1</li>
 <li>cuDNN SDK (>= 7.6)</li>
 <li>TensorRT 6.0 (recommended for speed)</li>
</ul>

You can find detailed instructions for these installations at <a href='https://www.tensorflow.org/install/gpu'>Tensorflow.org</a>. 
You may also choose to execute the code within a <a href='https://hub.docker.com/r/tensorflow/tensorflow/'>TensorFlow GPU Docker image</a>.

<h1>System Considerations</h1>

These networks were trained on a laptop NVIDIA 1050M. 40 training epochs took about 4 hours. The network isn't huge, but I would recommend using a GPU.

