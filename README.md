# Deep Cyber Security Twitter Bot

This is a quick write-up of the steps I took to train a Twitter bot using a recurrent neural network to generate "cyber security" tweets. The idea was inspired by Andrej Karpathy's excellent [blog post](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) on recurrent neural trained on character-level language models and the legendary [@DeepDrumpf](https://twitter.com/DeepDrumpf) Twitter bot created by Brad Hayes.

After experimenting with Justin Johnson's awesome [torch-rnn](https://github.com/jcjohnson/torch-rnn) on my laptop and training on some small sample sets I realized that I needed more computational power to speed up the training. Training performance of torch-rnn can be boosted by enabling GPU acceleration preferrably on a system with a beefy graphics card. While looking into the option of running an [Amazon EC2 GPU instance](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using_cluster_computing.html) I found a [tutorial](https://github.com/brotchie/torch-ubuntu-gpu-ec2-install) by James Brotchie together with a readily available AMI in the marketplace.

## Data collection

To collect tweets from the Twitter timelines of security companies I wrote a short Python script **timeline.py** that utilizes the [python-twitter](https://github.com/bear/python-twitter) library. A Twitter API key can be obtained by registering an app on the [Twitter Application Management](https://apps.twitter.com/) portal.

You can install the required python-twitter library using:
```
pip install python-twitter
```

## EC2 / torch-rnn setup

As mentioned I used James Brotchie's **torch-ubuntu-14.04-cuda-7.0-28** AMI (*ami-c79b7eac*) to spin up a GPU instance in AWS that served as a base for installing torch-rnn.

The following setup steps are a subset of the torch-rnn installation [tutorial](https://github.com/jcjohnson/torch-rnn#installation).

### HDF5
```
apt-get update
apt-get install libhdf5-dev
```

### torch packages
```
luarocks install torch
luarocks install nn
luarocks install optim
luarocks install lua-cjson
luarocks install cutorch
luarocks install cunn
```

### torch-hdf5
```
git clone https://github.com/deepmind/torch-hdf5
cd torch-hdf5
luarocks make hdf5-0-0.rockspec
cd ..
```

### torch-rnn
```
git clone https://github.com/jcjohnson/torch-rnn.git
cd torch-rnn
pip install -r requirements.txt
```

## Training/Sampling

Our sample data (stored in *data/twitter.txt*) has to be pre-processed before training can begin:
```
python scripts/preprocess.py --input_txt data/twitter.txt --output_h5 data/twitter.h5 --output_json data/twitter.json
```

The training will take several hours or even days depending on the selected [settings](https://github.com/jcjohnson/torch-rnn/blob/master/doc/flags.md#training). Here's the command I used for training @deep_cyber:
```
th train.lua -input_h5 data/twitter.h5 -input_json data/twitter.json -rnn_size 512
```
The only setting changed from default is the increased number of hidden units (512) in the neural network. Depending on the input data it's worth experimenting with the model and optimization options.

After training has produced checkpoint data files (stored in *cv/checkpoint_XXX.t7* by default) we can start sampling generated text. Again there are different [settings](https://github.com/jcjohnson/torch-rnn/blob/master/doc/flags.md#sampling) to experiment with:
```
th sample.lua -checkpoint cv/checkpoint_135700.t7 -length 1000 -temperature 0.4
```
For my sample data a temperature of 0.4 produced a good balance between novelty and valid tweets in my opinion.

## Example output

Here's an example output blob for the model trained above:
```
We're hosting the @FireEye Conference 2016 #CyberAware https://t.co/NabCuutoa4
@securitybrew: The Bit9 + Carbon Black Morning Coffee Headlines, Fear of Hacking Team http://t.co/o0qEAGOb
@sonaby We are not a great job ;)
@securitybrew: Protect your #Android devices and the #Internet. Click to learn more about our company http://t.co/tlrfn2ZF3E
@jeremyveix Hi James, the team think the samples of case study has been the process of the ticket.
@davemerkel Thank you for the feedback and we'll take a look.
@theCUBE: New Android apps are the critical infrastructure in the cloud. http://t.co/o8FaH1942u
```

The neural network apparently learned to make up random t.co links. While this is amazing and hilarious, I would like to prevent @deep_cyber from tweeting random links that potentially lead to any form of badness or unwanted content. That's why I'm replacing every link in the tweets with a link to a [description](http://armbues.github.io/deep_cyber.html) of "Deep Cyber Security". To prevent planting any rumours about the companies mentioned in the tweets I'm also replacing their Twitter handles with @deep_cyber.
