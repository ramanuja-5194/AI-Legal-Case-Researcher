
import os, json, glob
from tqdm import tqdm
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from .config import settings
from .utils.text_preprocess import clean_legal_text

def iter_txt_files(root):
    for p in glob.glob(os.path.join(root, "**/*.txt"), recursive=True):
        yield p

def main():
    corpus_dir = settings.corpus_dir
    vs_dir = settings.vectorstore_dir
    os.makedirs(vs_dir, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " "]
    )
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    all_docs = []
    for path in tqdm(list(iter_txt_files(corpus_dir)), desc="Loading corpus"):
        loader = TextLoader(path, autodetect_encoding=True)
        docs = loader.load()
        for d in docs:
            d.page_content = clean_legal_text(d.page_content)
            md = d.metadata or {}
            md.setdefault("source", path)
            md.setdefault("title", os.path.basename(path))
        chunks = splitter.split_documents(docs)
        all_docs.extend(chunks)

    if not all_docs:
        print("No documents found in corpus. Put .txt files under:", corpus_dir)
        return

    print(f"Building FAISS on {len(all_docs)} chunks...")
    vs = FAISS.from_documents(all_docs, embeddings)
    vs.save_local(vs_dir)
    print("Vectorstore saved to:", vs_dir)

if __name__ == "__main__":
    main()
