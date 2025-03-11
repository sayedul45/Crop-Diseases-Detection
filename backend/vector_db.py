import os
import re
import json
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from deep_translator import GoogleTranslator

class DiseaseRAGSystem:
    def __init__(self, db_path="../vector_db/diseases_vectordb/"):
        """Load FAISS vector database for disease treatment plans."""
        print("Loading FAISS Vector Database...")

        # Load embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load FAISS index
        self.vectordb = FAISS.load_local(db_path, self.embeddings, allow_dangerous_deserialization=True)

        # Initialize Translator (English → Bengali)
        self.translator = GoogleTranslator(source='en', target='bn')

        # Load stored disease knowledge
        disease_file = os.path.join("../data", "disease_knowledge.json")
        with open(disease_file, "r") as f:
            self.disease_data = json.load(f)

    def get_treatment_plan(self, disease_name):
        """Retrieve treatment plan using FAISS similarity search."""
        print(f"Retrieving treatment for: {disease_name}")

        # Check if disease exists in knowledge base
        direct_match = next((d for d in self.disease_data if d["disease"].lower() == disease_name.lower()), None)

        if direct_match:
            return self._format_response(direct_match)

        # Perform FAISS retrieval if no direct match
        retrieved_docs = self.vectordb.similarity_search(disease_name, k=3)

        if retrieved_docs:
            return self._format_response_from_docs(retrieved_docs)

        return self._fallback_response(disease_name)

    def _format_response(self, disease_info):
        """Format and translate response."""
        translated = {
            "disease": self.translator.translate(disease_info["disease"]),
            "symptoms": self.translator.translate(disease_info["symptoms"]),
            "treatment": self.translator.translate(disease_info["treatment"]),
            "prevention": self.translator.translate(disease_info["best_practices"]),
        }

        return {
            "english": disease_info,
            "bengali": translated,
            "source": disease_info["source"]
        }

    def _format_response_from_docs(self, docs):
        """Extract and translate retrieved documents."""
        context = "\n".join([doc.page_content for doc in docs])
        symptoms = self._extract_section("Symptoms", context)
        treatment = self._extract_section("Treatment", context)
        prevention = self._extract_section("Best Practices", context)

        return {
            "english": {
                "disease": docs[0].page_content.split("\n")[0].replace("Disease: ", ""),
                "symptoms": symptoms,
                "treatment": treatment,
                "prevention": prevention
            },
            "bengali": {
                "disease": self.translator.translate(docs[0].page_content.split("\n")[0]),
                "symptoms": self.translator.translate(symptoms),
                "treatment": self.translator.translate(treatment),
                "prevention": self.translator.translate(prevention)
            },
            "source": "Retrieved from FAISS Vector DB"
        }

    def _extract_section(self, section_name, text):
        """Extract relevant section from retrieved documents."""
        match = re.search(rf"{section_name}:\s*(.*?)(?=\n\w+:|$)", text, re.DOTALL)
        return match.group(1).strip() if match else "No data available"

    def _fallback_response(self, disease_name):
        """Provide a default response when no match is found."""
        return {
            "english": {
                "disease": disease_name,
                "symptoms": "General symptoms like leaf discoloration or abnormal growth.",
                "treatment": "Apply appropriate fungicides or pesticides.",
                "prevention": "Ensure good crop rotation and maintain plant hygiene."
            },
            "bengali": {
                "disease": self.translator.translate(disease_name),
                "symptoms": self.translator.translate("General symptoms like leaf discoloration or abnormal growth."),
                "treatment": self.translator.translate("Apply appropriate fungicides or pesticides."),
                "prevention": self.translator.translate("Ensure good crop rotation and maintain plant hygiene.")
            },
            "source": "Generated fallback response"
        }
