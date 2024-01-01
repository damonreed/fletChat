import flet as ft

from openai import OpenAI

client = OpenAI()

# Set the width of the UI elements
WIDTH = 600

# Set the initial text for the UI elements
SYSTEM_INIT = """
  You are a very senior network engineer of the type that posts to twitter repeatedly.  
  You are sarcastic, ironic, and cynical.  You try to be original, and avoid cliches.
  You like to very occasionally make obscure and subtle references to nerd culture going back to the 70s.
  You use a lot of terms from the Hacker's Dictionary and the Scary Devil Monastery.
  """
USER_INIT = """
  A junior engineer has asked you to explain the difference between IPv4 and IPv6.
  """


def main(page: ft.Page):
    # Function to handle button click
    def submit_click(e):
        # Process the input (you can replace this with your logic)
        response = f"Input 1: {text_input1.value}, Input 2: {text_input2.value}"
        response_text.value = response

        # For the image, you'd generate or retrieve it here. This is just a placeholder
        response_image.src = "path_to_your_image.jpg"

        page.update()

    # Create UI elements
    text_input1 = ft.TextField(label=SYSTEM_INIT, width=WIDTH, on_submit=submit_click)
    text_input2 = ft.TextField(label=USER_INIT, width=WIDTH, on_submit=submit_click)
    submit_button = ft.TextButton(text="Submit", on_click=submit_click)
    response_text = ft.Text(value="Awaiting input", width=WIDTH)
    response_image = ft.Image(src="https://i.imgflip.com/6nlb4g.jpg", width=WIDTH)

    # Add elements to the page
    page.add(text_input1, text_input2, submit_button, response_text, response_image)


ft.app(target=main, port=8550, view=ft.AppView.FLET_APP_WEB)
