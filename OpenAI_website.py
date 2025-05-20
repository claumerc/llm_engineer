openai = OpenAI()

# COMMAND ----------
message = "Hello, GPT! This is my first ever message to you! Hi!"
response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
print(response.choices[0].message.content)

# COMMAND ----------
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# COMMAND ----------
ed = Website("https://www.linkedin.com/in/claudiomercante/")
print(ed.title)
print(ed.text)

# COMMAND ----------
# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."
system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

# COMMAND ----------
# To give you a preview -- calling OpenAI with system and user messages:
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
print(response.choices[0].message.content)

# COMMAND ----------
# See how this function creates exactly the format above
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# COMMAND ----------
# And now: call the OpenAI API. You will get very familiar with this!
def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

# COMMAND ----------
# A function to display this nicely in the Jupyter output, using markdown
def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# COMMAND ----------
display_summary("https://www.linkedin.com/in/claudiomercante")