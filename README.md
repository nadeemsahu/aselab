# Library Management System (LMS) - ASE Lab

A modular, extensible Library Management System developed as part of the Advanced Software Engineering (ASE) Lab. This repository showcases Git Flow branching models, feature development, integration merging, and merge conflict resolution.

---

## 📌 Features

- **Book Catalog Management**: Add books, track quantities, and update available copies.
- **Member Directory**: Register members, enforce borrowing limits.
- **Lending & Returns**: Issue loans with tracking of due dates and automatic inventory updates.
- **Search Engine**: Search catalog by book title, author, or genre (introduced via `feature/book-search`).
- **Tiered Lending Policies**: Standard 3-week loans and Express 1-week loans with differentiated overdue fine rates (harmonized via conflict resolution).
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

## 🌿 Git Branching Strategy & Workflow Demonstrated

This repository illustrates industry-standard Git workflow practices required in modern software engineering:

```text
*   b928f99 (HEAD -> main, origin/main, origin/develop, develop) fix(merge): resolve loan policy conflict
|\  
| * cc3c600 (origin/feature/express-loan, feature/express-loan) feat(policy): configure express lending
* | c341753 refactor(policy): set standard member policy
|/  
*   0a4caa2 Merge branch 'feature/book-search' into develop
|\  
| * 89fab5e (origin/feature/book-search, feature/book-search) feat(search): implement search_books
|/  
* e3899b6 feat: implement base library management system with tests and documentation
* 35885b2 first commit
```

### 1. Branches Established
- **`main`**: Production release branch tracking stable versions.
- **`develop`**: Primary integration branch where completed features converge.
- **`feature/book-search`**: Isolated feature branch used to build and unit-test the search subsystem.
- **`feature/express-loan`**: Secondary feature branch used to establish express loan terms, leading to a merge conflict with `develop`.

### 2. Feature Development & Merge into `develop`
- Feature branch `feature/book-search` was created from `develop`.
- Implemented `search_books()` in `library.py` along with unit tests in `test_library.py`.
- Merged cleanly into `develop` with `--no-ff`.

### 3. Merge Conflict Creation & Resolution
- **Competing Edit 1 (`develop`)**: Updated loan policies for standard members (21-day loan, $0.50 fine, 5 books max).
- **Competing Edit 2 (`feature/express-loan`)**: Updated the same lines for express lending (7-day loan, $2.50 fine, 2 books max).
- **Trigger**: Attempting `git merge feature/express-loan` into `develop` produced:
  ```text
  Auto-merging library.py
  CONFLICT (content): Merge conflict in library.py
  Automatic merge failed; fix conflicts and then commit the result.
  ```
- **Resolution**:
  - Inspected `<<<<<<< HEAD`, `=======`, and `>>>>>>>` markers.
  - Synthesized both requirements into a unified `LOAN_POLICIES` tiered configuration supporting both `standard` and `express` tiers.
  - Staged with `git add library.py` and committed resolution.
  - Successfully merged into `main` and pushed all branches to remote origin.
