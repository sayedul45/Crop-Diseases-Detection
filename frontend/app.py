import gradio as gr
import requests

API_URL = "http://127.0.0.1:5000/predict"  # Change for Docker if needed

def predict(image_path):
    """Sends an image to the backend for prediction and returns Bengali results."""
    try:
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            result = response.json()

            if "বাংলা_ফলাফল" in result:
                output = "\n".join([
                    f"🦠 রোগ: {disease['🦠 রোগ']}\n"
                    f"\n🚩 লক্ষণ:\n{disease['🚩 লক্ষণ']}\n"
                    f"\n💊 চিকিৎসা:\n{disease['💊 চিকিৎসা']}\n"
                    f"\n🛡️ প্রতিরোধ:\n{disease['🛡️ প্রতিরোধ']}\n"
                    f"\n{'=' * 40}\n"
                    for disease in result["বাংলা_ফলাফল"]
                ])

                return output.strip()

        return "⚠️ সমস্যার কারণে ফলাফল আনতে ব্যর্থ।"
    
    except Exception as e:
        return f"⚠️ ত্রুটি হয়েছে: {str(e)}"

iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="filepath"),
    outputs="text",  # Display as text to keep formatting clean
    title="ফসল রোগ সনাক্তকরণ (Crop Disease Detection)",
    description="আপনার ফসলের পাতা আপলোড করুন এবং রোগ সম্পর্কে তথ্য পান।"
)

iface.launch(server_name="127.0.0.1", server_port=7860)
