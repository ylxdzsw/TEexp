// Max-Flow of Undirected Graphs

#include "stdc++.h"
using namespace std;

const int N = 3003;
typedef int T;
struct Edge {
    int u, v;
    T cap, flow;
    Edge(int u, int v, T c, T f) : u(u), v(v), cap(c), flow(f) {}
};

struct Dinic {
    int n, m, s, t;
    const T oo = 1e9;
    vector<Edge> edge;
    vector<int> G[N];
    bool vis[N];
    int d[N];
    int cur[N];
    vector<vector<int>> paths;
    
    void init(int n) {
        this->n = n;
        for (int i = 0; i <= n; i++)
            G[i].clear();
        edge.clear();
    }
    
    void addEdge(int u, int v, int cap) {
        edge.push_back(Edge(u, v, cap, 0));
        edge.push_back(Edge(v, u, cap, 0));
        m = (int)edge.size();
        G[u].push_back(m - 2);
        G[v].push_back(m - 1);
    }
    
    bool bfs() {
        memset(vis, 0, sizeof vis);
        queue<int> q;
        q.push(s);
        d[s] = 0;
        vis[s] = 1;
        while (!q.empty()) {
            int x = q.front();
            q.pop();
            for (int i = 0; i < G[x].size(); i++) {
                Edge &e = edge[G[x][i]];
                if (!vis[e.v] && e.cap > e.flow) {
                    vis[e.v] = true;
                    d[e.v] = d[x] + 1;
                    q.push(e.v);
                }
            }
        }
        return vis[t];
    }
    
    T dfs(int x, T a) {
        if (x == t || a == 0)
            return a;
        T flow = 0, f = 0;
        for (int &i = cur[x]; i < G[x].size(); i++) {
            Edge &e = edge[G[x][i]];
            if (d[x] + 1 == d[e.v] && (f = dfs(e.v, min(a, e.cap - e.flow))) > 0) {
                e.flow += f;
                edge[G[x][i] ^ 1].flow -= f;
                flow += f;
                a -= f;
                if (a == 0)
                    break;
            }
        }
        return flow;
    }
    
    bool find_path()
    {
        vector<int> p;
    
        for (int x=s; x != t && cur[x] < G[x].size(); )
        {
            for(int &i = cur[x]; i < G[x].size(); )
            {
                Edge &e = edge[G[x][i++]];
                if(e.flow == 1)
                {
                    p.push_back(x=e.v);
                    break;
                }
            }
        }
        if(p.empty())
            return false;

        paths.push_back(p);
        return true;
    }
    

    
    T dinitz(int s, int t) {
        this->s = s;
        this->t = t;
        int flow = 0;
        while (bfs()) {
            memset(cur, 0, sizeof cur);
            flow += dfs(s, oo);
        }
        
        paths.clear();
        memset(cur, 0, sizeof cur);
        while(find_path());
        
        return flow;
    }
    
};

extern "C" {
    // #include <stdio.h>
    
    void* init(int n) {
        auto mf = new Dinic;
        // fprintf( stderr, "init %d\n", n);
        mf->init(n);
        return mf;
    }
    
    void addEdge(Dinic* mf, int u, int v) {
        // fprintf( stderr, "addedge %d %d\n", u, v);
        mf->addEdge(u, v, 1);
    }
    
    int dinitz(Dinic* mf, int s, int t) {
        // fprintf( stderr, "dinitz %d %d\n", s, t);
        return mf->dinitz(s, t);
    }
    
    int npath(Dinic* mf) {
        return mf->paths.size();
    }
    
    int path_len(Dinic* mf, int path_id) {
        // fprintf( stderr, "pathlen %d \n", path_id);
        return mf->paths[path_id - 1].size();
    }
    
    void get_path(Dinic* mf, int path_id, int* buf) {
        // fprintf( stderr, "get_path %d \n", path_id);
        auto path = &(mf->paths)[path_id - 1];
        for(int i = 0; i < path->size(); i++)
            buf[i] = (*path)[i];
    }
    
    void del(Dinic* mf) {
        delete mf;
    }
}

int main() {
    // freopen("in.txt", "r", stdin);
    Dinic MaxFlow;
    int n, m; // nodes, edges
    scanf("%d %d", &n, &m);
        
    MaxFlow.init(n);
    for (int i = 0; i < m; i++) {
        int u, v; // node, node
        scanf("%d %d", &u, &v);
        MaxFlow.addEdge(u, v, 1);
    }

    for (int s = 1; s <= n; s++)
    for (int t = 1; t <= n; t++) {
        if (s == t)
            continue;
            
        printf("The max-flow is %d.\n", MaxFlow.dinitz(s, t));

        for(int i = 0; i<MaxFlow.paths.size();i++)
        {
            printf("Path %d: %d", i+1, s);
            for(int j =0;j<MaxFlow.paths[i].size();j++)
            {
                printf(" -> %d", MaxFlow.paths[i][j]);
            }
            printf("\n");
        }
    }

    return 0;
}
