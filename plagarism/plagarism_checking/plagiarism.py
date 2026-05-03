from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

sbert_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

def check_plagiarism(text1, text2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
    tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    emb1, emb2 = sbert_model.encode([text1, text2])
    sbert_score = cosine_similarity([emb1.reshape(1, -1)], [emb2.reshape(1, -1)])[0][0]

    hybrid = (tfidf_score + sbert_score) / 2
    verdict = "Plagiarized" if hybrid > 0.65 else "Unique"

    return {
        'tfidf': round(tfidf_score, 3),
        'sbert': round(sbert_score, 3),
        'hybrid': round(hybrid, 3),
        'verdict': verdict
    }
