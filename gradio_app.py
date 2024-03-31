import gradio as gr
from transformers import pipeline
import numpy as np

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-medium.en")

def transcribe(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    return transcriber({"sampling_rate": sr, "raw": y})["text"]


import gradio as gr

def greet(name, intensity,audio):
    #return audio
    return transcribe(audio)
    # print(type(audio))
    # return "Hello, " + name + "!" * intensity

demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.Slider(value=2, minimum=1, maximum=10, step=1),"audio"],
    outputs=[gr.Textbox(label="greeting", lines=10)],
)

if __name__ == "__main__":
    demo.launch(debug = True)
