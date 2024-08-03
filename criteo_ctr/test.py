#!/usr/bin/env python
from datasets import load_dataset
import tensorflow as tf

ds = load_dataset("reczoo/Criteo_x1")

print(ds)

'''
DatasetDict({
    train: Dataset({
        features: ['label', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26'],
        num_rows: 45840617
    })
})
'''

print(ds.keys())

'''
dict_keys(['train'])
'''

train_ds = ds['train']


FEATURE_COLUMNS = [f'I{i}' for i in range(1, 14)] + [f'C{i}' for i in range(1, 27)]
LABEL_COLUMN = 'label'

def preprocess(features):
    for col in [f'C{i}' for i in range(1, 27)]:
        features[col] = tf.strings.to_hash_bucket_fast(features[col], 1000) 
    return features

def to_tf_dataset(dataset):
    def gen():
        for row in dataset:
            features = {key: row[key] for key in FEATURE_COLUMNS}
            label = row[LABEL_COLUMN]
            yield preprocess(features), label
    return tf.data.Dataset.from_generator(gen, output_signature=(
        {key: tf.TensorSpec(shape=(), dtype=tf.string if key.startswith('C') else tf.float32) for key in FEATURE_COLUMNS},
        tf.TensorSpec(shape=(), dtype=tf.int64)
    ))

train_tf_ds = to_tf_dataset(train_ds).batch(1024).prefetch(tf.data.AUTOTUNE)
print(train_tf_ds)


from tensorflow.keras import layers, Model

inputs = {col: layers.Input(name=col, shape=(), dtype=tf.float32 if col.startswith('I') else tf.int32) for col in FEATURE_COLUMNS}

embeddings = []
for col in [f'C{i}' for i in range(1, 27)]:
    embeddings.append(layers.Embedding(input_dim=1000, output_dim=8)(inputs[col]))

numerical_inputs = [inputs[col] for col in [f'I{i}' for i in range(1, 14)]]

x = layers.Concatenate()(numerical_inputs + embeddings)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dense(128, activation='relu')(x)
output = layers.Dense(1, activation='sigmoid')(x)

model = Model(inputs=inputs, outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()
