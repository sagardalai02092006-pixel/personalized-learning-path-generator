# Personalized Learning Path Generator

A web-based Data Structures and Algorithms project that recommends a valid order for learning topics using prerequisite relationships. The project demonstrates a Directed Acyclic Graph (DAG), topological sorting, and dynamic programming.

## Features

- Select a target topic to learn.
- Mark topics that have already been completed.
- Generate a learning path containing the target and its prerequisite topics.
- Display estimated study hours and the longest prerequisite-chain duration.
- Visualize the generated sequence in a responsive web interface.
- Detect cycles in the prerequisite graph.
- Expose simple JSON endpoints for the topic list and learning path.

## DSA concepts

### Directed Acyclic Graph (DAG)
Each topic is a vertex. An edge `A -> B` means topic A is a prerequisite for topic B. The graph must be acyclic for a valid topological order to exist.

### Topological sorting
Kahn's algorithm uses indegrees and a queue to produce an order where every prerequisite appears before its dependent topic.

Time complexity: `O(V + E)`, where V is the number of topics and E is the number of prerequisite edges.

### Dynamic programming
The app computes the longest prerequisite-chain duration for each topic in topological order:

`dp[topic] = hours(topic) + max(dp[prerequisite])`

For a topic with no prerequisites, `dp[topic] = hours(topic)`.

This estimates the duration of the longest dependency chain. The app separately shows the sum of hours for all remaining required topics. These are different estimates: the former assumes independent topics on different branches may be studied in parallel, while the latter adds every remaining topic's estimated hours.

## Tech stack

- Python
- Flask
- HTML
- CSS
- JavaScript

## Run locally

### 1. Install Python
Use Python 3.10 or newer.

### 2. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```


Open the local address shown in the terminal (normally `http://127.0.0.1:5000`).
### images 
<img width="1920" height="1080" alt="Screenshot (64)" src="https://github.com/user-attachments/assets/60f7b850-56c1-47e0-b528-da5f8ea972a5" />
<img width="1920" height="1080" alt="Screenshot (65)" src="https://github.com/user-attachments/assets/8501cb61-0ab5-453b-ab8b-7ada83e2d92c" />


## API examples

### Get all topics

```http
GET /api/topics
```

### Generate a learning path

```http
POST /api/path
Content-Type: application/json
```

Example request:

```json
{
  "target": "Binary Search Trees",
  "completed": ["Programming Basics", "Arrays"]
}
```

The response includes the ordered path, required topic count, remaining study-hour estimate, and critical prerequisite-chain duration.

## Project structure

```text
personalized-learning-path/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Algorithm overview

1. Store topics and prerequisite lists.
2. Build an adjacency list and indegree map.
3. Starting from the target, find all prerequisite topics.
4. Run topological sorting on the required subgraph.
5. Remove topics the student has marked as completed.
6. Use dynamic programming over the topological order to calculate the longest prerequisite-chain duration.
7. Display the path and estimates in the web interface.

## Limitations and future improvements

- The topic catalog and estimated hours are sample data and can be customized.
- The current version treats completion as a user-provided checkbox selection.
- Personalization is based on the target topic and completed topics; it does not yet learn from quiz scores.
- A future version could add user accounts, a database, editable prerequisites, quiz-based difficulty estimates, and a visual DAG graph.
- For a production deployment, disable Flask debug mode and add input validation, authentication if needed, and persistent storage.

## GitHub project description

A web application that generates prerequisite-aware learning paths using DAGs, topological sorting, and dynamic programming. Built with Python, Flask, HTML, CSS, and JavaScript.

## Suggested GitHub topics

`dsa` `graph-algorithms` `topological-sort` `dynamic-programming` `python` `flask` `learning-path` `web-application`

## Author

Add your name, institution, and project details here before publishing.
