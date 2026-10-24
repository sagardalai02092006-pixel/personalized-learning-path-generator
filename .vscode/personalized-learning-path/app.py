from flask import Flask, render_template, request, jsonify
from collections import deque
from functools import lru_cache

app = Flask(__name__)

# Each edge prerequisite -> topic means the prerequisite should be learned first.
TOPICS = {
    "Programming Basics": {
        "prerequisites": [], "hours": 3, "difficulty": "Beginner",
        "description": "Variables, conditions, loops, and functions."
    },
    "Arrays": {
        "prerequisites": ["Programming Basics"], "hours": 2, "difficulty": "Beginner",
        "description": "Indexing, traversal, insertion, and deletion."
    },
    "Linked Lists": {
        "prerequisites": ["Programming Basics"], "hours": 3, "difficulty": "Beginner",
        "description": "Nodes, pointers/references, and list operations."
    },
    "Stacks and Queues": {
        "prerequisites": ["Arrays"], "hours": 2, "difficulty": "Beginner",
        "description": "LIFO and FIFO data structures and their applications."
    },
    "Searching": {
        "prerequisites": ["Arrays"], "hours": 2, "difficulty": "Beginner",
        "description": "Linear search and binary search."
    },
    "Sorting": {
        "prerequisites": ["Arrays"], "hours": 3, "difficulty": "Intermediate",
        "description": "Bubble, insertion, selection, merge, and quick sort."
    },
    "Recursion": {
        "prerequisites": ["Programming Basics"], "hours": 3, "difficulty": "Intermediate",
        "description": "Base cases, recursive calls, and call stack."
    },
    "Trees": {
        "prerequisites": ["Recursion"], "hours": 3, "difficulty": "Intermediate",
        "description": "Tree terminology, traversals, and binary trees."
    },
    "Binary Search Trees": {
        "prerequisites": ["Trees", "Searching"], "hours": 3, "difficulty": "Intermediate",
        "description": "BST insertion, search, deletion, and traversal."
    },
    "Graphs": {
        "prerequisites": ["Stacks and Queues"], "hours": 4, "difficulty": "Intermediate",
        "description": "Graph representations, BFS, and DFS."
    },
    "Dynamic Programming": {
        "prerequisites": ["Recursion"], "hours": 4, "difficulty": "Advanced",
        "description": "Overlapping subproblems, memoization, and tabulation."
    },
    "Advanced Graph Algorithms": {
        "prerequisites": ["Graphs", "Dynamic Programming"], "hours": 5, "difficulty": "Advanced",
        "description": "Shortest paths, DAG algorithms, and graph optimization."
    }
}


def build_graph():
    """Build adjacency list and indegree map for the full prerequisite DAG."""
    graph = {topic: [] for topic in TOPICS}
    indegree = {topic: 0 for topic in TOPICS}
    for topic, info in TOPICS.items():
        for prerequisite in info["prerequisites"]:
            if prerequisite not in TOPICS:
                raise ValueError(f"Unknown prerequisite: {prerequisite}")
            graph[prerequisite].append(topic)
            indegree[topic] += 1
    return graph, indegree


def topological_sort(nodes=None):
    """Kahn's algorithm. Returns a valid order or raises an error if a cycle exists."""
    graph, _ = build_graph()
    nodes = set(nodes or TOPICS.keys())
    indegree = {node: 0 for node in nodes}

    for source in nodes:
        for destination in graph[source]:
            if destination in nodes:
                indegree[destination] += 1

    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in sorted(graph[node]):
            if neighbor in indegree:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

    if len(order) != len(nodes):
        raise ValueError("A cycle was found in the prerequisite graph.")
    return order


def prerequisite_closure(target):
    """Return the target and every topic needed before it, recursively."""
    required = set()

    def visit(topic):
        if topic in required:
            return
        required.add(topic)
        for prerequisite in TOPICS[topic]["prerequisites"]:
            visit(prerequisite)

    visit(target)
    return required


def longest_prerequisite_hours(required):
    """
    Dynamic programming on the DAG.
    For each topic, calculate the longest prerequisite-chain duration ending there.
    This estimates the critical-path time if topics on the same level can be studied
    independently; it is not the sum of every topic's hours.
    """
    order = topological_sort(required)
    best = {}
    previous = {}

    for topic in order:
        prereqs = [p for p in TOPICS[topic]["prerequisites"] if p in required]
        if not prereqs:
            best[topic] = TOPICS[topic]["hours"]
            previous[topic] = None
        else:
            parent = max(prereqs, key=lambda p: best[p])
            best[topic] = best[parent] + TOPICS[topic]["hours"]
            previous[topic] = parent

    return best, previous


def generate_path(target, completed):
    if target not in TOPICS:
        raise ValueError("Please select a valid target topic.")

    required = prerequisite_closure(target)
    order = topological_sort(required)
    requested_completed = set(completed) & required
    completed_valid = set()

    # Respect prerequisite order: a topic is counted as completed only when
    # all of its required prerequisites are also counted as completed.
    for topic in order:
        prereqs = [p for p in TOPICS[topic]["prerequisites"] if p in required]
        if topic in requested_completed and all(p in completed_valid for p in prereqs):
            completed_valid.add(topic)

    remaining = [topic for topic in order if topic not in completed_valid]

    best, previous = longest_prerequisite_hours(required)
    total_hours = sum(TOPICS[t]["hours"] for t in remaining)

    path = []
    for index, topic in enumerate(remaining, start=1):
        info = TOPICS[topic]
        path.append({
            "step": index,
            "name": topic,
            "hours": info["hours"],
            "difficulty": info["difficulty"],
            "description": info["description"],
            "prerequisites": info["prerequisites"],
            "completed": False
        })

    return {
        "target": target,
        "path": path,
        "completed_count": len(completed_valid),
        "required_count": len(required),
        "remaining_count": len(remaining),
        "estimated_hours": total_hours,
        "critical_path_hours": best[target],
        "all_required_topics": order
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        topics=[
            {"name": name, **info}
            for name, info in TOPICS.items()
        ]
    )


@app.route("/api/path", methods=["POST"])
def api_path():
    data = request.get_json(silent=True) or {}
    target = data.get("target", "")
    completed = data.get("completed", [])
    if not isinstance(completed, list):
        return jsonify({"error": "Completed topics must be a list."}), 400
    try:
        result = generate_path(target, completed)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/topics", methods=["GET"])
def api_topics():
    return jsonify([
        {"name": name, **info} for name, info in TOPICS.items()
    ])


if __name__ == "__main__":
    app.run(debug=True)
