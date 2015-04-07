import pickle
# import time
import numpy
import random
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer

class NeuralNetwork():
    def __init__(self, in_count, hidden_counts, out_count):
        assert len(hidden_counts) > 0
        self.in_count = in_count
        self.out_count = out_count
        self.net = FeedForwardNetwork()
        in_layer = LinearLayer(in_count)
        hidden_layers = [SigmoidLayer(count) for count in hidden_counts]
        out_layer = SigmoidLayer(out_count)
        self.net.addInputModule(in_layer)
        for layer in hidden_layers: self.net.addModule(layer)
        self.net.addOutputModule(out_layer)
        in_connection = FullConnection(in_layer, hidden_layers[0])
        hidden_connections = [FullConnection(layer1, layer2) for layer1, layer2 in zip(hidden_layers[0:-1], hidden_layers[1:])]
        out_connection = FullConnection(hidden_layers[-1], out_layer)
        self.net.addConnection(in_connection)
        for connection in hidden_connections: self.net.addConnection(connection)
        self.net.addConnection(out_connection)
        self.net.sortModules()

    def set_trainer(self, ds, learning_rate):
        self.trainer = BackpropTrainer(self.net, ds, learningrate = learning_rate)

    def train(self):
        return self.trainer.train()

    def predicate_score(self, feature_list):
        return [self.net.activate(feature)[0] for feature in feature_list]

    def predicate_label(self, feature_list):
        score_list = self.predicate_score(feature_list)
        return [1 if score > 0.5 else 0 for score in score_list]

    def evaluate(self, feature_list, label_list):
        predicate = numpy.array(self.predicate_label(feature_list))
        label = numpy.array(label_list)
        positive_true = numpy.logical_and(label, predicate).sum()
        positive_predicate = predicate.sum()
        positive_label = label.sum()
        if positive_predicate == 0: positive_predicate = 1
        if positive_label == 0: positive_label = 1
        p = positive_true / positive_predicate
        r = positive_true / positive_label
        if p * r == 0: f1 = 0
        else: f1 = 2 * p * r / (p + r)
        return p, r, f1

# 特征列表，标签列表
training_list = pickle.load(open('/home/ezio/filespace/data/training_list.data', 'rb'))
testing_list = pickle.load(open('/home/ezio/filespace/data/testing_list.data', 'rb'))
training_feature_list = [sample[3:-1] for sample in training_list]
training_label_list = [sample[-1] for sample in training_list]
testing_feature_list = [sample[3:-1] for sample in testing_list]

# 设置数据集
feature_count = len(training_feature_list[0])
all_ds = SupervisedDataSet(feature_count, 1)
pos_ds = SupervisedDataSet(feature_count, 1)
neg_ds = SupervisedDataSet(feature_count, 1)
for x, y in zip(training_feature_list, training_label_list):
    all_ds.addSample(x, y)
    if y == 1:
        pos_ds.addSample(x, y)
    else:
        if random.randint(0, 100) == 0: neg_ds.addSample(x, y)

# 设置模型了
net = NeuralNetwork(feature_count, [100, 40], 1)
net.set_trainer(pos_ds, 0.001)


'''
print('begin train')
while True:
    begin = time.time()
    pos_trainer.train()
    neg_trainer.train()
    # all_trainer.train()
    end = time.time()
    print('train time:', end - begin)
    print('evaluate:')
    label = numpy.concatenate((pos_ds['target'][:, 0], neg_ds['target'][:, 0])) > 0
    predicate = numpy.array([net.activate(vec)[0] for vec in pos_ds['input']] + [net.activate(vec)[0] for vec in neg_ds['input']]) > 0
    print(evaluate(training_feature_list, training_label_list))


# trainer.trainUntilConvergence()

'''
