import asyncio
import logging
import json  # Import the json module for parsing API responses
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction # Import ChatAction for typing indicator

# Configure logging to see detailed information about the bot's operations.
# This is helpful for debugging.
logging.basicConfig(level=logging.INFO)

# --- IMPORTANT ---
# Replace 'YOUR_BOT_TOKEN_HERE' with your actual Telegram Bot API token.
# You can get a token by talking to BotFather on Telegram.
# Example: TOKEN = "1234567890:ABCDEFGHIJKLMN_OPQRSTUVWXYZabcdefg"
TOKEN = "7851836515:AAE41gcHdU1Fsn25V68ISYYmTNcaiPzlMS8"

# Initialize the Bot instance.
# This object represents your bot and is used to send requests to the Telegram Bot API.
bot = Bot(token=TOKEN)

# Initialize the Dispatcher instance.
# The Dispatcher is responsible for routing updates (messages, callbacks, etc.)
# from Telegram to the appropriate handlers in your code.
dp = Dispatcher()

# Define a handler for the '/start' command.
# The `CommandStart()` filter ensures this function is called only when
# the user sends the `/start` command.
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with the `/start` command.
    It sends a welcome message back to the user.
    """
    await message.answer(f"Hello, {message.from_user.full_name}! Send me a message, and I'll try to respond with AI!")

# Define a handler for all other text messages.
# This function will now send the message to an AI model and respond with its output.
@dp.message()
async def ai_response_handler(message: types.Message) -> None:
    """
    This handler receives any text message, sends it to the Gemini API for AI generation,
    and then sends the AI's response back to the user.
    """
    if message.text:
        prompt = message.text
        chat_history = []
        chat_history.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {"contents": chat_history}
        apiKey = "" # Leave this as-is; Canvas will provide the API key at runtime.
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apiKey}"

        try:
            # Send a "typing..." action to indicate that the bot is processing
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

            # Simulate a fetch call (in a real browser/JS environment this would be `fetch`)
            # For Python, we'd typically use `aiohttp` or `httpx`.
            # Since this is a conceptual example for a Canvas environment,
            # we'll represent the fetch call structure.
            # In a real Python bot, you'd use a library like `httpx` or `aiohttp` for HTTP requests.
            # Example with httpx:
            # import httpx
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(apiUrl, json=payload)
            #     result = response.json()

            # --- Mocking the fetch call for demonstration within a Python context ---
            # In a real Python environment, you would use an HTTP client library.
            # For this example, we'll simulate the response structure.
            # You would replace this with actual HTTP request logic.
            # For the purpose of this Canvas environment, the `fetch` concept is implied.

            # Placeholder for actual API call logic:
            # This part needs an actual HTTP client (e.g., aiohttp, httpx) to work in Python.
            # The prompt's instruction about `fetch` is for JS/HTML context.
            # For Python, we'll assume a successful API call and structure the response.

            # To make this runnable in a typical Python environment, you'd need:
            # pip install httpx
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(apiUrl, json=payload, timeout=30) # Added timeout
                response.raise_for_status() # Raise an exception for bad status codes
                result = response.json()

            ai_response_text = "I couldn't get a response from the AI." # Default message

            if result.get("candidates") and len(result["candidates"]) > 0 and \
               result["candidates"][0].get("content") and \
               result["candidates"][0]["content"].get("parts") and \
               len(result["candidates"][0]["content"]["parts"]) > 0:
                ai_response_text = result["candidates"][0]["content"]["parts"][0].get("text", ai_response_text)
            else:
                logging.warning(f"Unexpected API response structure: {json.dumps(result)}")

            await message.answer(ai_response_text)

        except httpx.RequestError as e:
            logging.error(f"HTTP request failed: {e}")
            await message.answer("Sorry, I'm having trouble connecting to the AI right now. Please try again later!")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response: {e}")
            await message.answer("Sorry, I received an invalid response from the AI service.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            await message.answer("An unexpected error occurred while processing your request.")
    else:
        await message.answer("Please send me a text message to get an AI response.")


# The main function to start the bot.
async def main() -> None:
    """
    Starts the bot in polling mode.
    `dp.run_polling()` will continuously check for new updates from Telegram.
    """
    # This line ensures that any pending updates are cleared before the bot starts.
    # This prevents the bot from processing old messages when it's started.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Entry point of the script.
# This ensures that the `main()` function is called when the script is executed.
if __name__ == "__main__":
    asyncio.run(main())
