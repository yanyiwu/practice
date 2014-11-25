all:
	g++ -o server server.cpp -L/usr/local/lib -levent 
	g++ -o server2 server2.cpp -L/usr/local/lib -levent 
	g++ -o EventServer EventServer.cpp -L/usr/local/lib -levent 
	g++ -o HttpClient HttpClient.cpp -L/usr/local/lib -levent
HttpClient2: HttpClient2.cpp
	g++ -o HttpClient2 HttpClient2.cpp -L/usr/local/lib -levent
server3: server3.cpp
	g++ -o $@ server3.cpp -L/usr/local/lib -levent
	
