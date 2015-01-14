/*
    Raw TCP packets
    Silver Moon (m00n.silv3r@gmail.com)
*/
#include<stdio.h> //for printf
#include<string.h> //memset
#include<sys/socket.h>    //for socket ofcourse
#include<stdlib.h> //for exit(0);
#include<errno.h> //For errno - the error number
#include<netinet/tcp.h>   //Provides declarations for tcp header
#include<netinet/ip.h>    //Provides declarations for ip header
#include <assert.h>
 
/* 
    96 bit (12 bytes) pseudo header needed for tcp header checksum calculation 
*/
struct pseudo_header
{
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
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
static uint16_t csum2(uint16_t* data, int len) {
  assert(len % 2 == 0);
  const uint16_t* p = data;
  int sum = 0;
  int i;
  for (i = 0; i < len; i+=2) {
    sum += *p++;
  }
  while (sum >> 16) {
    sum = (sum & 0xffff) + (sum >> 16);
  }
  assert(sum <= 0xffff);
  return ~sum;
}
 
int main (int argc, char ** argv)
{
    if(argc < 5) 
    {
        printf("args error.");
        exit(1);
    }
    const char * source_ip = argv[1];
    const int source_port = atoi(argv[2]);
    const char * dest_ip = argv[3];
    const int dest_port = atoi(argv[4]); 

    //Create a raw socket
    int s = socket (PF_INET, SOCK_RAW, IPPROTO_TCP);
     
    if(s == -1)
    {
        //socket creation failed, may be because of non-root privileges
        perror("Failed to create socket");
        exit(1);
    }
     
    //Datagram to represent the packet
    char datagram[4096] , *data , *pseudogram;
     
    //zero out the packet buffer
    memset (datagram, 0, 4096);
     
    //IP header
    struct iphdr *iph = (struct iphdr *) datagram;
     
    //TCP header
    struct tcphdr *tcph = (struct tcphdr *) (datagram + sizeof (struct ip));
    struct sockaddr_in sin;
    struct pseudo_header psh;
     
    //Data part
    data = datagram + sizeof(struct iphdr) + sizeof(struct tcphdr);
    strcpy(data , "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    //strcpy(data , "");
     
    //some address resolution
    sin.sin_family = AF_INET;
    sin.sin_port = htons(dest_port);
    sin.sin_addr.s_addr = inet_addr (dest_ip);
     
    //Fill in the IP Header
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0x00;
    const uint16_t HEADER_LEN = sizeof(struct iphdr) + sizeof(struct tcphdr);
    iph->tot_len = htons(HEADER_LEN + strlen(data));
    iph->id = htonl (54321); //Id of this packet
    iph->frag_off = 0;
    iph->ttl = 255;
    iph->protocol = IPPROTO_TCP;
    iph->check = 0;      //Set to 0 before calculating checksum
    iph->check = csum ((unsigned short *) datagram, sizeof(struct iphdr)-8);
    iph->saddr = inet_addr ( source_ip );    //Spoof the source ip address
    iph->daddr = sin.sin_addr.s_addr;

     
    //Ip checksum
    //iph->check = csum ((unsigned short *) datagram, ntohs(iph->tot_len));
    printf("%x\n", iph->check);
     
    //TCP Header
    tcph->source = htons (source_port);
    //tcph->dest = htons (80);
    tcph->dest = htons (dest_port);
    tcph->seq = 0;
    tcph->ack_seq = 0;
    tcph->doff = 5;  //tcp header size
    tcph->fin=0;
    tcph->syn=1;
    tcph->rst=0;
    tcph->psh=0;
    tcph->ack=0;
    tcph->urg=0;
    tcph->window = htons (5840); /* maximum allowed window size */
    tcph->check = 0; //leave checksum 0 now, filled later by pseudo header
    tcph->urg_ptr = 0;
     
    //Now the TCP checksum
    psh.source_address = inet_addr( source_ip );
    psh.dest_address = sin.sin_addr.s_addr;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(data) );
     
    int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr) + strlen(data);
    pseudogram = malloc(psize);
     
    memcpy(pseudogram , (char*) &psh , sizeof (struct pseudo_header));
    memcpy(pseudogram + sizeof(struct pseudo_header) , tcph , sizeof(struct tcphdr) + strlen(data));
     
    tcph->check = csum( (unsigned short*) pseudogram , psize);
     
    //IP_HDRINCL to tell the kernel that headers are included in the packet
    int one = 1;
    const int *val = &one;
     
    if (setsockopt (s, IPPROTO_IP, IP_HDRINCL, val, sizeof (one)) < 0)
    {
        perror("Error setting IP_HDRINCL");
        exit(0);
    }
     
    //loop if you want to flood :)
    while (1)
    {
        //Send the packet
        if (sendto (s, datagram, ntohs(iph->tot_len) ,  0, (struct sockaddr *) &sin, sizeof (sin)) < 0)
        {
            perror("sendto failed");
        }
        //Data send successfully
        else
        {
            printf ("Packet Send. Length : %d \n" , ntohs(iph->tot_len));
        }
        printf("press any key to continue:");
        getchar();
    }
     
    return 0;
}
