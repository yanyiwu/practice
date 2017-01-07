# Demo

## Introduction

https://github.com/JohnLangford/vowpal_wabbit/wiki/Tutorial

## Examples

```
vw house_dataset -l 10 -c --passes 25 --holdout_off
vw house_dataset -l 10 -c --passes 25 --holdout_off -f house.model

vw house_dataset -p /dev/stdout --quiet

vw -i house.model -t house_dataset -p /dev/stdout --quiet
vw house_dataset --audit --quiet


```
