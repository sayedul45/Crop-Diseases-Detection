from flask import Flask, request, jsonify
from model import detect_disease
from vector_db import DiseaseRAGSystem
import os

app = Flask(__name__)

# Initialize RAG system
rag_system = DiseaseRAGSystem()

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    
    # Ensure temp directory exists
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    image_path = os.path.join(temp_dir, file.filename)
    file.save(image_path)

    try:
        # Detect disease
        predictions = detect_disease(image_path)

        # Retrieve treatment plans for detected diseases
        bengali_results = []
        seen_diseases = set()  # To prevent duplicate diseases

        for pred in predictions.get("detections", []):
            disease_name = pred["disease"].strip()  # Clean disease name
            if disease_name in seen_diseases:
                continue  # Skip duplicate diseases
            seen_diseases.add(disease_name)

            try:
                treatment_plan = rag_system.get_treatment_plan(disease_name)

                # Clean up text and remove redundant lines
                symptoms = treatment_plan["bengali"]["symptoms"].split("।")[0]  # Keep first sentence only
                treatment = treatment_plan["bengali"]["treatment"].split("।")[0]  # Keep first sentence only
                prevention = treatment_plan["bengali"]["prevention"].split("।")[0]  # Keep first sentence only

                bengali_results.append({
                    "🦠 রোগ": disease_name,  # Remove duplicate "রোগ: রোগ:"
                    "🚩 লক্ষণ": symptoms.strip(),
                    "💊 চিকিৎসা": treatment.strip(),
                    "🛡️ প্রতিরোধ": prevention.strip()
                })

            except Exception as e:
                bengali_results.append({
                    "🦠 রোগ": disease_name,
                    "🚩 লক্ষণ": "তথ্য পাওয়া যায়নি।",
                    "💊 চিকিৎসা": "তথ্য পাওয়া যায়নি।",
                    "🛡️ প্রতিরোধ": "তথ্য পাওয়া যায়নি।",
                    "ত্রুটি": f"তথ্য আনতে সমস্যা হয়েছে: {str(e)}"
                })

        return jsonify({"বাংলা_ফলাফল": bengali_results})
    
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
