all:
	wget https://github.com/yanyiwu/limonp/archive/v0.5.0.tar.gz
	tar zxvf v0.5.0.tar.gz
	g++ -o demo -I./limonp-0.5.0/include thread_pool_demo.cpp -lpthread 
	./demo
clean:
	rm -rf *.gz demo limonp-v0.5.0
