#!/usr/bin/env python

from data_prepare import prepare_criteo_ctr_ds
from model_prepare import get_model


def run(total_num_rows=100*1000):
    train_tf_ds, test_tf_ds = prepare_criteo_ctr_ds(total_num_rows=total_num_rows)

    model = get_model()

    res = model.fit(
        train_tf_ds, 
        epochs=2, 
        validation_data=test_tf_ds)
    print(res.history)

if __name__ == '__main__':
    run(10*1000)
    run(100*1000)
    run(1000*1000)
