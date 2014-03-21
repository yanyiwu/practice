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
const int N=1005, M=4005;

int s, t;
int n, m;

int visit[N];
int dis[N];
int mat[N][N];

int spfa()
{
    for(int i = 0; i <= n;i++)
    {
        dis[i] = inf;
    }

    queue<int> que;
    que.push(s);
    visit[s] = true;
    dis[s] = 0;
    while(!que.empty())
    {
        int now = que.front();
        que.pop();
        visit[now] = false;
        for(int i =1; i<= n ;i++)
        {
            if(mat[now][i] != inf && dis[i] > dis[now] + mat[now][i])
            {
                dis[i] = dis[now] + mat[now][i];
                if(!visit[i])
                {
                    que.push(i);
                    visit[i] = true;
                }
            }
        }
    }
    return dis[t];
}

void solve()
{
    printf("%d\n", spfa());
}

int main()
{
#ifdef WYY_DEBUG
    freopen("data/poj2387.in", "r", stdin);
#endif
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

