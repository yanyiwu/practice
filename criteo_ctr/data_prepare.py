import tensorflow as tf
from datasets import load_dataset
ds = load_dataset("reczoo/Criteo_x1")
ds = ds['train'].train_test_split(test_size=0.05)
print(ds)

FEATURE_COLUMNS = [f'I{i}' for i in range(1, 14)] + [f'C{i}' for i in range(1, 27)]
print(FEATURE_COLUMNS)
LABEL_COLUMN = 'label'

def to_tf_dataset(dataset):
    def preprocess(features):
        for col in [f'C{i}' for i in range(1, 27)]:
            features[col] = tf.strings.to_hash_bucket_fast(tf.strings.as_string(features[col]), 1000)
        for col in [f'I{i}' for i in range(1, 14)]:
            features[col] = tf.cast(features[col], tf.float32)
        return features

    def gen():
        for row in dataset:
            features = {key: row[key] for key in FEATURE_COLUMNS}
            label = row[LABEL_COLUMN]
            yield preprocess(features), label

    output_signature = (
        {key: tf.TensorSpec(shape=(), dtype=tf.int32 if key.startswith('C') else tf.float32) for key in FEATURE_COLUMNS},
        tf.TensorSpec(shape=(), dtype=tf.int64),
    )
    return tf.data.Dataset.from_generator(gen, output_signature=output_signature)

train_tf_ds = to_tf_dataset(ds['train']).batch(1024).prefetch(tf.data.AUTOTUNE)
test_tf_ds = to_tf_dataset(ds['test']).batch(1024).prefetch(tf.data.AUTOTUNE)

