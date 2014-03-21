
#include<iostream>
#include<fstream>
#include<map>
#include<vector>
#include<string>
#include<memory.h>
#include<cmath>
#include<algorithm>
#include<queue>
#define Min(a,b) ((a)<(b)?(a):(b))
#define Max(a,b) ((a)>(b)?(a):(b))
#define Abs(a) ((a)>0?(a):-(a))
#define llong long long int
#define CLEAN(x) (memset(x, 0, sizeof(x)))
using namespace std;
const int inf = 0x7fffffff;
const int N=1005, M=40005;

int s, t;
int n, m;

int visit[N];
int dis[N];

struct Edge
{
    int v,next,w;
}edge[M];
int edgehead[N];
int edgen;

void addedge(int u,int v,int w)
{
    edge[edgen].v = v;
    edge[edgen].w = w;
    edge[edgen].next = edgehead[u];
    edgehead[u] = edgen++;
}

int spfa()
{
    for(int i =0; i<=n;i++)
    {
        dis[i] =inf;
    }
    queue<int> que;
    dis[s] = 0;
    visit[s] = true;
    que.push(s);
    while(!que.empty())
    {
        int now = que.front();
        que.pop();
        visit[now] = false;
        for(int j = edgehead[now]; j ; j = edge[j].next)
        {
            int v = edge[j].v;
            int w = edge[j].w;
            if(dis[v] > dis[now] + w)
            {
                dis[v]=dis[now]+w;
                if(!visit[v])
                {
                    visit[v] =true;
                    que.push(v);
                }
            }
        }
    }
    return dis[t];
    
}

void solve()
{
    printf("%d\n",spfa());
}

int main()
{
#ifdef WYY_DEBUG
    freopen("data/poj2387.in", "r", stdin);
#endif
    scanf("%d%d",&m,&n);
    edgen = 1;
    int u, v, w;
    for(int i = 0; i < m; i++)
    {
        scanf("%d%d%d",&u,&v,&w);
        addedge(u,v,w);
        addedge(v,u,w);
    }
    s = 1;
    t = n;
    solve();
    return 0;
}

