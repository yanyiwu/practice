# seaweedfs 之 volumeSizeLimitMB 参数实验验证

## 猜想

当某次上传的文件过大，导致 volume 的大小超过 volumeSizeLimitMB 之后，会发生什么事情？
猜想： 该次上传成功，同时 volume 会被 master 标记为不可写状态。以防该 volume 会被继续写入。

## 实验步骤

1. 启动 master `./master.sh` ，设置 volumeSizeLimitMB 参数为 1，也就是每个 volume 最大值为 1 MB。
2. 启动 volume `./volume1.sh`
3. 拷贝任意大于 1MB 的文件，比如 `cp $GOPATH/bin/weed .`
4. 上传文件，`curl -F "file=@./weed" "http://127.0.0.1:10333/submit"`，返回成功，比如 `{"fid":"5,013bba0010","fileName":"weed","fileUrl":"localhost:9090/5,013bba0010","size":14383312}` ，注意虽然该文件超过 1MB ，但是是上传成功。
5. 查看 vol1 下面的数据大小，如下
```
4.0K    vol1/1.dat
0       vol1/1.idx
4.0K    vol1/2.dat
0       vol1/2.idx
4.0K    vol1/3.dat
0       vol1/3.idx
4.0K    vol1/4.dat
0       vol1/4.idx
14M     vol1/5.dat
4.0K    vol1/5.idx
4.0K    vol1/6.dat
0       vol1/6.idx
4.0K    vol1/7.dat
0       vol1/7.idx
```
6. 所以其实是上传成功，同时发现 master 的日志里面可以看到 `I0923 19:01:33 29339 volume_layout.go:158] Volume 5 becomes unwritable` ，也就是此时 volume 5 已经为不可写的。


## 结论

1. 验证出猜想正确。
2. 每个 volume 的大小其实是会大于 volumeSizeLimitMB，比如如上实验中，虽然 volumeSizeLimitMB 是1MB，但是上传的文件达到了14M也是上传成功的。
