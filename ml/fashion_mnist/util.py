#coding: utf-8
import numpy as np
import struct

def decode_idx3_ubyte(idx3_ubyte_file):
    """
    解析idx3文件的通用函数
    :param idx3_ubyte_file: idx3文件路径
    :return: 数据集
    """
    # 读取二进制数据
    bin_data = open(idx3_ubyte_file, 'rb').read()

    # 解析文件头信息，依次为魔数、图片数量、每张图片高、每张图片宽
    offset = 0
    fmt_header = '>iiii'
    magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
    #print '魔数:%d, 图片数量: %d张, 图片大小: %d*%d' % (magic_number, num_images, num_rows, num_cols)

    # 解析数据集
    image_size = num_rows * num_cols
    offset += struct.calcsize(fmt_header)
    fmt_image = '>' + str(image_size) + 'B'
    images = np.empty((num_images, num_rows, num_cols))
    for i in range(num_images):
        #if (i + 1) % 10000 == 0:
        #    print '已解析 %d' % (i + 1) + '张'
        images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
        offset += struct.calcsize(fmt_image)
    return images

def decode_idx1_ubyte(idx1_ubyte_file):
    """
    解析idx1文件的通用函数
    :param idx1_ubyte_file: idx1文件路径
    :return: 数据集
    """
    # 读取二进制数据
    bin_data = open(idx1_ubyte_file, 'rb').read()

    # 解析文件头信息，依次为魔数和标签数
    offset = 0
    fmt_header = '>ii'
    magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
    #print '魔数:%d, 图片数量: %d张' % (magic_number, num_images)

    # 解析数据集
    offset += struct.calcsize(fmt_header)
    fmt_image = '>B'
    labels = np.empty(num_images)
    for i in range(num_images):
        #if (i + 1) % 10000 == 0:
        #    print '已解析 %d' % (i + 1) + '张'
        labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
        offset += struct.calcsize(fmt_image)
    return labels

def load_train_data_batch(batch_size=100):
    #images = decode_idx3_ubyte('./data/t10k-images-idx3-ubyte')
    #labels = decode_idx1_ubyte('./data/t10k-labels-idx1-ubyte')
    images = decode_idx3_ubyte('./data/train-images-idx3-ubyte')
    labels = decode_idx1_ubyte('./data/train-labels-idx1-ubyte')
    for i in range(0, len(images), batch_size):
        imgs = images[i:i+batch_size]
        lbs = labels[i:i+batch_size]
        yield imgs, lbs

def load_test_data_batch(batch_size=10000):
    images = decode_idx3_ubyte('./data/t10k-images-idx3-ubyte')
    labels = decode_idx1_ubyte('./data/t10k-labels-idx1-ubyte')
    for i in range(0, len(images), batch_size):
        imgs = images[i:i+batch_size]
        lbs = labels[i:i+batch_size]
        yield imgs, lbs

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    #print 'xxx', np.sum(np.exp(x))
    #print 'xxx', np.exp(x)
    #print 'xxx axis=0', np.sum(np.exp(x), axis=0)
    #print 'xxx axis=1', np.sum(np.exp(x), axis=1)
    return np.exp(x-np.max(x, axis=0)) / np.sum(np.exp(x-np.max(x, axis=0)), axis=0)

if __name__ == '__main__':
    pass
