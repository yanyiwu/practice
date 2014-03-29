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
const int N=105,M=40005;

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
    queue<int> que;
    que.push(source);
    visit[source] = true;
    level[source] = 1;
    while(!que.empty())
    {
        int now = que.front();
        que.pop();
        if(now == sink)
        {
            return true;
        }
        for(int i = edgehead[now]; i ; i = edge[i].next)
        {
            int v = edge[i].v;
            int w = edge[i].w;
            if(w && !visit[v])
            {
                level[v] = level[now] +1;
                que.push(v);
                visit[v] = true;
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
    for(int i = edgehead[now]; i ; i = edge[i].next)
    {
        int v = edge[i].v;
        int w = edge[i].w;
        if(w && level[now] + 1== level[v])
        {
            int ret = dinic(v, Min(w, sum));
            sum -= ret;
            edge[i].w -= ret;
            edge[edge[i].re].w += ret;
        }
    }
    return os - sum;
}

void solve()
{
    int sum =0;
    while(bfs())
    {
        sum+= dinic(source, inf);
    }
    printf("%d\n", sum);
}

int main()
{
    
#ifdef WYY_DEBUG
    freopen("data/poj1459.in", "r", stdin);
#endif
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

