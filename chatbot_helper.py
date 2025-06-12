import sqlite3
import re
import numpy as np
from sentence_transformers import SentenceTransformer, util

DB_PATH = "database.db"
# EMBEDDING_MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(EMBEDDING_MODEL)

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def get_file_descriptions():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_path, description FROM file_metadata")
        return cursor.fetchall()

def rank_files_by_question(question):
    question_embedding = model.encode(question, convert_to_tensor=True)
    file_descriptions = get_file_descriptions()

    similarities = []
    for path, desc in file_descriptions:
        if not desc:
            continue
        desc_embedding = model.encode(desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(question_embedding, desc_embedding).item()
        similarities.append((similarity, path))

    similarities.sort(reverse=True)  # Higher score = more relevant
    return [path for score, path in similarities]

if __name__ == "__main__":
    question = input("Ask a question: ")
    ranked_paths = rank_files_by_question(question)
    print("Relevant files:")
    for path in ranked_paths:
        print("-", path)
