#!/usr/bin/env python

from data_prepare import train_tf_ds, test_tf_ds
from model_prepare import get_model

model = get_model()
model.summary()

# 训练模型
res = model.fit(
    train_tf_ds.take(10), 
    epochs=2, 
    validation_data=test_tf_ds.take(10))
print(res.history)
