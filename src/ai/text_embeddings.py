"""
Text Embeddings Module
Vector embeddings for semantic search, similarity matching, and clustering.
"""

import os
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import faiss
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️ sentence-transformers not available. Install with: pip install sentence-transformers")

class TextEmbeddings:
    """
    Text embeddings for semantic search and similarity analysis.
    Uses sentence transformers for high-quality embeddings.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "models/embeddings"):
        """
        Initialize text embeddings.

        Args:
            model_name: Sentence transformer model name
            cache_dir: Directory to cache models and indices
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.model = None
        self.index = None
        self.feedback_data = []
        self.embeddings = None

        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name, cache_folder=str(self.cache_dir))
                print(f"✓ Text embeddings model loaded: {model_name}")
            except Exception as e:
                print(f"⚠️ Failed to load embeddings model: {e}")
        else:
            print("⚠️ Sentence transformers not available for embeddings")

    def is_available(self) -> bool:
        """Check if embeddings are available."""
        return self.model is not None

    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings
            batch_size: Batch size for processing

        Returns:
            Numpy array of embeddings
        """
        if not self.is_available():
            raise RuntimeError("Embeddings model not available")

        if not texts:
            return np.array([])

        try:
            # Generate embeddings in batches to manage memory
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.model.encode(batch_texts, convert_to_numpy=True)
                all_embeddings.append(batch_embeddings)

            embeddings = np.vstack(all_embeddings)
            return embeddings

        except Exception as e:
            print(f"Embedding generation failed: {e}")
            raise

    def build_search_index(self, feedback_data: List[Dict[str, Any]]) -> bool:
        """
        Build FAISS search index from feedback data.

        Args:
            feedback_data: List of feedback dictionaries

        Returns:
            Success status
        """
        if not self.is_available():
            return False

        try:
            self.feedback_data = feedback_data

            # Prepare texts for embedding
            texts = []
            for fb in feedback_data:
                # Combine title and feedback for better search
                text = f"{fb.get('title', '')} {fb.get('feedback', '')}".strip()
                if not text:
                    text = "No content available"
                texts.append(text)

            # Generate embeddings
            print(f"Generating embeddings for {len(texts)} feedback items...")
            self.embeddings = self.generate_embeddings(texts)

            # Build FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)

            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)

            # Save index
            self._save_index()

            print(f"✓ Search index built with {len(feedback_data)} items")
            return True

        except Exception as e:
            print(f"⚠️ Failed to build search index: {e}")
            return False

    def _save_index(self):
        """Save the FAISS index and data."""
        try:
            if self.index and self.embeddings is not None:
                # Save FAISS index
                faiss.write_index(self.index, str(self.cache_dir / 'feedback_index.faiss'))

                # Save embeddings and data
                np.save(self.cache_dir / 'embeddings.npy', self.embeddings)
                joblib.dump(self.feedback_data, self.cache_dir / 'feedback_data.pkl')

                print("✓ Search index saved")

        except Exception as e:
            print(f"⚠️ Failed to save index: {e}")

    def _load_index(self) -> bool:
        """Load saved FAISS index."""
        try:
            index_path = self.cache_dir / 'feedback_index.faiss'
            embeddings_path = self.cache_dir / 'embeddings.npy'
            data_path = self.cache_dir / 'feedback_data.pkl'

            if all(p.exists() for p in [index_path, embeddings_path, data_path]):
                self.index = faiss.read_index(str(index_path))
                self.embeddings = np.load(embeddings_path)
                self.feedback_data = joblib.load(data_path)

                print("✓ Search index loaded")
                return True

        except Exception as e:
            print(f"⚠️ Failed to load index: {e}")

        return False

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search on feedback data.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of similar feedback items with scores
        """
        if not self.index or self.embeddings is None:
            if not self._load_index():
                return []

        try:
            # Generate embedding for query
            query_embedding = self.generate_embeddings([query])
            faiss.normalize_L2(query_embedding)

            # Search
            scores, indices = self.index.search(query_embedding, top_k)

            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.feedback_data):
                    feedback_item = self.feedback_data[idx].copy()
                    feedback_item['similarity_score'] = float(score)
                    results.append(feedback_item)

            return results

        except Exception as e:
            print(f"Semantic search failed: {e}")
            return []

    def find_similar_feedback(self, feedback_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find feedback items similar to a given feedback.

        Args:
            feedback_id: ID of the feedback to find similar items for
            top_k: Number of similar items to return

        Returns:
            List of similar feedback items
        """
        # Find the feedback item
        target_feedback = None
        for fb in self.feedback_data:
            if fb.get('id') == feedback_id:
                target_feedback = fb
                break

        if not target_feedback:
            return []

        # Use the feedback text as search query
        query = f"{target_feedback.get('title', '')} {target_feedback.get('feedback', '')}"
        similar_items = self.semantic_search(query, top_k + 1)  # +1 to exclude self

        # Remove the original feedback from results
        return [item for item in similar_items if item.get('id') != feedback_id][:top_k]

    def detect_duplicates(self, threshold: float = 0.9) -> List[Dict[str, Any]]:
        """
        Detect duplicate or very similar feedback items.

        Args:
            threshold: Similarity threshold for duplicates

        Returns:
            List of duplicate groups
        """
        if not self.embeddings is not None:
            return []

        try:
            # Compute similarity matrix
            similarity_matrix = np.dot(self.embeddings, self.embeddings.T)

            # Find highly similar pairs
            duplicate_groups = []
            processed = set()

            for i in range(len(self.feedback_data)):
                if i in processed:
                    continue

                duplicates = []
                for j in range(i + 1, len(self.feedback_data)):
                    if similarity_matrix[i, j] >= threshold:
                        if i not in processed:
                            duplicates.append(self.feedback_data[i])
                            processed.add(i)
                        duplicates.append(self.feedback_data[j])
                        processed.add(j)

                if len(duplicates) > 1:
                    duplicate_groups.append({
                        'group_id': f"group_{len(duplicate_groups)}",
                        'duplicates': duplicates,
                        'count': len(duplicates)
                    })

            return duplicate_groups

        except Exception as e:
            print(f"Duplicate detection failed: {e}")
            return []

    def cluster_feedback(self, n_clusters: int = 10) -> Dict[str, Any]:
        """
        Cluster feedback items into thematic groups.

        Args:
            n_clusters: Number of clusters

        Returns:
            Clustering results
        """
        if self.embeddings is None:
            return {'clusters': [], 'error': 'No embeddings available'}

        try:
            from sklearn.cluster import KMeans

            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(self.embeddings)

            # Group feedback by clusters
            clusters = {}
            for i, label in enumerate(cluster_labels):
                cluster_id = f"cluster_{label}"
                if cluster_id not in clusters:
                    clusters[cluster_id] = []

                feedback_item = self.feedback_data[i].copy()
                feedback_item['cluster_id'] = cluster_id
                clusters[cluster_id].append(feedback_item)

            # Calculate cluster centroids and themes
            cluster_info = []
            for cluster_id, items in clusters.items():
                cluster_embeddings = self.embeddings[[i for i, fb in enumerate(self.feedback_data)
                                                    if fb.get('cluster_id') == cluster_id]]

                centroid = np.mean(cluster_embeddings, axis=0)

                cluster_info.append({
                    'cluster_id': cluster_id,
                    'size': len(items),
                    'centroid': centroid.tolist(),
                    'sample_titles': [item.get('title', 'Untitled') for item in items[:5]],
                    'categories': list(set(item.get('category', 'Unknown') for item in items))
                })

            return {
                'clusters': cluster_info,
                'total_clusters': n_clusters,
                'method': 'kmeans'
            }

        except Exception as e:
            print(f"Clustering failed: {e}")
            return {'clusters': [], 'error': str(e)}

    def get_feedback_insights(self) -> Dict[str, Any]:
        """
        Generate insights from feedback embeddings.

        Returns:
            Various insights and statistics
        """
        if not self.feedback_data or self.embeddings is None:
            return {'error': 'No data available'}

        try:
            insights = {
                'total_feedbacks': len(self.feedback_data),
                'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else 0,
                'average_similarity': float(np.mean(self._compute_similarity_stats())),
                'duplicate_groups': len(self.detect_duplicates()),
                'clusters': self.cluster_feedback(n_clusters=min(10, len(self.feedback_data)//5))['clusters']
            }

            return insights

        except Exception as e:
            return {'error': str(e)}

    def _compute_similarity_stats(self) -> np.ndarray:
        """Compute similarity statistics."""
        if self.embeddings is None:
            return np.array([])

        # Sample similarities for performance
        sample_size = min(1000, len(self.embeddings))
        indices = np.random.choice(len(self.embeddings), sample_size, replace=False)
        sample_embeddings = self.embeddings[indices]

        similarity_matrix = np.dot(sample_embeddings, sample_embeddings.T)
        # Get upper triangle values (excluding diagonal)
        similarities = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]

        return similarities

    def update_index(self, new_feedback: List[Dict[str, Any]]) -> bool:
        """
        Update the search index with new feedback.

        Args:
            new_feedback: New feedback items to add

        Returns:
            Success status
        """
        if not new_feedback:
            return True

        try:
            # Add to existing data
            self.feedback_data.extend(new_feedback)

            # Generate embeddings for new items
            new_texts = [f"{fb.get('title', '')} {fb.get('feedback', '')}".strip() for fb in new_feedback]
            new_embeddings = self.generate_embeddings(new_texts)

            # Update embeddings array
            if self.embeddings is not None:
                self.embeddings = np.vstack([self.embeddings, new_embeddings])
            else:
                self.embeddings = new_embeddings

            # Rebuild FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)

            # Save updated index
            self._save_index()

            print(f"✓ Index updated with {len(new_feedback)} new items")
            return True

        except Exception as e:
            print(f"⚠️ Failed to update index: {e}")
            return False