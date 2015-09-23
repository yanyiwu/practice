test -d ./vol1 || mkdir ./vol1
weed -v=5 volume -dir=./vol1 -mserver="localhost:10333" -ip="localhost" -port=9090
