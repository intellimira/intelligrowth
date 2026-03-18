import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ACCTSemanticMesh:
    """
    Implements a Hybrid TF-IDF Semantic Mesh for ACCT.
    Provides mathematical similarity search across the Knowledge Base.
    """
    def __init__(self, system_path):
        self.system_path = system_path
        self.kb_path = os.path.join(system_path, "Knowledge_Base")
        self.mesh_path = os.path.join(system_path, "Memory_Mesh")
        self.db_path = os.path.join(system_path, "Laboratory/Vector_Mesh/db/semantic_mesh.pkl")
        
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.filenames = []
        self.tfidf_matrix = None

    def build_index(self):
        print("\n--- ACCT SEMANTIC MESH: BUILDING INDEX ---")
        documents = []
        
        # Collect all markdown files
        target_dirs = [self.kb_path, self.mesh_path]
        for target_dir in target_dirs:
            for root, _, files in os.walk(target_dir):
                for file in files:
                    if file.endswith(".md"):
                        path = os.path.join(root, file)
                        try:
                            with open(path, 'r', errors='ignore') as f:
                                documents.append(f.read())
                                self.filenames.append(path)
                        except Exception:
                            continue
        
        if not documents:
            print("[!] No documents found for indexing.")
            return

        print(f"[*] Vectorizing {len(documents)} documents...")
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        # Save the index
        with open(self.db_path, 'wb') as f:
            pickle.dump((self.vectorizer, self.filenames, self.tfidf_matrix), f)
        
        print(f"[+] Indexing Complete. Saved to {os.path.basename(self.db_path)}")

    def semantic_search(self, query, top_k=5):
        if self.tfidf_matrix is None:
            # Load existing index
            with open(self.db_path, 'rb') as f:
                self.vectorizer, self.filenames, self.tfidf_matrix = pickle.load(f)

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Rank results
        related_indices = similarities.argsort()[::-1][:top_k]
        
        print(f"\n--- ACCT SEMANTIC SEARCH: '{query}' ---")
        for idx in related_indices:
            score = similarities[idx]
            if score > 0:
                print(f"[*] RESULT: {os.path.basename(self.filenames[idx])} (Sim: {score:.4f})")
                print(f"    Path: ...{self.filenames[idx].split('ACCT_SYSTEM')[-1]}")
                print("-" * 20)

if __name__ == "__main__":
    mesh = ACCTSemanticMesh("/home/sir-v/ACCT_SYSTEM")
    # Step 1: Index the system
    mesh.build_index()
    # Step 2: Test a semantic query
    mesh.semantic_search("how do I integrate sensory nodes and vision?")
