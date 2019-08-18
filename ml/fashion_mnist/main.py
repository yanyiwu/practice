from util import load_train_data_batch, softmax
import numpy as np

def main():
    weight = np.random.rand(28 * 28, 10)
    #print weight.shape
    bias = np.random.rand(10)
    #print softmax(np.arange(6).reshape(2,3).T).T
    #print bias.shape
    #print np.zeros((2,3)).reshape((6,))
    #print np.arange(6).reshape((2,3))
    #print np.arange(6).shape
    pos_cnt = 0
    total_cnt = 0
    batch_size = 2
    for _ in range(10):
        for feature, label in load_train_data_batch(batch_size):
            feature = feature/256.0
            feature = feature.reshape((batch_size, 28*28))
            pred = np.matmul(feature, weight)
            #print pred
            #print pred.shape
            #print bias.shape
            pred = pred + bias
            #print pred, pred.shape
            pred = softmax(pred.T).T
            pred_y = np.argmax(pred, axis=1)
            #print pred_y
            #print pred_y
            #print label
            pos_cnt += np.sum(np.equal(pred_y, label))
            total_cnt += label.shape[0]
    print pos_cnt, total_cnt, 1.0*pos_cnt/total_cnt

if __name__ == '__main__':
    main()
