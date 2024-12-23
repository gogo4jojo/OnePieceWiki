# One Piece Database (CMPSC 431w)
Group: repent-for-your-sin-tax [Ramy Mohammed, Josiah Kutai]

## Project Overview

Our One Piece Database project is a comprehensive application designed to manage, analyze, and explore the vast world of the One Piece anime and manga series and also showcase what we learned in CMPSC 431W. It provides an organized database system for handling characters, Devil Fruits, pirate crews, marine officers, and more, with features to insert, update, delete, and query data. This was built using pgAdmin with PostgreSQL for handling our database operations, Python for scripting, and Kivy for the GUI.

We intended this project to simulate the role of a high-ranking World Government officer tasked with managing sensitive information about the One Piece world. From tracking pirates and marines to recording Devil Fruits and legendary swords, the application ensures data integrity and allows for detailed analytical reports. It also features transactional operations with rollback capabilities for critical data management tasks.

---

## File Descriptions

### 1. `app.py`
This is the main application script. It provides a Kivy GUI with various tabs for inserting, updating, deleting, and analyzing data. Users can interact with the database through intuitive forms and dropdown menus.

- **Key Features:**
  - Tabs for each database entity (e.g., Person, Devil Fruit, Pirate).
  - Update and report generation tools.
  - Sorting and navigation through large datasets.

### 2. `build tables.txt`
This file contains the necessary SQL commands to create the database schema. It defines tables for entities like `Person`, `Devil_Fruit`, `Pirate`, and `Marine`, along with their relationships.

- **Key Features:**
  - Defines the necessary tables and their relationships to each other.
  - Primary and foreign keys to enforce data integrity.
  - Constraints to maintain valid and consistent data.

### 3. `conn.py`
Handles the database connection using the `psycopg2` library. It sets up the connection parameters and manages transaction settings.

- **Key Features:**
  - Reusable function for establishing database connections.
  - Ensures `autocommit` is enabled to avoid transaction lock issues.

### 4. `df.py`
Manages interactions with the `Devil_Fruit` table. It provides a GUI for generating reports about Devil Fruits, including their type, awakening status, and known users.

- **Key Features:**
  - Generates detailed Devil Fruit reports.
  - Displays associated users and their abilities.

### 5. `list.txt`
Contains pre-defined lists for dropdown options, including pirate positions, marine ranks, sword types, and world regions.

- **Key Features:**
  - Ensures consistent data entry.
  - Simplifies UI development by standardizing choices.

### 6. `person_table.py`
Implements a GUI for interacting with the `Person` table. Users can view, update, and paginate through character data, with sorting options for columns.

- **Key Features:**
  - Provides an interactive table view.
  - Supports efficient navigation and updates.

### 7. `report.py`
Generates detailed reports about characters, including their associations with Devil Fruits, groups, swords, and more. 

- **Key Features:**
  - Combines data from multiple tables for comprehensive insights.
  - Displays results with a user-friendly GUI.

### 8. `UserManual.pdf`
A comprehensive guide to the application, covering its features, usage, and technical details to showcase functionality.

- **Key Features:**
   - Provides an in-depth overview of the application's capabilities.

### 9. `TeamReport.pdf`
A final report on the team's performance, including our progress, challenges, and achievements.

## How It Works

1. **Database Setup:** The schema is initialized using `build tables.txt` to create tables and relationships in PostgreSQL.
2. **User Interface:** Users interact with the application via the Kivy GUI in `app.py`.
3. **Data Management:** The application supports inserting, updating, and deleting data across multiple entities like `Person`, `Devil_Fruit`, and `Marine`.
4. **Analytical Reporting:** Users can generate reports on characters, Devil Fruits, and pirate crews, including visual elements like images.
5. **Transactions:** Critical operations involve multi-step transactions with rollback capabilities to ensure data integrity.

## Acknowledgments

We cite our sources in the code files where necessary.
Eiichiro Oda; for creating One Piece.

---

Enjoy exploring the One Piece universe with this database!