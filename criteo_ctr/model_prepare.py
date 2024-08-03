import tensorflow as tf
from tensorflow.keras import layers, Model

from data_prepare import FEATURE_COLUMNS, LABEL_COLUMN

def get_model():
    inputs = {col: layers.Input(name=col, shape=(), dtype=tf.float32 if col.startswith('I') else tf.int32) for col in FEATURE_COLUMNS}

    embeddings = []
    for col in [f'C{i}' for i in range(1, 27)]:
        embeddings.append(layers.Embedding(input_dim=1000, output_dim=8)(inputs[col]))

    numerical_inputs = [layers.Reshape((1,))(inputs[col]) for col in [f'I{i}' for i in range(1, 14)]]

    # 合并所有特征
    x = layers.Concatenate()(numerical_inputs + embeddings)
    #x = layers.Dense(256, activation='relu')(x)
    #x = layers.Dense(128, activation='relu')(x)
    output = layers.Dense(1, activation='sigmoid')(x)

    model = Model(inputs=inputs, outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

if __name__ == '__main__':
    model = get_model()
    model.summary()
