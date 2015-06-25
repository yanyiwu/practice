test -d volume_dir || mkdir volume_dir
weed volume -port=8080 -dir=./volume_dir -mserver=127.0.0.1:9333
