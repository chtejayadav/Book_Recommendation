import streamlit as st
import pandas as pd
import base64
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# Function to encode GIF in base64
def get_base64_of_gif(file_path):
    with open(file_path, "rb") as gif_file:
        encoded_gif = base64.b64encode(gif_file.read()).decode()
    return f"data:image/gif;base64,{encoded_gif}"

# Set background GIF
gif_path = "bg.gif"  # Change this to your local GIF file path
base64_gif = get_base64_of_gif(gif_path)

st.markdown(
    f"""
    <style>
    body {{
        background: url("{base64_gif}");
        background-size: cover;
    }}
    .stApp {{
        background-color: rgba(255, 255, 255, 0.5);
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
df = pd.read_csv("br.csv")

# Combine relevant text features for similarity calculation
df["combined_features"] = df["genre"] + " " + df["author"]

# Convert text data into numerical representation using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
feature_matrix = vectorizer.fit_transform(df["combined_features"])

# Compute similarity matrix using cosine similarity
similarity_matrix = cosine_similarity(feature_matrix)

# Function to get book recommendations
def recommend_books(book_title, top_n=5):
    if book_title not in df["title"].values:
        return [f"Book '{book_title}' not found in the dataset."]
    
    book_idx = df[df["title"] == book_title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[book_idx]))
    sorted_books = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_books = [df.iloc[i[0]]["title"] for i in sorted_books]
    return recommended_books


st.title("📚 Book Recommendation System")
st.write("Select a book title to get similar recommendations based on genre and author.")

# Dropdown for book selection
book_title = st.selectbox("Select a book title:", df["title"].unique())

if book_title:
    recommendations = recommend_books(book_title)
    st.subheader("Recommended Books:")
    for book in recommendations:
        st.write(f"- {book}")
