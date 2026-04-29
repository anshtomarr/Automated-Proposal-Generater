"""
RAG query layer — keyword-based retrieval from the historical proposals database.
"""

import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "proposals.db")


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from raw text for SQL matching."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "must", "to", "of",
        "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "above", "below", "between", "out", "off",
        "over", "under", "again", "further", "then", "once", "and", "but", "or",
        "nor", "not", "so", "yet", "both", "either", "neither", "each", "every",
        "all", "any", "few", "more", "most", "other", "some", "such", "no",
        "only", "own", "same", "than", "too", "very", "just", "because", "if",
        "when", "where", "how", "what", "which", "who", "whom", "this", "that",
        "these", "those", "i", "me", "my", "we", "our", "you", "your", "he",
        "him", "his", "she", "her", "it", "its", "they", "them", "their",
        "want", "like", "also", "us", "about", "up",
    }

    words = re.findall(r'[a-zA-Z]+', text.lower())
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]

    seen = set()
    unique = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)

    return unique[:30]


def query_similar_projects(text: str) -> list[dict]:
    """
    Query the database for projects matching keywords from the given text.
    Returns a list of matched project dicts, ranked by number of keyword hits.
    """
    keywords = extract_keywords(text)

    if not keywords:
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    where_clauses = []
    params = []
    for kw in keywords:
        where_clauses.append(
            "(LOWER(keywords) LIKE ? OR LOWER(description) LIKE ? OR LOWER(project_type) LIKE ?)"
        )
        pattern = f"%{kw}%"
        params.extend([pattern, pattern, pattern])

    query = f"""
        SELECT *, (
            {' + '.join([
                f"(CASE WHEN LOWER(keywords) LIKE ? OR LOWER(description) LIKE ? THEN 1 ELSE 0 END)"
                for _ in keywords
            ])}
        ) as relevance_score
        FROM projects 
        WHERE {' OR '.join(where_clauses)}
        ORDER BY relevance_score DESC
        LIMIT 3
    """

    score_params = []
    for kw in keywords:
        pattern = f"%{kw}%"
        score_params.extend([pattern, pattern])

    cursor.execute(query, score_params + params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "project_type": row["project_type"],
            "title": row["title"],
            "description": row["description"],
            "tech_stack": row["tech_stack"],
            "timeline": row["timeline"],
            "complexity": row["complexity"],
            "budget_range": row["budget_range"],
            "outcome": row["outcome"],
            "relevance_score": row["relevance_score"],
        }
        for row in rows
    ]


if __name__ == "__main__":
    results = query_similar_projects("We need an e-commerce platform with payment processing")
    for r in results:
        print(f"[Score: {r['relevance_score']}] {r['title']} — {r['project_type']}")
