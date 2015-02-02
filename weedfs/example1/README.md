
```
./master.sh
./volume1.sh
./volume2.sh
./volume3.sh
```

```
./test1.sh > log
./check1.sh < log
ok.
```

```
ls vol1 vol2 vol3
vol1:
1.dat 1.idx 2.dat 2.idx 3.dat 3.idx 5.dat 5.idx

vol2:
2.dat 2.idx 3.dat 3.idx 4.dat 4.idx 6.dat 6.idx

vol3:
1.dat 1.idx 4.dat 4.idx 5.dat 5.idx 6.dat 6.idx
```

```
ls vol1 vol2 vol3
vol1:
1.dat 1.idx 2.dat 2.idx 3.dat 3.idx 4.dat 4.idx 5.dat 5.idx 6.dat 6.idx

vol2:
1.dat 1.idx 2.dat 2.idx 3.dat 3.idx 4.dat 4.idx 5.dat 5.idx 6.dat 6.idx

vol3:

```


log

```
localhost:8081/1,03c616736731
localhost:8082/3,03c7c94d54fc
localhost:8081/5,03c85548e9df
localhost:8082/6,03c9e8b580ab
localhost:8082/3,03cabdadf310
localhost:8082/4,03cb904d6fc0
localhost:8081/1,03ccf3a9ff45
localhost:8081/5,03cd9c8f4fce
```


```
./check1.sh < log
ok.
```

