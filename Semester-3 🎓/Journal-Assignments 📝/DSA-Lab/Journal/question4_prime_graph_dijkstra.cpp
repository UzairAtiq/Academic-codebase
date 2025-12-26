#include <iostream>
#include <vector>
#include <queue>
#include <map>
#include <set>
#include <climits>
#include <algorithm>
using namespace std;

// ===============================================
// TASK 1: Prime Sum Graph Implementation
// ===============================================

class PrimeGraph {
private:
    int N;
    vector<vector<int>> adjList;
    
    // Function to check if a number is prime
    bool isPrime(int num) {
        if (num <= 1) return false;
        if (num == 2) return true;
        if (num % 2 == 0) return false;
        
        for (int i = 3; i * i <= num; i += 2) {
            if (num % i == 0) return false;
        }
        return true;
    }
    
public:
    PrimeGraph(int n) : N(n) {
        adjList.resize(N + 1);  // Index 0 unused, vertices are 1 to N
        buildGraph();
    }
    
    void buildGraph() {
        // For each pair of vertices (i, j), add edge if i + j is prime
        for (int i = 1; i <= N; i++) {
            for (int j = i + 1; j <= N; j++) {
                if (isPrime(i + j)) {
                    // Undirected graph - add edge in both directions
                    adjList[i].push_back(j);
                    adjList[j].push_back(i);
                }
            }
        }
        
        // Sort adjacency lists for consistent output
        for (int i = 1; i <= N; i++) {
            sort(adjList[i].begin(), adjList[i].end());
        }
    }
    
    void displayGraph() {
        cout << "\n===============================================" << endl;
        cout << "   TASK 1: PRIME SUM GRAPH" << endl;
        cout << "===============================================" << endl;
        cout << "\nRule: Edge exists between vertices i and j if (i + j) is prime" << endl;
        cout << "Number of vertices: " << N << " (1 to " << N << ")\n" << endl;
        
        cout << "Adjacency List Representation:" << endl;
        cout << "-------------------------------" << endl;
        
        for (int i = 1; i <= N; i++) {
            cout << "(" << (char)('a' + i - 1) << ") " << i;
            if (!adjList[i].empty()) {
                cout << ", ";
                for (size_t j = 0; j < adjList[i].size(); j++) {
                    cout << adjList[i][j];
                    if (j < adjList[i].size() - 1) cout << ",";
                }
            }
            cout << endl;
        }
        
        cout << "\nEdge Explanation:" << endl;
        for (int i = 1; i <= N; i++) {
            for (int neighbor : adjList[i]) {
                if (i < neighbor) {  // Print each edge only once
                    cout << "  " << i << " -- " << neighbor 
                         << " (sum = " << (i + neighbor) << ", prime)" << endl;
                }
            }
        }
    }
    
