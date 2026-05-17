import json
import discord
from discord.ext import commands

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

PROVIDER = config.get('provider', 'openai').lower()

if PROVIDER == 'gemini':
    import google.generativeai as genai
    genai.configure(api_key=config['gemini_api_key'])
    ai_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    from openai import OpenAI
    openai_client = OpenAI(api_key=config['openai_api_key'])

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store conversation history for each channel
conversation_history = {}


def get_ai_response(messages):
    if PROVIDER == 'gemini':
        # Convert OpenAI-style messages to Gemini history format
        gemini_history = []
        system_prompt = None
        for msg in messages:
            if msg['role'] == 'system':
                system_prompt = msg['content']
                continue
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': [msg['content']]})

        # Last message is the new user turn; rest is history
        if not gemini_history:
            return "I couldn't process that message."

        history = gemini_history[:-1]
        last_message = gemini_history[-1]['parts'][0]

        chat = ai_model.start_chat(history=history)
        # Prepend system prompt to first user turn if present
        prompt = f"{system_prompt}\n\n{last_message}" if system_prompt and not history else last_message
        response = chat.send_message(prompt)
        return response.text.strip()
    else:
        response = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        return response.choices[0].message.content.strip()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! (provider: {PROVIDER})')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.content.startswith(bot.command_prefix):
        return

    if message.channel.id not in conversation_history:
        conversation_history[message.channel.id] = []

    conversation_history[message.channel.id].append(
        {"role": "user", "content": f"{message.author.name}: {message.content}"}
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ] + conversation_history[message.channel.id][-10:]

    assistant_reply = get_ai_response(messages)

    conversation_history[message.channel.id].append(
        {"role": "assistant", "content": assistant_reply}
    )

    await message.channel.send(assistant_reply)


@bot.command(name='reset')
async def reset_memory(ctx):
    """Reset the bot's memory for the current channel."""
    channel_id = ctx.channel.id
    if channel_id in conversation_history:
        conversation_history[channel_id] = []
        await ctx.send("Memory has been reset for this channel.")
    else:
        await ctx.send("There was no conversation history to reset in this channel.")


bot.run(config['discord_token'])
