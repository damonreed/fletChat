import flet as ft
from openai import OpenAI
from time import sleep
import requests

client = OpenAI()

# Set the width of the UI elements
WIDTH = 600

# Set the initial text for the UI elements
SYSTEM_INIT = "You are a very senior network engineer of the type that posts to \
twitter repeatedly. You are sarcastic, ironic, and cynical.  \
You try to be original, and avoid cliches. \
You like to very occasionally make obscure and subtle references to nerd culture going back to the 70s.  \
You use a lot of terms from the Hacker's Dictionary and the Scary Devil Monastery."
USER_INIT = (
    "A junior engineer has asked you to explain the difference between IPv4 and IPv6."
)
MEMESTER_ROLE = "You are a meme creator. You frequent 4chan, reddit, and Know Your Meme. Your favorite memes are Bad Luck Brian and Borat."


def main(page: ft.Page):
    page.scroll.value = ScrollMode.AUTO

    # Function to handle button click
    def submit_click(e):
        # Form Text Response to user
        status_text.value = "Working on chat response"
        status_text.update()
        sleep(1)

        # Generate the response
        response = (
            client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_role.value},
                    {"role": "user", "content": user_role.value},
                ],
            )
            .choices[0]
            .message.content
        )
        # response = "This is a test response"
        # status_text.value = "Working on image prompt"
        # status_text.update()

        # Populate the text response
        response_text.value = response
        response_text.update()
        sleep(1)

        # Use the response to generate an image prompt
        # image_prompt = (
        #     client.chat.completions.create(
        #         model="gpt-4",
        #         messages=[
        #             {"role": "system", "content": MEMESTER_ROLE},
        #             {
        #                 "role": "user",
        #                 "content": f"Create a meme from the following reply: {response}",
        #             },
        #         ],
        #     )
        #     .choices[0]
        #     .text
        # )
        image_prompt = "This is a test image prompt"

        meme_prompt.value = image_prompt
        meme_prompt.update()

        status_text.value = "Working on image prompt"
        status_text.update()
        sleep(1)

        # Use the image prompt to generate an image
        # response_image.src = (
        #     client.images.create(
        #         images=image_prompt,
        #         captions=[response_text.value],
        #         max_tokens=64,
        #     )
        #     .data[0]
        #     .image_url
        # )
        # response_image.update()

        # Get random meme from API at https://api.imgflip.com/get_memes
        random_img_response = requests.get(url="https://random.imagecdn.app/500/150")
        response_image.src = random_img_response.url
        response_image.update()
        sleep(1)

        status_text.value = "Awaiting input"

    # Create UI elements
    system_role = ft.TextField(
        label="Context",
        value=SYSTEM_INIT,
        width=WIDTH,
        multiline=True,
        min_lines=5,
        max_lines=5,
        on_submit=submit_click,
    )
    user_role = ft.TextField(
        label="Prompt",
        value=USER_INIT,
        width=WIDTH,
        multiline=True,
        min_lines=5,
        max_lines=5,
        on_submit=submit_click,
    )
    submit_button = ft.OutlinedButton(text="Submit", on_click=submit_click)
    status_text = ft.Text(value="Awaiting input", width=WIDTH)
    response_text = ft.Text(value="Awaiting input", width=WIDTH)
    meme_prompt = ft.Text(value="Awaiting input", width=WIDTH)
    response_image = ft.Image(src="https://i.imgflip.com/6nlb4g.jpg", width=WIDTH)

    # Add elements to the page
    page.add(
        system_role,
        user_role,
        submit_button,
        status_text,
        response_text,
        meme_prompt,
        response_image,
    )


ft.app(target=main, port=8550, view=ft.AppView.FLET_APP_WEB)
