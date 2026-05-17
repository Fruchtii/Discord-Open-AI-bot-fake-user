import json
from discord.ext import commands

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

PROVIDER = config.get('provider', 'openai').lower()

if PROVIDER == 'gemini':
    import google.generativeai as genai
    genai.configure(api_key=config['gemini_api_key'])
    _gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    from openai import OpenAI
    _openai_client = OpenAI(api_key=config['openai_api_key'])


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        prompt = f"{message.author.name}: {message.content}"

        if PROVIDER == 'gemini':
            response = _gemini_model.generate_content(prompt)
            reply = response.text.strip()
        else:
            response = _openai_client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()

        await message.channel.send(reply)


def setup(bot):
    bot.add_cog(Chat(bot))
