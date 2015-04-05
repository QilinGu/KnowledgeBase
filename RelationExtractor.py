import pickle
import time
import numpy
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer

class RelationExtractor():
    def __init__(self, inCount, outCount):
        self.inCount = inCount
        self.outCount = outCount
        self.net = FeedForwardNetwork()
        inLayer = LinearLayer(inCount)
        hiddenLayer = SigmoidLayer(100)
        outLayer = SigmoidLayer(outCount)
        self.net.addInputModule(inLayer)
        self.net.addModule(hiddenLayer)
        self.net.addOutputModule(outLayer)
        in_to_hidden = FullConnection(inLayer, hiddenLayer)
        hidden_to_out = FullConnection(hiddenLayer, outLayer)
        self.net.addConnection(in_to_hidden)
        self.net.addConnection(hidden_to_out)
        self.net.sortModules()

    def set_data(self, feature_list, label_list):
        self.ds = SupervisedDataSet(self.inCount, self.outCount)
        for x, y in zip(feature_list, label_list):
            self.ds.addSample(x, y)
        self.trainer = BackpropTrainer(self.net, self.ds)

    def train(self):
        return self.trainer.train()

    def apply(self, feature_list):
        return [self.net.activate(feature)[0] for feature in feature_list]

    def evaluate(self, feature_list, label_list):
        predicate = numpy.array(self.apply(feature_list))
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

training_list = pickle.load(open('/home/ezio/filespace/data/training_list.data', 'rb'))
testing_list = pickle.load(open('/home/ezio/filespace/data/testing_list.data', 'rb'))
training_feature_list = [sample[3:-1] for sample in training_list]
training_label_list = [sample[-1] for sample in training_list]
testing_feature_list = [sample[3:-1] for sample in testing_list]
feature_count = len(training_feature_list[0])
extractor = RelationExtractor(feature_count, 1)
extractor.set_data(training_feature_list, training_label_list)

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
    # label = all_ds['target'][:, 0]
    # predicate = numpy.array([net.activate(vec)[0] for vec in all_ds['input']]) > 0
    print(evaluate(predicate, label))


# trainer.trainUntilConvergence()

'''
