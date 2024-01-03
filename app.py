import flet as ft
from openai import OpenAI
from time import sleep
import requests
import os
import json
import base64

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
    "A junior engineer has asked you to explain the difference between IPv4 and IPv6.  Give a very short answer"
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

    # Pretty print the response
    # print(json.dumps(response.json(), indent=4, sort_keys=True))  

    # Return the URL of the random gif
    # return response.json()["data"]["images"]["original"]["url"]
    return "https://i.imgflip.com/6nlb4g.jpg"

# Use requests to download a png url and return a base64 encoded string
def get_base64_image(url):
    # Get the image from the url
    response = requests.get(url)

    # Encode the image as base64
    base64_image = base64.b64encode(response.content).decode("utf-8")

    # Return the base64 encoded image
    return base64_image

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
        print(response)
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
            .message.content
        )
        # image_prompt = "This is a test image prompt"
        print(image_prompt)
        meme_prompt.value = image_prompt
        meme_prompt.update()

        status_text.value = "Working on image generation"
        status_text.update()
        sleep(1)

        # Use the image prompt to generate an image
        gen_image_url = (
            client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
            )
            .data[0]
            .url
        )
        print(gen_image_url)
        image_b64 = get_base64_image(gen_image_url)
        response_image.src = f"data:image/png;base64,{image_b64}"
        response_image.update()

        # response_image.src = get_random_meme()
        # response_image.update()
        sleep(1)

        status_text.value = "Ready for input"
    ##
    ## End of submit_click function
    ##
        
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
    response_image = ft.Image(src="https://i.imgflip.com/6nlb4g.jpg", width=WIDTH)

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
