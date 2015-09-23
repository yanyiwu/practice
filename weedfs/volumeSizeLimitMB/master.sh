test -d ./mdata || mkdir ./mdata
weed master -mdir="./mdata" -volumeSizeLimitMB=1 -defaultReplication="000" -ip="localhost" -port=10333
