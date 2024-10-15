# Import necessary libraries
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

# Load environment variables
load_dotenv()

class storybook_rag:

    def __init__(self):
        print("DEBUG=> Initializing Rag...")
        # Load documents from a directory (you can change this path as needed)
        documents = SimpleDirectoryReader("data").load_data()
        print("DEBUG=> Start Indexing...")
        # Create index
        index = VectorStoreIndex.from_documents(documents)
        print("DEBUG=> End Indexing...")
        # Create retriever
        self.retriever = index.as_retriever(retrieval_mode='similarity', k=3)

    def get_relevant_docs(self, query):
        print("DEBUG=> Fetching relevant docs..")
        relevant_docs = self.retriever.retrieve(query)

        document_contents =[]

        for i,doc in enumerate(relevant_docs):
            document_contents.append(doc.node.get_content()[:2000])
        
        return document_contents