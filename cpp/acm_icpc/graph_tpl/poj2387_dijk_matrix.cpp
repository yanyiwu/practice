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
const int N=1005, M=4005;

int mat[N][N];

int s, t;
int dis[N];
bool visit[N];
int n, m;


int dijkstra()
{
    for(int i = 0; i <= n; i++)
    {
        dis[i] = inf;
    }
    CLEAN(visit);
    int now = s;
    dis[now] = 0;
    visit[now] = true;
    for(int i = 0;  i < n; i++)
    {
        int mn = inf;
        int min_v = 0;
        for(int j = 1; j <= n; j++)
        {
            if(!visit[j])
            {
                if(mat[now][j] != inf && dis[j] > dis[now] + mat[now][j])
                {
                    dis[j] = dis[now] + mat[now][j];
                }
                if(dis[j] < mn)
                {
                    mn = dis[j];
                    min_v = j;
                }
            }
        }
        if(mn == inf)
        {
            break;
        }
        now = min_v;
        visit[now] = true;
        if(now == t)
        {
            break;
        }
    }
    return dis[t];
}

void solve()
{
    printf("%d\n", dijkstra());
}

int main()
{
    freopen("data/poj2387.in", "r", stdin);
    scanf("%d%d",&m,&n);
    for(int i = 1; i <= n; i++)
    {
        for(int j = 1; j <= n; j++)
        {
            mat[i][j] = inf;
        }
    }
    int u, v, w;
    for(int i = 0; i < m; i++)
    {
        scanf("%d%d%d",&u,&v,&w);
        mat[u][v] = Min(mat[u][v], w);
        mat[v][u] = mat[u][v];
    }
    s = 1;
    t = n;
    solve();
    return 0;
}

