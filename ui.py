import gradio as gr

from lib import estimate


def main_ui():
    with (gr.Row()):
        with gr.Column(scale=1, min_width=1):
            ...
        with gr.Column(scale=10):
            header = gr.Image(
                "data/Zeppelin_combined.png",
                label="Zeppelin machines overview",
                interactive=False,
                show_download_button=False,
                show_label=False
            )
        with gr.Column(scale=1, min_width=1):
            ...
    with (gr.Row()):
        with gr.Column(scale=1):
            brand = gr.Dropdown(
                label="Brand",
                choices=["Caterpillar"],
                value="Caterpillar",
                info="Brand of the construction machine."
            )
            model = gr.Dropdown(
                label="Model",
                choices=["308"],
                value="308",
                info="Model of the construction machine."
            )
            series = gr.Dropdown(
                label="Series",
                choices=["C", "D", "E", "E2"],
                value="C",
                info="The series of the construction machine."
            )
            cr = gr.Dropdown(
                label="CR",
                choices=[0, 1],
                value=1,
                info="CR."
            )
            location = gr.Dropdown(
                label="Location",
                choices=[
                    "FI", "PL", "GB", "IT", "FR", "DE", "NL", "CH", "AT",
                    "SE", "ES", "IE", "RO", "GE", "SK", "EE", "LT", "NO",
                    "UA", "LV", "CZ", "SI", "BE"
                ],
                value="DE",
                info="The country the construction machine is located."
            )
            working_hours = gr.Number(
                label="Working hours",
                minimum=1,
                value=1000,
                maximum=100000,
                info="The number of working hours the machine was used."
            )

            year = gr.Number(
                label="Year",
                minimum=2007,
                value=2011,
                maximum=2024,
                info="The year the construction machine was build."
            )
        with gr.Column(scale=1):
            ...
    with gr.Row():
        with gr.Column():
            ...
        with gr.Column():
            ...
        with gr.Column():
            ...
        with gr.Column():
            button = gr.Button(value="start")
    with gr.Row():
        with gr.Column():
            estimated_price = gr.Textbox(label="Estimated price", interactive=False)
        with gr.Column():
            ...
        with gr.Column():
            ...
        with gr.Column():
            ...

    @button.click(inputs=[series, cr, location, working_hours, year], outputs=estimated_price)
    def on_click(series, cr, location, working_hours, year):
        try:
            estimated_price = str(estimate(series, cr, location, working_hours, year))
        except Exception as _:
            estimated_price = "No valid estimation could be calculated."
        return estimated_price
