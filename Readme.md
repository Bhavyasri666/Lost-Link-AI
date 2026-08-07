# LostLink AI

## Overview

LostLink AI is a graph-powered Lost and Found application built using **Python Flask** and **CognoDB**. The application allows users to report lost and found items and automatically identifies potential matches by traversing relationships in a graph database.

---

# Use Case

People frequently lose valuable belongings such as mobile phones, laptops, wallets, jewellery, bags, ID cards, and documents. Traditional databases store this information in separate tables, making relationship-based searches complex.

LostLink AI models users, items, brands, categories, locations, and matches as connected nodes, making it easy to discover possible matches through graph traversal.

---

# Why a Graph Database?

This application is relationship-driven. Every lost item is connected to its owner, category, brand, and location, while found items are connected in a similar way.

A graph database enables efficient traversal of these relationships and simplifies queries such as:

* Which user reported this lost item?
* Which found item matches the lost item?
* Where was the item lost or found?
* Which category and brand does the item belong to?

These queries are more naturally represented in a graph than in a relational database.

---

# Technology Stack

**Frontend**

* HTML
* CSS

**Backend**

* Python
* Flask

**Database**

* CognoDB Cloud

**Driver**

* Neo4j Python Driver

---

# Graph Data Model

```text
Person
   │
   ├── REPORTED_LOST ─────► LostItem
   │                          │
   │                          ├── BELONGS_TO ─► Category
   │                          ├── HAS_BRAND ─► Brand
   │                          ├── LAST_SEEN_AT ─► Location
   │                          └── POSSIBLE_MATCH ─► FoundItem
   │
   └── REPORTED_FOUND ────► FoundItem
                              │
                              ├── BELONGS_TO ─► Category
                              ├── HAS_BRAND ─► Brand
                              └── FOUND_AT ─► Location
```

---

# Features

* Report Lost Items
* Report Found Items
* AI-Based Matching
* Graph Relationship Traversal
* Search Lost and Found Items
* Match Confidence Score
* User-Friendly Interface

---

# Project Structure

```text
LostLink/
│
├── app.py
├── database.py
├── seed.py
├── requirements.txt
├── README.md
│
├── templates/
│
├── static/
│
└── screenshots/
```

---

# Setting Up CognoDB

1. Create a free account on CognoDB Cloud.
2. Create a free database instance.
3. Copy the Bolt connection URI and password.
4. Create a `.env` file in the project root.

Example:

```text
NEO4J_URI=bolt+s://your-instance.databases.cognodb.com
NEO4J_USERNAME=cognodb
NEO4J_PASSWORD=your_password
```

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
cd LostLink
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Running the Application

Load the sample graph data.

```bash
python seed.py
```

Start the Flask application.

```bash
python app.py
```

Open the application in your browser.

```text
http://127.0.0.1:5000
```

---

# Main Cypher Queries

### View the complete graph

```cypher
MATCH(n)-[r]->(m)
RETURN n,r,m
LIMIT 100;
```

This query displays all nodes and relationships stored in the graph.

### View AI Matches

```cypher
MATCH(l:LostItem)-[r:POSSIBLE_MATCH]->(f:FoundItem)
RETURN l,r,f;
```

This query retrieves all AI-generated matches between lost and found items.

### Count Total Nodes

```cypher
MATCH(n)
RETURN count(n);
```

This query returns the total number of nodes in the database.

---

# Screenshots

#Demo Video : https://drive.google.com/file/d/18Xx3k56mMtiHiH0X19JczKZuWHYsenwd/view?usp=drivesdk 

# Conclusion

LostLink AI demonstrates how a graph database can efficiently model and query relationships between users, lost items, found items, categories, brands, and locations. Using CognoDB and Flask, the application provides an intuitive platform for reporting items and discovering possible matches through graph traversal.
