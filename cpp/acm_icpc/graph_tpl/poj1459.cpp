#include<iostream>
#include<fstream>
#include<map>
#include<vector>
#include<string>
#include<memory.h>
#include<cmath>
#include<algorithm>
#include<queue>
#define Min(a,b) (a<b?a:b)
#define Max(a,b) (a>b?a:b)
#define Abs(a) (a>0?(a):-(a))
#define llong long long int
#define CLEAN(x) (memset(x, 0, sizeof(x)))
using namespace std;
const int inf = 0x7fffffff;
const int N=55,M=2505;

struct Edge
{
    int v;
    int w;
    int next;
    int re;
}edge[M];
int edgehead[N];

int source, sink;
int edgenum;

bool visit[N];
int que[N];
int level[N];

void addedge(int u, int v, int w)
{
    edge[edgenum].v = v;
    edge[edgenum].w = w;
    edge[edgenum].next = edgehead[u];
    edge[edgenum].re = edgenum + 1;
    edgehead[u] = edgenum;
    edgenum ++;
    
    edge[edgenum].v = u;
    edge[edgenum].w = 0;
    edge[edgenum].next = edgehead[v];
    edge[edgenum].re = edgenum - 1;
    edgenum ++;
}

void init()
{
    edgenum = 1;
    CLEAN(edge);
    CLEAN(edgehead);
}

bool bfs()
{
    CLEAN(visit);
    CLEAN(level);
    int head = 1, tail = 1;
    que[tail ++] = source;
    visit[source] = true;
    level[source] = 0;
    while(head < tail)
    {
        int now = que[head++];
        if(now == sink)
        {
            return true;
        }
        for(int i = edgehead[now]; i; i = edge[i].next)
        {
            int v = edge[i].v;
            if(!visit[v] && edge[i].w > 0)
            {
                que[tail++] = v;
                visit[v] = true;
                level[v] = level[now] + 1;

            }
        }
    }
    return false;
}

int dinic(int now, int sum)
{
    if(now == sink)
    {
        return sum;
    }
    int os = sum;
    for(int i = edgehead[now]; i; i = edge[i].next)
    {
        int v = edge[i].v;
        if(level[v] == level[now] + 1 && edge[i].w > 0)
        {
            int ret = dinic(v, Min(sum, edge[i].w));
            edge[i].w -= ret;
            edge[edge[i].re].w += ret;
            sum -= ret;
        }
    }
    return os - sum;
}

void solve()
{
    int sum = 0;
    while(bfs())
    {
        sum += dinic(source, inf);
    }
    printf("%d\n", sum);
}

int main()
{
    
    freopen("data/poj1459.in", "r", stdin);
    int n, s_n, t_n , k, tmp;
    while(scanf("%d%d%d%d", &n, &s_n, &t_n, &k)!=EOF)
    {
        init();
        int u, v, w;
        for(int i = 0; i < k ; i++)
        {
            scanf(" (%d,%d)%d", &u, &v, &w);
            addedge(u, v, w);
        }
        source = n;
        sink = n+1;
        for(int i = 0; i < s_n ; i++)
        {
            scanf(" (%d)%d", &v, &w);
            addedge(source, v, w);
        }
        for(int i = 0; i < t_n ; i++)
        {
            scanf(" (%d)%d", &v, &w);
            addedge(v, sink, w);
        }
        solve();
    }
    return 0;
}

