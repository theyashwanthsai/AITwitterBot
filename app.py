import os
import time

from crewai import Agent, Crew, Process, Task
from decouple import config
from langchain_openai import ChatOpenAI

from tool.exa_search import *
from twitter import *
from tool.image_gen import *
# from flask import Flask

# Creating a research agent with ExaTool
exa_tool = search_and_get_contents_tool
twitter_tool = tweet
img_tool = path_of_image

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

gpt = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.9)


# Research Agent
research_agent = Agent(
    role="Researcher",
    goal="Conduct research using Exa to find top AI news from Reddit and Hackernews",
    tools=[exa_tool],
    backstory="A researcher who uses Exa for finding detailed information on the latest AI news.",
    llm=gpt,
)

# Research Task
research_task = Task(
    description="""Use Exa to research the top AI news. Search from Reddit and Hackernews.
    Focus on news that are innovative, trending, and have practical applications.
    Research thoroughly to find the most relevant news.
    """,
    expected_output="""A key note of the top AI news.
    Format:
    - News title
    - Brief description
    - Why it's interesting or innovative
    - Source (Reddit link or Hackernews link)
    """,
    agent=research_agent,
)

# Image Generator Agent
image_generator_agent = Agent(
  role="Image Generator",
  goal="""Generate images based on the research done by the researcher agent. Aim to make it visually appealing and relevant to the research.""",
  tools=[img_tool],
  backstory="An artist who can create visually appealing images based on research.",
  llm=gpt,
)

# Image Generation Task
image_generation_task = Task(
  description="""Generate an image using a prompt. The prompt should have these keywords, add more according to your feelings: "classical, retro, oil painting style, 80s style painting, dystopian world".""",
  expected_output="A visually appealing image relevant to the research.",
  agent=image_generator_agent,
)

# Tweet Agent
tweet_agent = Agent(
  role="Tweet Creator",
  goal="""Create engaging and visually appealing SEO Optimized tweets based on the research done by the researcher agent. Ensure the character limit is 280 characters.""",
  tools=[twitter_tool],
  backstory="A social media expert who crafts engaging tweets based on research.",
  llm=gpt,
)

# Tweet Task
tweet_task = Task(
  description="""Create a tweet based on the work done by the researcher agent. The tweet should be engaging, SEO optimized, and within the 280 character limit. Include relevant hashtags and a link to the source.""",
  expected_output="""An engaging tweet with strict limit 280 letters:
  - Top 3 Bullet point summary of the latest news in AI
  - Make the tweet sound like human and less like AI.
  """,
  agent=tweet_agent,
)




# Forming the crew
crew = Crew(
    agents=[research_agent, image_generator_agent, tweet_agent],
    tasks=[research_task, image_generation_task, tweet_task],
    process=Process.sequential,
    # planning=True,
    # memory=True
    # Ensuring tasks are executed in sequence
)


def start_crew():
    # while True:
        # Execute the desired line
    result = crew.kickoff(inputs={"topic": "LLMs, AI, Agents, Crewai, llamaindex, langchain, claude."})
    print(result)
    # tweet(result)
        # Wait for 2 hours (2 hours * 60 minutes/hour * 60 seconds/minute)
        # time.sleep(60)



start_crew()



