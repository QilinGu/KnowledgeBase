import pickle
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer

class RelationExtractor():
    def __init__(self):
        pass

    def train(self, feature_matrix, label_array):
        pass

    def test(self, test_set):
        pass

training_list = pickle.load(open('/home/ezio/filespace/data/training_list.data', 'rb'))
testing_list = pickle.load(open('/home/ezio/filespace/data/testing_list.data', 'rb'))
ds = SupervisedDataSet(11, 1)
for sample in training_list:
    ds.addSample(sample[3:-1], sample[-1])
net = buildNetwork(11, 40, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds)
trainer.train()
# trainer.trainUntilConvergence()
