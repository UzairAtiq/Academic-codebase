#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
using namespace std;

// Question 2: Depth-First Search (DFS) and Breadth-First Search (BFS) Traversal

class GraphTraversal {
private:
    int numVertices;
    map<char, int> vertexIndex;
    map<int, char> indexVertex;
    vector<pair<char, int>> adjList[5];  // Adjacency list
    
public:
    GraphTraversal() {
        numVertices = 5;
        
        // Map vertices to indices
        vertexIndex['A'] = 0;
        vertexIndex['B'] = 1;
        vertexIndex['C'] = 2;
        vertexIndex['D'] = 3;
        vertexIndex['E'] = 4;
        
        indexVertex[0] = 'A';
        indexVertex[1] = 'B';
        indexVertex[2] = 'C';
        indexVertex[3] = 'D';
        indexVertex[4] = 'E';
        
        // Build adjacency list from the graph
        addEdge('A', 'B', 5);
        addEdge('A', 'D', 10);
        addEdge('A', 'E', 6);
        addEdge('B', 'D', 3);
        addEdge('D', 'D', 0);  // Self-loop
        addEdge('D', 'C', 4);
        addEdge('E', 'C', 4);
    }
    
    void addEdge(char from, char to, int weight) {
        int fromIndex = vertexIndex[from];
        adjList[fromIndex].push_back({to, weight});
    }
    
    // Depth-First Search (DFS) using recursion
    void DFSUtil(int vertex, vector<bool>& visited, vector<char>& traversal) {
        visited[vertex] = true;
        traversal.push_back(indexVertex[vertex]);
        
        // Visit all adjacent vertices
        for (auto& neighbor : adjList[vertex]) {
            char neighborVertex = neighbor.first;
            int neighborIndex = vertexIndex[neighborVertex];
            
            if (!visited[neighborIndex]) {
                DFSUtil(neighborIndex, visited, traversal);
            }
        }
    }
    
    void DFS(char startVertex) {
        cout << "\n=== DEPTH-FIRST SEARCH (DFS) ===" << endl;
        cout << "Starting from vertex: " << startVertex << "\n" << endl;
        
        vector<bool> visited(numVertices, false);
        vector<char> traversal;
        
        int startIndex = vertexIndex[startVertex];
        DFSUtil(startIndex, visited, traversal);
        
        // Print DFS traversal
        cout << "DFS Traversal Order: ";
        for (size_t i = 0; i < traversal.size(); i++) {
            cout << traversal[i];
            if (i < traversal.size() - 1) {
                cout << " -> ";
            }
        }
        cout << endl;
        
        // Explanation
        cout << "\nExplanation:" << endl;
        cout << "- Start at A, mark it as visited" << endl;
        cout << "- Visit A's first unvisited neighbor (B)" << endl;
        cout << "- From B, visit its first unvisited neighbor (D)" << endl;
        cout << "- From D, visit its first unvisited neighbor (C)" << endl;
        cout << "- Backtrack to A and visit next unvisited neighbor (E)" << endl;
        cout << "- All vertices visited, DFS complete" << endl;
    }
    
    // Breadth-First Search (BFS) using queue
    void BFS(char startVertex) {
        cout << "\n=== BREADTH-FIRST SEARCH (BFS) ===" << endl;
        cout << "Starting from vertex: " << startVertex << "\n" << endl;
        
        vector<bool> visited(numVertices, false);
        vector<char> traversal;
        queue<int> q;
        
        int startIndex = vertexIndex[startVertex];
        visited[startIndex] = true;
        q.push(startIndex);
        traversal.push_back(indexVertex[startIndex]);
        
        while (!q.empty()) {
            int current = q.front();
            q.pop();
            
            // Visit all adjacent vertices
            for (auto& neighbor : adjList[current]) {
                char neighborVertex = neighbor.first;
                int neighborIndex = vertexIndex[neighborVertex];
                
                if (!visited[neighborIndex]) {
                    visited[neighborIndex] = true;
                    q.push(neighborIndex);
                    traversal.push_back(neighborVertex);
                }
            }
        }
        
        // Print BFS traversal
        cout << "BFS Traversal Order: ";
        for (size_t i = 0; i < traversal.size(); i++) {
            cout << traversal[i];
            if (i < traversal.size() - 1) {
                cout << " -> ";
            }
        }
        cout << endl;
        
        // Explanation
        cout << "\nExplanation:" << endl;
        cout << "- Start at A, add it to queue and mark as visited" << endl;
        cout << "- Dequeue A, add all its neighbors (B, D, E) to queue" << endl;
        cout << "- Dequeue B, add its unvisited neighbor (none, D already visited)" << endl;
        cout << "- Dequeue D, add its unvisited neighbor (C) to queue" << endl;
        cout << "- Dequeue E, all its neighbors already visited" << endl;
        cout << "- Dequeue C, no neighbors to add" << endl;
        cout << "- Queue empty, BFS complete" << endl;
    }
    
    void displayGraphInfo() {
        cout << "\n===============================================" << endl;
        cout << "        GRAPH TRAVERSAL ALGORITHMS" << endl;
        cout << "===============================================" << endl;
        cout << "\nGraph Structure:" << endl;
        cout << "  Vertices: A, B, C, D, E" << endl;
        cout << "  Edges: A→B(5), A→D(10), A→E(6), B→D(3)," << endl;
        cout << "         D→D(0), D→C(4), E→C(4)" << endl;
    }
};

int main() {
    GraphTraversal g;
    
    g.displayGraphInfo();
    
    // Perform DFS starting from vertex A
    g.DFS('A');
    
    // Perform BFS starting from vertex A
    g.BFS('A');
    
    cout << "\n===============================================" << endl;
    cout << "\nKey Differences:" << endl;
    cout << "- DFS: Goes deep into the graph before backtracking" << endl;
    cout << "       Uses recursion (or stack) - explores one path fully" << endl;
    cout << "- BFS: Explores level by level, visiting all neighbors first" << endl;
    cout << "       Uses queue - explores neighbors before going deeper" << endl;
    cout << "===============================================" << endl;
    
    return 0;
}
