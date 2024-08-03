#!/usr/bin/env python

from datasets import load_dataset
import tensorflow as tf
from tensorflow.keras import layers, Model

# 加载Criteo数据集
ds = load_dataset("reczoo/Criteo_x1")

ds = ds['train'].train_test_split(test_size=0.05)
print(ds)

FEATURE_COLUMNS = [f'I{i}' for i in range(1, 14)] + [f'C{i}' for i in range(1, 27)]
LABEL_COLUMN = 'label'

def preprocess(features):
    for col in [f'C{i}' for i in range(1, 27)]:
        features[col] = tf.strings.to_hash_bucket_fast(tf.strings.as_string(features[col]), 1000)
    for col in [f'I{i}' for i in range(1, 14)]:
        features[col] = tf.cast(features[col], tf.float32)
    return features

def to_tf_dataset(dataset):
    def gen():
        for row in dataset:
            features = {key: row[key] for key in FEATURE_COLUMNS}
            label = row[LABEL_COLUMN]
            yield preprocess(features), label
    return tf.data.Dataset.from_generator(gen, output_signature=(
        {key: tf.TensorSpec(shape=(), dtype=tf.int32 if key.startswith('C') else tf.float32) for key in FEATURE_COLUMNS},
        tf.TensorSpec(shape=(), dtype=tf.int64)
    ))

train_tf_ds = to_tf_dataset(ds['train']).batch(1024).prefetch(tf.data.AUTOTUNE)
test_tf_ds = to_tf_dataset(ds['test']).batch(1024).prefetch(tf.data.AUTOTUNE)

# 定义输入层
inputs = {col: layers.Input(name=col, shape=(), dtype=tf.float32 if col.startswith('I') else tf.int32) for col in FEATURE_COLUMNS}

# 嵌入层
embeddings = []
for col in [f'C{i}' for i in range(1, 27)]:
    embeddings.append(layers.Embedding(input_dim=1000, output_dim=8)(inputs[col]))

# 数值特征
numerical_inputs = [layers.Reshape((1,))(inputs[col]) for col in [f'I{i}' for i in range(1, 14)]]

# 合并所有特征
x = layers.Concatenate()(numerical_inputs + embeddings)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dense(128, activation='relu')(x)
output = layers.Dense(1, activation='sigmoid')(x)

model = Model(inputs=inputs, outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

# 训练模型
res = model.fit(train_tf_ds.take(100), epochs=2, validation_data=test_tf_ds.take(10))
print(res.history)
