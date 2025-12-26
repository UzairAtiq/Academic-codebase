# 📚 Library Management System

> *A console-based library management system built with C++ implementing core Data Structures*

---

## 📋 About

A comprehensive library management system that demonstrates fundamental data structures and algorithms including **Arrays**, **Linked Lists**, **Queues**, and **Merge Sort**. The system allows librarians to manage books, track borrowing history, and organize the library collection efficiently.

## ✨ Features

- ➕ **Add Books** - Add new books to the library collection
- ❌ **Delete Books** - Remove books from inventory
- 📋 **Display Library** - View all books with beautiful formatting
- 🔄 **Sort by Year** - Organize books chronologically using Merge Sort
- 🔍 **Search Books** - Find books by ID instantly
- 📤 **Borrow System** - Queue-based borrowing with FIFO processing
- 📜 **Borrow History** - Track all borrowing transactions using linked lists

## 🛠️ Technologies & Data Structures

| Component | Data Structure |
|-----------|----------------|
| **Book Storage** | Dynamic Array (Array ADT) |
| **Borrow Queue** | Queue (Linked List implementation) |
| **History Tracking** | Singly Linked List |
| **Sorting Algorithm** | Merge Sort (O(n log n)) |

## 🚀 How to Run

### Prerequisites
- **C++ Compiler** (g++, clang++, or MSVC)
- **Terminal/Command Prompt**

### Compilation & Execution

**Using g++:**
```bash
# Compile
g++ -o library main.cpp

# Run
./library
```

**Using clang++:**
```bash
# Compile
clang++ -o library main.cpp

# Run
./library
```

**On Windows (MSVC):**
```bash
# Compile
cl /EHsc main.cpp

# Run
main.exe
```

## 📖 Usage Guide

### Main Menu Options

```
📚 LIBRARY MANAGEMENT SYSTEM 📚

📖 Book Management:
   1. ➕ Add Book
   2. ❌ Delete Book
   3. 📋 Display All Books
   4. 🔄 Sort Books by Year
   5. 🔍 Search Book by ID

📚 Borrowing:
   6. 📤 Borrow Book
   7. 📜 View Borrow History

   0. 🚪 Exit
```

### Example Workflow

1. **Add Books** - Populate your library with books
2. **Display Books** - View the collection
3. **Sort by Year** - Organize chronologically
4. **Search** - Find specific books quickly
5. **Borrow** - Process borrowing requests
6. **View History** - Track all transactions

## 💡 Key Algorithms

### Merge Sort Implementation
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Use Case**: Sorting books by publication year

### Search Algorithm
- **Type**: Linear Search
- **Time Complexity**: O(n)
- **Use Case**: Finding books by ID

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│      Library Management System          │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐  ┌────────────────┐  │
│  │  BookArray  │  │  BorrowQueue   │  │
│  │  (Dynamic)  │  │  (Queue ADT)   │  │
│  └─────────────┘  └────────────────┘  │
│         │                  │           │
│         └──────┬───────────┘           │
│                │                       │
│         ┌──────▼────────┐             │
│         │ BorrowHistory │             │
│         │ (Linked List) │             │
│         └───────────────┘             │
└─────────────────────────────────────────┘
```

## 🎯 Learning Outcomes

This project demonstrates:
- ✅ Implementation of custom Array ADT
- ✅ Queue implementation using linked lists
- ✅ Singly linked list for history tracking
- ✅ Merge Sort algorithm for efficient sorting
- ✅ Memory management with dynamic allocation
- ✅ Object-oriented programming in C++

---

**Course:** Data Structures & Algorithms (DSA)  
**Semester:** 3  
*Part of the academic curriculum*
