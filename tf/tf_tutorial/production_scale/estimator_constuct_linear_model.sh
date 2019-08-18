#!/bin/bash

#git clone --depth 1 https://github.com/tensorflow/models
cd models
python -m official.wide_deep.census_main --help
python -m official.wide_deep.census_main --model_type=wide --train_epochs=2
ls /tmp/census_data/
