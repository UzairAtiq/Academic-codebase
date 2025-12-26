#include <iostream>
#include <vector>
#include <map>
using namespace std;

// Question 1: Graph Representation using Adjacency Matrix and Adjacency List

class Graph {
private:
    int numVertices;
    map<char, int> vertexIndex;  // Map vertex names to indices
    map<int, char> indexVertex;  // Map indices to vertex names
    
public:
    Graph() {
        numVertices = 5;
        // Map vertices A, B, C, D, E to indices 0, 1, 2, 3, 4
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
    }
    
    // Adjacency Matrix Representation
    void displayAdjacencyMatrix() {
        cout << "\n=== ADJACENCY MATRIX ===" << endl;
        cout << "Rows represent source vertices, columns represent destination vertices" << endl;
        cout << "Values represent edge weights (0 means no edge)\n" << endl;
        
        // Initialize matrix with 0s
        int adjMatrix[5][5] = {0};
        
        // Fill the matrix based on the graph edges
        // A → B (weight 5)
        adjMatrix[vertexIndex['A']][vertexIndex['B']] = 5;
        // A → D (weight 10)
        adjMatrix[vertexIndex['A']][vertexIndex['D']] = 10;
        // A → E (weight 6)
        adjMatrix[vertexIndex['A']][vertexIndex['E']] = 6;
        // B → D (weight 3)
        adjMatrix[vertexIndex['B']][vertexIndex['D']] = 3;
        // D → D (weight 0, self-loop)
        adjMatrix[vertexIndex['D']][vertexIndex['D']] = 0;
        // D → C (weight 4)
        adjMatrix[vertexIndex['D']][vertexIndex['C']] = 4;
        // E → C (weight 4)
        adjMatrix[vertexIndex['E']][vertexIndex['C']] = 4;
        
        // Display matrix with headers
        cout << "     ";
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i] << "   ";
        }
        cout << endl;
        cout << "   ----------------" << endl;
        
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i] << " | ";
            for (int j = 0; j < numVertices; j++) {
                cout << adjMatrix[i][j] << "   ";
            }
            cout << endl;
        }
    }
    
    // Adjacency List Representation
    void displayAdjacencyList() {
        cout << "\n=== ADJACENCY LIST ===" << endl;
        cout << "Each vertex shows its adjacent vertices with edge weights\n" << endl;
        
        // Create adjacency list using vector of pairs (destination, weight)
        vector<pair<char, int>> adjList[5];
        
        // Add edges to adjacency list
        // A → B (5), A → D (10), A → E (6)
        adjList[vertexIndex['A']].push_back({'B', 5});
        adjList[vertexIndex['A']].push_back({'D', 10});
        adjList[vertexIndex['A']].push_back({'E', 6});
        
        // B → D (3)
        adjList[vertexIndex['B']].push_back({'D', 3});
        
        // D → D (0), D → C (4)
        adjList[vertexIndex['D']].push_back({'D', 0});
        adjList[vertexIndex['D']].push_back({'C', 4});
        
        // E → C (4)
        adjList[vertexIndex['E']].push_back({'C', 4});
        
        // Display adjacency list
        for (int i = 0; i < numVertices; i++) {
            cout << indexVertex[i] << " -> ";
            if (adjList[i].empty()) {
                cout << "NULL";
            } else {
                for (size_t j = 0; j < adjList[i].size(); j++) {
                    cout << adjList[i][j].first << "(" << adjList[i][j].second << ")";
                    if (j < adjList[i].size() - 1) {
                        cout << " -> ";
                    }
                }
            }
            cout << endl;
        }
    }
    
    void displayGraphInfo() {
        cout << "\n===============================================" << endl;
        cout << "        GRAPH REPRESENTATION" << endl;
        cout << "===============================================" << endl;
        cout << "\nGraph Edges (from the diagram):" << endl;
        cout << "  A → B (weight: 5)" << endl;
        cout << "  A → D (weight: 10)" << endl;
        cout << "  A → E (weight: 6)" << endl;
        cout << "  B → D (weight: 3)" << endl;
        cout << "  D → D (weight: 0, self-loop)" << endl;
        cout << "  D → C (weight: 4)" << endl;
        cout << "  E → C (weight: 4)" << endl;
    }
};

int main() {
    Graph g;
    
    g.displayGraphInfo();
    g.displayAdjacencyMatrix();
    g.displayAdjacencyList();
    
    cout << "\n===============================================" << endl;
    
    return 0;
}
