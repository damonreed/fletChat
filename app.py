import flet as ft
from openai import OpenAI
from time import sleep
import requests
import os

## Static Variables

# Set the width of the UI elements
WIDTH = 600

# Set the initial text for the UI elements
SYSTEM_INIT = "You are a very senior network engineer of the type that posts to twitter repeatedly.\
You are sarcastic, ironic, and cynical.  \
You try to be original, and avoid cliches. \
You like to very occasionally make obscure and subtle references to nerd culture going back to the 70s.  \
You use a lot of terms from the Hacker's Dictionary and the Scary Devil Monastery."
USER_INIT = (
    "A junior engineer has asked you to explain the difference between IPv4 and IPv6."
)
MEMESTER_ROLE = "You are a meme creator. You frequent 4chan, reddit, and Know Your Meme. Your favorite memes are Bad Luck Brian and Borat."

## Objects

client = OpenAI()


## Functions
def get_random_meme():
    # Set params for API call- get key from environment variable
    params = {"q": "neteng", "api_key": os.environ.get("GIPHY_API_KEY"), "limit": "1"}

    # Get random gif from API at https://developers.giphy.com/docs/api/endpoint#random
    response = requests.get(url="https://api.giphy.com/v1/gifs/random", params=params)

    # Print json p of response
    print(response.json())

    # Return the URL of the random gif
    return response.url


def main(page: ft.Page):
    # Function to handle submit calls
    def submit_click(e):
        # Form Text Response to user
        status_text.value = "Working on chat response"
        status_text.update()

        # sleep(1)

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

        status_text.value = "Working on image prompt"
        status_text.update()

        # Populate the text response
        response_text.value = response
        response_text.update()

        sleep(1)

        # Use the response to generate an image prompt
        image_prompt = (
            client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": MEMESTER_ROLE},
                    {
                        "role": "user",
                        "content": f"Create a DALL-E image prompt for a meme from the following story: {response}",
                    },
                ],
            )
            .choices[0]
            .text
        )
        # image_prompt = "This is a test image prompt"

        meme_prompt.value = image_prompt
        meme_prompt.update()

        status_text.value = "Working on image generation"
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

        response_image.src = get_random_meme()
        response_image.update()
        sleep(1)

        status_text.value = "Ready for input"

    ## Functional Controls

    # Create Context UI element for system_role prompt input
    system_role = ft.TextField(
        label="Context",
        value=SYSTEM_INIT,
        width=WIDTH,
        multiline=True,
        min_lines=5,
        max_lines=5,
        on_submit=submit_click,
    )

    # Create Prompt UI element for user_role prompt input
    user_role = ft.TextField(
        label="Prompt",
        value=USER_INIT,
        width=WIDTH,
        multiline=True,
        min_lines=5,
        max_lines=5,
        on_submit=submit_click,
    )

    # Submit button to trigger the response
    submit_button = ft.OutlinedButton(text="Submit", on_click=submit_click)

    ## Display Controls

    # Status text to show the user what is happening
    status_text = ft.TextField(value="Ready for input", read_only=True)

    # Response text to show the user the AI response to the user prompt
    response_text = ft.TextField(
        value="Awaiting results",
        read_only=True,
        multiline=True,
        min_lines=5,
    )

    # Meme prompt to show the user the AI generated prompt for the memester output
    meme_prompt = ft.Text(value="Awaiting results", width=WIDTH)

    # Display meme image
    response_image = ft.Image(src=get_random_meme(), width=WIDTH)

    ## Layout Controls

    # Add elements for input and status
    input_column = ft.Column(
        scroll=True,
        controls=[
            system_role,
            user_role,
            submit_button,
            status_text,
        ],
    )

    # Add response elements to the page
    response_column = ft.Column(
        scroll=True,
        controls=[
            response_text,
            meme_prompt,
        ],
    )

    # Add image elements to the page
    image_column = ft.Column(
        scroll=True,
        controls=[
            response_image,
        ],
    )

    # Add the columns to a row
    main_row = ft.Row(controls=[input_column, response_column, image_column])

    page.add(main_row)


ft.app(target=main, port=8550, view=ft.AppView.FLET_APP_WEB)
