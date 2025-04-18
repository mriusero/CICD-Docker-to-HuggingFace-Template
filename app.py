# Streamlit
from src.frontend.layout import app_layout

def main():
    """
    Main function to run the streamlit app.
    """
    app_layout()

if __name__ == "__main__":
    main()

# --------------------------------------
# Gradio
import gradio as gr

def greet(name):
    return f"Hello {name}!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=name, outputs=output)

if __name__ == "__main__":
    demo.launch()