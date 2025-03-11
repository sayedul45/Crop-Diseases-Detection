# 🌱 ফসল রোগ সনাক্তকরণ (Crop Disease Detection) 🚜  

This project detects crop diseases using **YOLO (Object Detection)** and **ViT (Vision Transformer for Classification)**.  
It also provides **treatment recommendations** using **FAISS vector database** and **LangChain RAG** with **Bengali translations**.  

---

## 🚀 Features
✅ Detects crop diseases from leaf images 📷  
✅ Provides **Bengali** treatment plans using **FAISS + LangChain**  
✅ **Flask Backend** for model inference 🖥️  
✅ **Gradio Frontend** for easy image upload 🌐  
✅ **Docker support** for easy deployment 🐳  

---

## 📁 Project Structure
crop_disease_detection/ │── backend/ # Flask backend │ ├── app.py # Main API for model inference │ ├── model.py # YOLO & ViT model loader │ ├── vector_db.py # FAISS & LangChain retrieval │ ├── requirements.txt # Backend dependencies │── frontend/ # Gradio UI │ ├── app.py # Main Gradio interface │ ├── requirements.txt # Frontend dependencies │── models/ # Trained model weights │ ├── best.pt # YOLOv8 model │ ├── vit_best/ # ViT model │── vector_db/ # FAISS database │ ├── disease_vectordb/
│ ├── index.faiss
│ ├── index.pkl
│── data/ # Disease information │ ├── disease_knowledge.json │── docker/ # Docker setup │ ├── backend.Dockerfile
│ ├── frontend.Dockerfile
│── docker-compose.yml # Orchestration file │── README.md # Documentation │── .gitignore # Ignore unnecessary files