    void traverseGraph() {
        cout << "\n\nGraph Traversal (BFS from vertex 1):" << endl;
        cout << "------------------------------------" << endl;
        
        vector<bool> visited(N + 1, false);
        queue<int> q;
        vector<int> traversalOrder;
        
        q.push(1);
        visited[1] = true;
        
        while (!q.empty()) {
            int current = q.front();
            q.pop();
            traversalOrder.push_back(current);
            
            for (int neighbor : adjList[current]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
        
        cout << "BFS Order: ";
        for (size_t i = 0; i < traversalOrder.size(); i++) {
            cout << traversalOrder[i];
            if (i < traversalOrder.size() - 1) cout << " -> ";
        }
        cout << endl;
    }
};

// ===============================================
// TASK 2: Dijkstra's Shortest Path Algorithm
// ===============================================

class DijkstraGraph {
private:
    int numVertices;
    map<int, char> indexToVertex;
    map<char, int> vertexToIndex;
    vector<vector<pair<int, int>>> adjList;  // pair<destination, weight>
    
public:
    DijkstraGraph(int n) : numVertices(n) {
        adjList.resize(n);
    }
    
    void addVertex(char vertex, int index) {
        vertexToIndex[vertex] = index;
        indexToVertex[index] = vertex;
    }
    
    void addEdge(char from, char to, int weight) {
        int fromIdx = vertexToIndex[from];
        int toIdx = vertexToIndex[to];
        adjList[fromIdx].push_back({toIdx, weight});
    }
    
    void dijkstra(char source) {
        int srcIdx = vertexToIndex[source];
        
        // Distance array initialized to infinity
        vector<int> dist(numVertices, INT_MAX);
        vector<int> parent(numVertices, -1);
        vector<bool> visited(numVertices, false);
        
        // Priority queue: pair<distance, vertex>
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        
        dist[srcIdx] = 0;
        pq.push({0, srcIdx});
        
        cout << "\n===============================================" << endl;
        cout << "   TASK 2: DIJKSTRA'S SHORTEST PATH" << endl;
        cout << "===============================================" << endl;
        cout << "\nSource vertex: " << source << "\n" << endl;
        
        cout << "Algorithm Steps:" << endl;
        cout << "----------------" << endl;
        int step = 1;
        
        while (!pq.empty()) {
            int u = pq.top().second;
            int currentDist = pq.top().first;
            pq.pop();
            
            if (visited[u]) continue;
            visited[u] = true;
            
            cout << "Step " << step++ << ": Visit vertex " << indexToVertex[u] 
                 << " (distance: " << currentDist << ")" << endl;
            
            // Update distances to neighbors
            for (auto& edge : adjList[u]) {
                int v = edge.first;
                int weight = edge.second;
                
                if (!visited[v] && dist[u] != INT_MAX && dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    parent[v] = u;
                    pq.push({dist[v], v});
                    
                    cout << "  → Update " << indexToVertex[v] 
                         << ": distance = " << dist[v] << endl;
                }
            }
        }
        
        // Display results
        cout << "\n\nShortest Path Results:" << endl;
        cout << "=======================" << endl;
        cout << "From vertex " << source << " to all other vertices:\n" << endl;
        
        for (int i = 0; i < numVertices; i++) {
            cout << source << " → " << indexToVertex[i] << ": ";
            
            if (dist[i] == INT_MAX) {
                cout << "No path exists" << endl;
            } else {
                cout << "Distance = " << dist[i];
                
                // Reconstruct path
                vector<int> path;
                int current = i;
                while (current != -1) {
                    path.push_back(current);
                    current = parent[current];
                }
                reverse(path.begin(), path.end());
                
                cout << ", Path: ";
                for (size_t j = 0; j < path.size(); j++) {
                    cout << indexToVertex[path[j]];
                    if (j < path.size() - 1) cout << " → ";
                }
                cout << endl;
            }
        }
    }
    
    void displayGraph() {
        cout << "\nDirected Weighted Graph:" << endl;
        cout << "------------------------" << endl;
        
        for (int i = 0; i < numVertices; i++) {
            cout << indexToVertex[i] << " → ";
            if (adjList[i].empty()) {
                cout << "NULL";
            } else {
                for (size_t j = 0; j < adjList[i].size(); j++) {
                    cout << indexToVertex[adjList[i][j].first] 
                         << "(" << adjList[i][j].second << ")";
                    if (j < adjList[i].size() - 1) cout << ", ";
                }
            }
            cout << endl;
        }
    }
};

int main() {
    // ==================== TASK 1 ====================
    cout << "\n\n";
    cout << "###############################################" << endl;
    cout << "#          GRAPH ALGORITHMS TASKS            #" << endl;
    cout << "###############################################" << endl;
    
    // Create prime graph with N = 7
    PrimeGraph pg(7);
    pg.displayGraph();
    pg.traverseGraph();
    
    // ==================== TASK 2 ====================
    cout << "\n\n";
    
    // Create a sample directed weighted graph for Dijkstra's algorithm
    // Using a typical example graph
    DijkstraGraph dg(5);
    
    dg.addVertex('A', 0);
    dg.addVertex('B', 1);
    dg.addVertex('C', 2);
    dg.addVertex('D', 3);
    dg.addVertex('E', 4);
    
    // Add weighted directed edges
    dg.addEdge('A', 'B', 4);
    dg.addEdge('A', 'C', 2);
    dg.addEdge('B', 'C', 1);
    dg.addEdge('B', 'D', 5);
    dg.addEdge('C', 'B', 3);
    dg.addEdge('C', 'D', 8);
    dg.addEdge('C', 'E', 10);
    dg.addEdge('D', 'E', 2);
    
    dg.displayGraph();
    
    // Run Dijkstra's algorithm from vertex A
    dg.dijkstra('A');
    
    cout << "\n\n";
    cout << "===============================================" << endl;
    cout << "          ALGORITHM COMPLEXITY" << endl;
    cout << "===============================================" << endl;
    cout << "\nTask 1 - Prime Graph Construction:" << endl;
    cout << "  Time Complexity: O(N² × √M) where M is max sum" << endl;
    cout << "  Space Complexity: O(N + E)" << endl;
    
    cout << "\nTask 2 - Dijkstra's Algorithm:" << endl;
    cout << "  Time Complexity: O((V + E) log V) with priority queue" << endl;
    cout << "  Space Complexity: O(V)" << endl;
    cout << "  Note: Works only for graphs with non-negative weights" << endl;
    cout << "===============================================\n" << endl;
    
    return 0;
}
