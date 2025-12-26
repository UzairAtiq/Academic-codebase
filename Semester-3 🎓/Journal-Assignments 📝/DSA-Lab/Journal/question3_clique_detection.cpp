#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
using namespace std;

// Question: Clique Detection in a Graph
// A clique is a subset of vertices where every pair of vertices is adjacent

class Graph {
private:
    int numVertices;
    map<char, int> vertexIndex;
    map<int, char> indexVertex;
    vector<vector<int>> adjMatrix;  // Adjacency matrix for easier clique checking
    set<pair<int, int>> edges;  // Store edges for reference
    
public:
    Graph(int n) {
        numVertices = n;
        adjMatrix.resize(n, vector<int>(n, 0));
    }
    
    void addVertex(char vertex, int index) {
        vertexIndex[vertex] = index;
        indexVertex[index] = vertex;
    }
    
    void addEdge(char from, char to) {
        int fromIdx = vertexIndex[from];
        int toIdx = vertexIndex[to];
        
        // Undirected graph - add edge in both directions
        adjMatrix[fromIdx][toIdx] = 1;
        adjMatrix[toIdx][fromIdx] = 1;
        
        // Store edge for display
        if (fromIdx < toIdx) {
            edges.insert({fromIdx, toIdx});
        } else {
            edges.insert({toIdx, fromIdx});
        }
    }
    
    // Function to check if given list of nodes forms a clique
    bool is_clique(vector<char> list_nodes) {
        // A clique requires at least 1 node
        if (list_nodes.empty()) {
            return false;
        }
        
        // Single node is trivially a clique
        if (list_nodes.size() == 1) {
            return true;
        }
        
        // Check if all nodes exist in the graph
        for (char node : list_nodes) {
            if (vertexIndex.find(node) == vertexIndex.end()) {
                cout << "Error: Node '" << node << "' does not exist in graph!" << endl;
                return false;
            }
        }
        
        // Check if every pair of nodes is adjacent
        for (size_t i = 0; i < list_nodes.size(); i++) {
            for (size_t j = i + 1; j < list_nodes.size(); j++) {
                int idx1 = vertexIndex[list_nodes[i]];
                int idx2 = vertexIndex[list_nodes[j]];
                
                // If any pair is not connected, it's not a clique
                if (adjMatrix[idx1][idx2] == 0) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    // Helper function to display clique check results
    void checkAndDisplayClique(vector<char> nodes) {
        cout << "Checking if {";
        for (size_t i = 0; i < nodes.size(); i++) {
            cout << nodes[i];
            if (i < nodes.size() - 1) cout << ", ";
        }
        cout << "} is a clique: ";
        
        bool result = is_clique(nodes);
        cout << (result ? "TRUE ✓" : "FALSE ✗") << endl;
        
        if (result && nodes.size() > 1) {
            cout << "  → All " << (nodes.size() * (nodes.size() - 1)) / 2 
                 << " pairs are adjacent" << endl;
        } else if (!result && nodes.size() > 1) {
            cout << "  → Not all pairs are adjacent (missing edges)" << endl;
        }
    }
    
    void displayGraph() {
        cout << "\n===============================================" << endl;
        cout << "           CLIQUE DETECTION" << endl;
        cout << "===============================================" << endl;
        cout << "\nGraph from the diagram:" << endl;
        cout << "Vertices: ";
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i];
            if (i < numVertices - 1) cout << ", ";
        }
        cout << "\n\nEdges (undirected):" << endl;
        
        for (const auto& edge : edges) {
            cout << "  " << indexVertex[edge.first] << " -- " 
                 << indexVertex[edge.second] << endl;
        }
    }
    
    void displayAdjacencyMatrix() {
        cout << "\nAdjacency Matrix:" << endl;
        cout << "   ";
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i] << " ";
        }
        cout << endl;
        cout << "  ";
        for (int i = 0; i < numVertices; i++) {
            cout << "--";
        }
        cout << endl;
        
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i] << "| ";
            for (int j = 0; j < numVertices; j++) {
                cout << adjMatrix[i][j] << " ";
            }
            cout << endl;
        }
    }
};

int main() {
    // Create graph based on the diagram (6 vertices: a, b, c, d, e, f)
    Graph g(6);
    
    // Add vertices
    g.addVertex('a', 0);
    g.addVertex('b', 1);
    g.addVertex('c', 2);
    g.addVertex('d', 3);
    g.addVertex('e', 4);
    g.addVertex('f', 5);
    
    // Add edges from the diagram
    // The highlighted clique region shows: a, b, c, d are all connected
    g.addEdge('a', 'b');
    g.addEdge('a', 'c');
    g.addEdge('a', 'd');
    g.addEdge('b', 'c');
    g.addEdge('b', 'd');
    g.addEdge('c', 'd');
    
    // Connections to e and f (outside the clique)
    g.addEdge('c', 'e');
    g.addEdge('e', 'f');
    g.addEdge('d', 'f');
    
    // Display graph information
    g.displayGraph();
    g.displayAdjacencyMatrix();
    
    // Test the is_clique function
    cout << "\n===============================================" << endl;
    cout << "           CLIQUE TESTING" << endl;
    cout << "===============================================\n" << endl;
    
    // Test 1: The actual clique from the diagram (highlighted region)
    cout << "Test 1: Highlighted clique from diagram" << endl;
    g.checkAndDisplayClique({'a', 'b', 'c', 'd'});
    
    cout << "\nTest 2: Subset of the clique" << endl;
    g.checkAndDisplayClique({'a', 'b', 'c'});
    
    cout << "\nTest 3: Another subset" << endl;
    g.checkAndDisplayClique({'b', 'd'});
    
    cout << "\nTest 4: Not a clique (includes node outside clique)" << endl;
    g.checkAndDisplayClique({'a', 'b', 'e'});
    
    cout << "\nTest 5: Not a clique (e and f are connected but not all pairs)" << endl;
    g.checkAndDisplayClique({'c', 'e', 'f'});
    
    cout << "\nTest 6: Single node (trivially a clique)" << endl;
    g.checkAndDisplayClique({'a'});
    
    cout << "\nTest 7: Two connected nodes" << endl;
    g.checkAndDisplayClique({'e', 'f'});
    
    cout << "\nTest 8: All nodes (not a clique)" << endl;
    g.checkAndDisplayClique({'a', 'b', 'c', 'd', 'e', 'f'});
    
    cout << "\n===============================================" << endl;
    cout << "\nDefinition:" << endl;
    cout << "A CLIQUE is a subset of vertices where EVERY" << endl;
    cout << "pair of distinct vertices is adjacent (connected)." << endl;
    cout << "\nIn this graph, {a, b, c, d} forms a 4-clique" << endl;
    cout << "because all 6 pairs are connected:" << endl;
    cout << "  (a,b), (a,c), (a,d), (b,c), (b,d), (c,d)" << endl;
    cout << "===============================================" << endl;
    
    return 0;
}
