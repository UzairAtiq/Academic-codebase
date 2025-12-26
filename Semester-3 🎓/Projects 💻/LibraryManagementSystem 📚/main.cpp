#include <iostream>
#include <string>
using namespace std;

/* ================= BOOK STRUCT ================= */
struct Book {
    int id;
    string title;
    string author;
    int year;
};

/* ================= ARRAY ADT ================= */
class BookArray {
private:
    Book* arr;
    int size;
    int capacity;

public:
    BookArray(int cap = 50) {
        capacity = cap;
        size = 0;
        arr = new Book[capacity];
    }

    int getSize() { return size; }

    Book& get(int i) { return arr[i]; }

    void addBook(Book b) {
        if (size < capacity) {
            arr[size++] = b;
            cout << "\n✓ Book added successfully!\n";
        }
        else {
            cout << "\n✗ Library full!\n";
        }
    }

    void deleteBook(int id) {
        for (int i = 0; i < size; i++) {
            if (arr[i].id == id) {
                for (int j = i; j < size - 1; j++)
                    arr[j] = arr[j + 1];
                size--;
                cout << "\n✓ Book deleted successfully!\n";
                return;
            }
        }
        cout << "\n✗ Book not found!\n";
    }

    int searchBook(int id) {
        for (int i = 0; i < size; i++)
            if (arr[i].id == id)
                return i;
        return -1;
    }

    void displayBooks() {
        if (size == 0) {
            cout << "\n📚 No books available.\n";
            return;
        }
        cout << "\n" << string(70, '=') << endl;
        cout << "                      📚 LIBRARY COLLECTION\n";
        cout << string(70, '=') << endl;
        for (int i = 0; i < size; i++) {
            cout << "\n📖 Book #" << (i + 1) << "\n";
            cout << "   ID:     " << arr[i].id << endl;
            cout << "   Title:  " << arr[i].title << endl;
            cout << "   Author: " << arr[i].author << endl;
            cout << "   Year:   " << arr[i].year << endl;
            cout << "   " << string(50, '-') << endl;
        }
    }
};

/* ================= MERGE SORT ================= */
void merge(Book arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    Book* L = new Book[n1];
    Book* R = new Book[n2];

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;

    while (i < n1 && j < n2) {
        if (L[i].year <= R[j].year)
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    delete[] L;
    delete[] R;
}

void mergeSort(Book arr[], int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

/* ================= QUEUE (BORROW) ================= */
struct QueueNode {
    int bookID;
    QueueNode* next;
};

class BorrowQueue {
private:
    QueueNode* front;
    QueueNode* rear;

public:
    BorrowQueue() {
        front = rear = NULL;
    }

    void borrowBook(int id) {
        QueueNode* node = new QueueNode{ id, NULL };
        if (!rear)
            front = rear = node;
        else {
            rear->next = node;
            rear = node;
        }
        cout << "\n✓ Borrow request added to queue.\n";
    }

    int processBorrow() {
        if (!front) return -1;
        int id = front->bookID;
        QueueNode* temp = front;
        front = front->next;
        delete temp;
        return id;
    }
};

/* ================= LINKED LIST (HISTORY) ================= */
struct HistoryNode {
    int userID;
    int bookID;
    HistoryNode* next;
};

class BorrowHistory {
private:
    HistoryNode* head;

public:
    BorrowHistory() {
        head = NULL;
    }

    void addHistory(int user, int book) {
        HistoryNode* node = new HistoryNode{ user, book, head };
        head = node;
    }

    void displayHistory() {
        if (!head) {
            cout << "\n📜 No borrowing history.\n";
            return;
        }
        cout << "\n" << string(70, '=') << endl;
        cout << "                   📜 BORROWING HISTORY\n";
        cout << string(70, '=') << endl;
        HistoryNode* temp = head;
        int count = 1;
        while (temp) {
            cout << count++ << ". 👤 User " << temp->userID
                << " borrowed 📖 Book ID " << temp->bookID << endl;
            temp = temp->next;
        }
        cout << string(70, '=') << endl;
    }
};

/* ================= MAIN MENU ================= */
int main() {
    BookArray library;
    BorrowQueue queue;
    BorrowHistory history;

    int choice;

    do {
        cout << "\n" << string(50, '=') << endl;
        cout << "     📚 LIBRARY MANAGEMENT SYSTEM 📚\n";
        cout << string(50, '=') << endl;
        cout << "\n  📖 Book Management:\n";
        cout << "     1. ➕ Add Book\n";
        cout << "     2. ❌ Delete Book\n";
        cout << "     3. 📋 Display All Books\n";
        cout << "     4. 🔄 Sort Books by Year\n";
        cout << "     5. 🔍 Search Book by ID\n";
        cout << "\n  📚 Borrowing:\n";
        cout << "     6. 📤 Borrow Book\n";
        cout << "     7. 📜 View Borrow History\n";
        cout << "\n     0. 🚪 Exit\n";
        cout << string(50, '=') << endl;
        cout << "\n➤ Enter your choice: ";
        cin >> choice;

        if (choice == 1) {
            Book b;
            cout << "\n➕ ADD NEW BOOK\n";
            cout << string(30, '-') << endl;
            cout << "Enter Book ID: "; cin >> b.id;
            cin.ignore();
            cout << "Enter Title: "; getline(cin, b.title);
            cout << "Enter Author: "; getline(cin, b.author);
            cout << "Enter Year: "; cin >> b.year;
            library.addBook(b);
        }
        else if (choice == 2) {
            int id;
            cout << "\n❌ DELETE BOOK\n";
            cout << string(30, '-') << endl;
            cout << "Enter Book ID to delete: ";
            cin >> id;
            library.deleteBook(id);
        }
        else if (choice == 3) {
            library.displayBooks();
        }
        else if (choice == 4) {
            if (library.getSize() > 0) {
                mergeSort(&library.get(0), 0, library.getSize() - 1);
                cout << "\n✓ Books sorted by year successfully!\n";
            } else {
                cout << "\n✗ No books to sort!\n";
            }
        }
        else if (choice == 5) {
            int id;
            cout << "\n🔍 SEARCH BOOK\n";
            cout << string(30, '-') << endl;
            cout << "Enter Book ID to search: ";
            cin >> id;
            int index = library.searchBook(id);
            if (index != -1) {
                cout << "\n✓ Book Found!\n";
                cout << "   Title:  " << library.get(index).title << endl;
                cout << "   Author: " << library.get(index).author << endl;
                cout << "   Year:   " << library.get(index).year << endl;
            }
            else
                cout << "\n✗ Book not found.\n";
        }
        else if (choice == 6) {
            int bookID, userID;
            cout << "\n📤 BORROW BOOK\n";
            cout << string(30, '-') << endl;
            cout << "Enter User ID: ";
            cin >> userID;
            cout << "Enter Book ID: ";
            cin >> bookID;

            queue.borrowBook(bookID);
            int processed = queue.processBorrow();
            history.addHistory(userID, processed);
            cout << "✓ Book borrowed successfully!\n";
        }
        else if (choice == 7) {
            history.displayHistory();
        }

    } while (choice != 0);

    cout << "\n" << string(50, '=') << endl;
    cout << "     👋 Thank you for using the system!\n";
    cout << "     🚪 Exiting...\n";
    cout << string(50, '=') << endl;
    return 0;
}