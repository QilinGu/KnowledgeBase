import pickle
import time
import numpy
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer
#from sklearn import svm

class NeuralNetwork():

    def __init__(self, hidden_counts, training_list, learning_rate, balance_num):
        self.training_list = training_list
        self.set_network(len(training_list[0]) - 4, hidden_counts, 1)
        self.set_trainer(learning_rate, balance_num)

    def set_network(self, in_count, hidden_counts, out_count):
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

    def set_trainer(self, learning_rate, balance_num):
        self.origin_ds = SupervisedDataSet(self.in_count, self.out_count)
        self.balance_ds = SupervisedDataSet(self.in_count, self.out_count)
        for sample in self.training_list:
            feature = sample[3:-1]
            label = sample[-1]
            self.origin_ds.addSample(feature, label)
            if label == 1:
                for i in range(balance_num): self.balance_ds.addSample(feature, label)
            else:
                self.balance_ds.addSample(feature, label)
        self.learning_rate = learning_rate
        self.balance_num = balance_num
        self.origin_trainer = BackpropTrainer(self.net, self.origin_ds, learningrate = learning_rate)
        self.balance_trainer = BackpropTrainer(self.net, self.balance_ds, learningrate = learning_rate)

    def origin_train(self):
        return self.origin_trainer.train()

    def pos_train(self):
        return self.pos_trainer.train()

    def balance_train(self):
        return self.balance_trainer.train()

    def predicate_score(self, feature_list):
        return [self.net.activate(feature)[0] for feature in feature_list]

    def predicate_label(self, feature_list):
        score_list = self.predicate_score(feature_list)
        return [1 if score > 0.5 else 0 for score in score_list]

    def evaluate(self):
        predicate = numpy.array(self.predicate_label(self.origin_ds['input']))
        label = self.origin_ds['target'][:, 0].astype('int32')
        assert len(predicate.shape) == 1
        assert len(label.shape) == 1
        positive_true = numpy.logical_and(label, predicate).sum()
        positive_predicate = predicate.sum()
        positive_label = label.sum()
        if positive_predicate == 0: positive_predicate = 1
        if positive_label == 0: positive_label = 1
        p = positive_true / positive_predicate
        r = positive_true / positive_label
        if p * r == 0: f1 = 0
        else: f1 = 2 * p * r / (p + r)
        return positive_true, positive_predicate, positive_label, p, r, f1

# 特征列表，标签列表
training_list = pickle.load(open('/home/ezio/filespace/data/training_list.data', 'rb'))
testing_list = pickle.load(open('/home/ezio/filespace/data/testing_list.data', 'rb'))
print('pickle load done')
feature_count = len(training_list[0]) - 4

feature_list = [sample[3:-1] for sample in training_list]
label_list = [sample[-1] for sample in training_list]
testing_feature_list = [sample[3:-1] for sample in testing_list]

'''
clf = svm.SVC()
clf.fit(feature_list, label_list)
print('svm fit done')
predicate_list = clf.predict(feature_list)
'''

net = NeuralNetwork([100], training_list, 0.001, 30)
begin = time.time()
end = time.time()
print('train time:', end - begin)
