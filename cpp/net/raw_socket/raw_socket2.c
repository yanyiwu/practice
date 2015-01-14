#include<stdio.h> //for printf
#include<string.h> //memset
#include<sys/socket.h>    //for socket ofcourse
#include<stdlib.h> //for exit(0);
#include<errno.h> //For errno - the error number
#include<netinet/tcp.h>   //Provides declarations for tcp header
#include<netinet/ip.h>    //Provides declarations for ip header

//#include <netinet/in.h>
//#include <arpa/inet.h>

/* 
    96 bit (12 bytes) pseudo header needed for tcp header checksum calculation 
*/
struct pseudo_header
{
    uint32_t source_address;
    uint32_t dest_address;
    uint8_t placeholder;
    uint8_t protocol;
    uint16_t tcp_length;
};

/*
    Generic checksum calculation function
*/
unsigned short csum(unsigned short *ptr,int nbytes) 
{
    register long sum;
    unsigned short oddbyte;
    register short answer;
 
    sum=0;
    while(nbytes>1) {
        sum+=*ptr++;
        nbytes-=2;
    }
    if(nbytes==1) {
        oddbyte=0;
        *((u_char*)&oddbyte)=*(u_char*)ptr;
        sum+=oddbyte;
    }
 
    sum = (sum>>16)+(sum & 0xffff);
    sum = sum + (sum>>16);
    answer=(short)~sum;
     
    return(answer);
}

unsigned short tcpcsum(uint32_t source_ip, uint32_t dest_ip) {
    struct pseudo_header psh;
    psh.source_address = source_ip;
    psh.dest_address = dest_ip;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr));
    
    int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr);
    pseudogram = malloc(psize);
}

int main(int argc, char ** argv) {
  if(argc < 5) {
    printf("args error.");
    exit(1);
  }
  const char * source_ip = argv[1];
  const uint16_t source_port = atoi(argv[2]);
  const char * dest_ip = argv[3];
  const uint16_t dest_port = atoi(argv[4]); 

  int s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);

  if(s == -1) {
    perror("failed to create socket");
    exit(1);
  }

  char datagram[4096];
  
  memset(datagram, 0, sizeof(datagram));

  struct iphdr *iph = (struct iphdr *) datagram;
  
  struct tcphdr *tcph =(struct tcphdr *) (datagram + sizeof(struct ip));
  struct sockaddr_in sin;

  sin.sin_family = AF_INET;
  sin.sin_port = htons(dest_port);
  sin.sin_addr.s_addr = inet_addr(dest_ip);

  iph->ihl = sizeof(struct iphdr) / 4; // 5
  iph->version = IPVERSION; // 4
  iph->tos = 0x04;
  iph->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr); // 40

  iph->id = htonl(54321);

  iph->frag_off = 0;
  iph->ttl = 255;
  iph->protocol = IPPROTO_TCP;
  iph->check = 0; 

  //iph->check = csum((unsigned short *)datagram, sizeof(struct iphdr) - 8);
  iph->saddr = inet_addr(source_ip);
  iph->daddr = sin.sin_addr.s_addr;
  
  iph->check = csum ((unsigned short *) datagram, iph->tot_len);

  printf("iph->check %x\n", iph->check); // f195

  //TCP Header
  tcph->source = htons(source_port);
  tcph->dest = htons(dest_port);

  tcph->seq = 0;
  tcph->ack_seq = 0;

  tcph->doff = sizeof(struct tcphdr) / 4; // 5
  tcph->fin=0;
  tcph->syn=1;
  tcph->rst=0;
  tcph->psh=0;
  tcph->ack=0;
  tcph->urg=0;

  tcph->window = htons(5840);
  tcph->check = 0; //TODO
  tcph->urg_ptr = 0;

  //check TODO

  

  int one = 1;
  if(setsockopt(s, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
    perror("Error setting IP_HDRINCL");
    exit(1);
  }
  
  if(sendto(s, datagram, iph->tot_len, 0, (struct sockaddr *)&sin, sizeof(sin) < 0)) {
    perror("sendto failed");
  } 

  return 0;
}
