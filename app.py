from flask import Flask, request, send_file, jsonify
import torchaudio
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
import io

app = Flask(__name__)

# Инициализируйте модель
model = AudioGen.get_pretrained('facebook/audiogen-medium')

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    descriptions = data.get('descriptions', [])
    
    # Получите значение duration из запроса
    duration = data.get('duration', 5)
    
    # Проверьте, чтобы duration был числом и в допустимом диапазоне
    if not isinstance(duration, int) or not (5 <= duration <= 300):
        duration = 5
    
    model.set_generation_params(duration=duration)
    
    wav = model.generate(descriptions)
    
    # Создайте буфер для первого аудиофайла
    buffer = io.BytesIO()
    audio_write(buffer, wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    buffer.seek(0)

    # Отправьте файл в ответе
    return send_file(buffer, attachment_filename='generated_audio.wav', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
