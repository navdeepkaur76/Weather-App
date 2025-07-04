import gradio as gr
import requests
import plotly.graph_objects as go

API_KEY = "03f6d152c684f1bea5891f52499dd692"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return f"City '{city}' not found!", None
    data = res.json()

    weather_info = {
        "City": data["name"],
        "Temperature(°C)": data["main"]["temp"],
        "Humidity(%)": data["main"]["humidity"],
        "Pressure(hPa)": data["main"]["pressure"],
        "Weather": data["weather"][0]["description"].title(),
        "Wind Speed(m/s)": data["wind"]["speed"]
    }

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[
            weather_info["Temperature(°C)"],
            weather_info["Humidity(%)"],
            weather_info["Pressure(hPa)"] / 10,
            weather_info["Wind Speed(m/s)"]
        ],
        theta=["Temp", "Humidity", "Pressure/10", "Wind Speed"],
        fill='toself',
        name="Weather Stats"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title=f"Weather Radar: {city}"
    )

    report = "\n".join(f"{k}: {v}" for k, v in weather_info.items())
    return report, fig

with gr.Blocks(title="Weather Report App") as demo:
    gr.Markdown("Enter City Name to Get Weather Report")
    city_input = gr.Textbox(label="Enter City", placeholder="e.g. Delhi, New York, Tokyo")
    output_text = gr.Textbox(label="Weather Report", lines=8)
    output_chart = gr.Plot(label="Weather Radar Chart")
    submit = gr.Button("Get Weather")
    submit.click(fn=get_weather, inputs=city_input, outputs=[output_text, output_chart])
    demo.launch(share=True)
