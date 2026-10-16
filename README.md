# Library Management System (LMS) - ASE Lab

A modular, extensible Library Management System developed as part of the Advanced Software Engineering (ASE) Lab. This repository showcases Git Flow branching models, feature development, integration merging, and merge conflict resolution.

---

## 📌 Features

- **Book Catalog Management**: Add books, track quantities, and update available copies.
- **Member Directory**: Register members, enforce borrowing limits.
- **Lending & Returns**: Issue loans with tracking of due dates and automatic inventory updates.
- **Fine Calculation Engine**: Overdue calculation based on loan duration and daily fine rates.
- **Automated Test Suite**: Full `unittest` test coverage.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git

### Running the Demo
```bash
python3 library.py
```

### Running Unit Tests
```bash
python3 -m unittest test_library.py -v
```

---

## 🌿 Git Branching Strategy & Workflow

This project follows a professional Git branching workflow:

1. **`main`**: Production-ready, stable releases.
2. **`develop`**: Central integration branch for ongoing features.
3. **`feature/*`**: Isolated branches for specific enhancements (e.g. `feature/book-search`).
4. **Merge Conflict Simulation & Resolution**: Systematic resolution of competing changes during feature integration.
