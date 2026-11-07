# 🔍 CampusFind – Smart Lost & Found System

**CampusFind** is a Python-based command-line application designed to help students report, search, and recover lost items within a college campus.

The system allows users to report lost and found items, search existing reports, and automatically identify possible matches using a similarity-based matching algorithm.

## 🚀 Features

- **Report Lost Items:** Submit details about items you have lost.
- **Report Found Items:** Register items found anywhere on campus.
- **View All Reports:** Display all reported lost and found items.
- **Search Reports:** Search open reports using keywords such as item name, category, description, or location.
- **Smart Matching System:** Automatically compares lost items with found items and calculates a matching percentage.
- **Find Matches by ID:** Retrieve possible matches using a previously generated lost-item report ID.
- **Mark Items as Returned:** Update the status of recovered items.
- **Data Persistence:** Stores reports in a text file so that data remains available after restarting the application.

## 🧠 Smart Matching Algorithm

CampusFind uses Python's `SequenceMatcher` from the `difflib` library to calculate text similarity between lost and found items.

The matching score is calculated using four parameters:

| Parameter | Weight |
|---|---:|
| Category Similarity | 35% |
| Item Name Similarity | 30% |
| Description Similarity | 25% |
| Location Similarity | 10% |

**Matching Formula:**

```text
Score = (0.35 × Category Similarity)
      + (0.30 × Name Similarity)
      + (0.25 × Description Similarity)
      + (0.10 × Location Similarity)
```

- Items with a matching score of **35% or above** are considered possible matches.
- Results are sorted in descending order of matching score.
- The system displays the top 5 possible matches.

This helps users identify potentially matching items without manually checking every report.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Libraries:**
  - `os` – File handling and existence checking.
  - `csv` – Reading and writing report data.
  - `datetime` – Handling report dates.
  - `difflib` – Text similarity and matching.

No external Python packages are required.

## 📂 Project Structure

```text
CampusFind/
│
├── main.py              # Main application
├── campus_items.txt     # Stores lost and found reports
└── README.md            # Project documentation
```

`campus_items.txt` is created automatically when the first report is saved.

## ⚙️ Installation & Execution

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CampusFind.git
```

### 2. Navigate to the Project Directory

```bash
cd CampusFind
```

### 3. Run the Application

Make sure Python 3 is installed.

```bash
python main.py
```

## 📋 Application Menu

After running the application, you will see the following menu:

```text
==================================================
       CAMPUSFIND - SMART LOST & FOUND
==================================================

1. Report a LOST item
2. Report a FOUND item
3. View all reports
4. Search open reports
5. Find possible matches for a lost report
6. Mark an item as returned
7. Exit
```

Select an option from 1 to 7 to perform the desired operation.

## 💡 How It Works

1. A student reports a lost or found item by entering its name, category, description, location, date, and contact details.
2. The application generates a unique report ID.
3. All reports are stored in `campus_items.txt`.
4. When a lost item is reported, the system automatically compares it with existing open found-item reports.
5. The similarity algorithm calculates matching percentages.
6. Possible matches are displayed, helping students recover their belongings.
7. Once an item is recovered, its status can be updated to `RETURNED`.

## 🔮 Future Improvements

- Develop a graphical user interface (GUI).
- Build a web-based platform for campus-wide access.
- Integrate a database such as MySQL or SQLite.
- Add user authentication and student verification.
- Implement image-based item matching.
- Introduce email or notification alerts when a possible match is found.

## 👨‍💻 Author

**Anshuman Kumar Upadhyay**

Computer Science & Engineering Student  
National Institute of Technology (NIT) Manipur

---

⭐ If you find this project useful, consider giving the repository a star!
