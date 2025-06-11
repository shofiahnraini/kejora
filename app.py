import gradio as gr
import requests
from datetime import datetime, timedelta

API_KEY = "e655015edec8dbbcae8e6b498a5afe09"
CITY = "Jakarta"

def get_weather(year, month, day):
    try:
        selected_date = datetime(year, month, day).date()
        today = datetime.now().date()
        max_date = today + timedelta(days=5)

        if selected_date < today:
            return "❌ Tanggal yang dipilih sudah lewat."
        if selected_date > max_date:
            return "❌ Tanggal maksimal hanya sampai 5 hari ke depan."

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return f"❌ Gagal mengambil data: {data.get('message', 'Unknown error')}"

        target_str = selected_date.strftime("%Y-%m-%d") + " 12:00:00"
        for entry in data["list"]:
            if entry["dt_txt"] == target_str:
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                return f"📅 {selected_date} di Jakarta:\n🌡️ Suhu: {temp}°C\n🌤️ Deskripsi: {desc.capitalize()}"

        return "⚠️ Data cuaca belum tersedia untuk tanggal itu."

    except Exception as e:
        return f"❌ Terjadi kesalahan: {e}"

today = datetime.now()
years = [today.year, today.year + 1]
months = list(range(1, 13))
days = list(range(1, 32)) 

with gr.Blocks(title="AstroCuaca") as demo:
    gr.Markdown("## 🔮 ASTROCUACA - Cek Cuaca Jakarta Berdasarkan Tanggal")

    with gr.Row():
        year_input = gr.Dropdown(choices=years, value=years[0], label="Tahun")
        month_input = gr.Dropdown(choices=months, value=today.month, label="Bulan")
        day_input = gr.Dropdown(choices=days, value=today.day, label="Tanggal")

    result = gr.Textbox(label="Hasil", lines=4)
    btn = gr.Button("Cek Cuaca")
    btn.click(fn=get_weather, inputs=[year_input, month_input, day_input], outputs=result)

if __name__ == "__main__":
    demo.launch()