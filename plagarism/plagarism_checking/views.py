import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from docx import Document
from tempfile import NamedTemporaryFile

from transformers import pipeline

# Load models only once
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")


def splash_view(request):
    return render(request, 'splash.html')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not any(c.isupper() for c in username):
            raise ValidationError("Username must contain at least one uppercase letter.")
        return username


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home_view(request):
    def extract_text(source, is_textarea=False):
        if is_textarea:
            return source.strip()

        if not source:
            return ""

        try:
            ext = os.path.splitext(source.name)[1].lower()

            if ext in ['.png', '.jpg', '.jpeg']:
                img = Image.open(source)
                return pytesseract.image_to_string(img).strip()

            elif ext == '.txt':
                source.seek(0)
                return source.read().decode(errors='ignore').strip()

            elif ext == '.pdf':
                source.seek(0)
                pdf = fitz.open(stream=source.read(), filetype="pdf")
                return "".join(page.get_text() for page in pdf).strip()

            elif ext in ['.docx', '.doc']:
                return extract_docx(source)

            else:
                source.seek(0)
                return textract.process(source).decode('utf-8').strip()

        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    def extract_docx(file):
        text = ""
        file.seek(0)
        tmp_path = None
        try:
            with NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                for chunk in file.chunks():
                    tmp.write(chunk)
                tmp.flush()
                tmp_path = tmp.name
            doc = Document(tmp_path)
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        return text

    def highlight_common_sentences(text1, text2):
        sentences1 = [s.strip() for s in text1.replace('\n', '. ').split('.') if s.strip()]
        sentences2 = [s.strip() for s in text2.replace('\n', '. ').split('.') if s.strip()]

        common = set(sentences1) & set(sentences2)

        def mark(text, commons):
            for sentence in commons:
                if sentence in text:
                    text = text.replace(sentence, f'<mark>{sentence}</mark>')
            return text

        return mark(text1, common), mark(text2, common)

    if request.method == "POST":
        text1 = request.POST.get('text1', '').strip()
        text2 = request.POST.get('text2', '').strip()
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        question = request.POST.get('question', '').strip()
        question_target = request.POST.get('question_target', '').strip()  # which doc to ask

        doc1 = extract_text(file1) if file1 else extract_text(text1, is_textarea=True)
        doc2 = extract_text(file2) if file2 else extract_text(text2, is_textarea=True)

        if not doc1 or not doc2:
            if not doc1 and not doc2:
                messages.error(request, "❌ Both documents must contain some readable text or valid file content.")
            elif not doc1:
                messages.error(request, "❌ First document is empty or unreadable.")
            elif not doc2:
                messages.error(request, "❌ Second document is empty or unreadable.")
            return render(request, 'home.html')

        # TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([doc1, doc2])
        tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        # SBERT
        embeddings = sbert_model.encode([doc1, doc2])
        sbert_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

        hybrid_score = round((tfidf_score + sbert_score) / 2, 3)
        verdict = "Plagiarized" if hybrid_score >= 0.7 else "Unique"

        # Highlight common
        doc1_highlighted, doc2_highlighted = highlight_common_sentences(doc1, doc2)

        # Summarization
        try:
            summary1 = summarizer(doc1, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            summary2 = summarizer(doc2, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        except:
            summary1, summary2 = "⚠️ Summarization failed.", "⚠️ Summarization failed."

        # Q&A
        answer = ""
        if question and question_target in ["doc1", "doc2"]:
            context = doc1 if question_target == "doc1" else doc2
            try:
                result = qa_pipeline(question=question, context=context)
                if result['score'] >= 0.3:  # confidence threshold
                    answer = result['answer']
                else:
                    answer = "⚠️ Could not confidently find an answer."
            except:
                answer = "⚠️ Could not process your question."

        return render(request, 'home.html', {
            'doc1': doc1_highlighted,
            'doc2': doc2_highlighted,
            'tfidf_score': round(tfidf_score, 3),
            'sbert_score': round(sbert_score, 3),
            'hybrid_score': hybrid_score,
            'plagiarism': verdict,
            'summary1': summary1,
            'summary2': summary2,
            'question': question,
            'answer': answer,
            'question_target': question_target,
        })

    return render(request, 'home.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully.")
    return redirect('login')
