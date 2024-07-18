import os
import time

from crewai import Agent, Crew, Process, Task
from decouple import config
from langchain_openai import ChatOpenAI

from tool.exa_search import *
from tool.twitter import *
from flask import Flask

# Creating a research agent with ExaTool
exa_tool = search_and_get_contents_tool
twitter_tool = tweet

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

gpt = ChatOpenAI(model_name="gpt-4o", temperature=0.9)

research_agent = Agent(
    role="Researcher",
    goal="Conduct research using Exa",
    tools=[exa_tool],
    backstory="A diligent researcher using Exa for detailed information.",
    llm=gpt,
)

tweet_agent = Agent(
    role="Tweet Creator",
    goal="""
    Create and post tweets based on research to increase engagement of the account and to teach users AI
    """,
    tools=[twitter_tool],
    backstory="A creative writer who can craft engaging tweets based on the latest research.",
    llm=gpt,
)

# Research task
research_task = Task(
    description="""Use Exa to research the latest trends in AI/LLM/AI Agents. 
    Research should be latest (past week), Should be about AI news.
    Research should be helpful for anyone who wants to stay updated and survive in this age of AI/LLM/AI Agents
    """,
    expected_output="""A key summary of the latest news in AI/LLM/AI Agents.
    Should include:
    - One line about an Influential Person in AI
    - Latest AI companies fundings
    - Latest AI research
    """,
    agent=research_agent,
)

# Tweet task
tweet_task = Task(
    description="""
    Create a tweet based on the research and post it on Twitter.
    You have access to twitter tool which can post on twitter
    Ensure the character limit is 280 characters
    """,
    expected_output="""
    A tweet posted using the tool summarizing the latest trends in AI/LLMs/AI Agents. 
    Ensure the character limit is 280 characters

    <Example Tweet>
    Expected formatted:
    Hook to engage audience
    bullet point summary (Around 3-4)
    </Example Tweet>

    Important: Tweet is posted using the tweet function tool. 
    The tool takes an argument content which is basically the tweet content. 
    Pass the content before using the tool. Very important!
    """,
    agent=tweet_agent,
    context=[research_task],
)

# Forming the crew
crew = Crew(
    agents=[research_agent, tweet_agent],
    tasks=[research_task, tweet_task],
    process=Process.sequential,  # Ensuring tasks are executed in sequence
)


def start_crew():
    # while True:
        # Execute the desired line
    result = crew.kickoff(inputs={"topic": "latest AI/LLM/AI Agents trends"})
    print(result)
        # Wait for 2 hours (2 hours * 60 minutes/hour * 60 seconds/minute)
        # time.sleep(60)



start_crew()



