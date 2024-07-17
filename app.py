from crewai import Agent, Task, Crew, Process
from tool.twitter import *
from tool.exa_search import *
from langchain_openai import ChatOpenAI
import os
from decouple import config


# Creating a research agent with ExaTool

exa_tool = search_and_get_contents_tool
twitter_tool = tweet

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")


gpt = ChatOpenAI(model_name="gpt-4o", temperature=0.9)

research_agent = Agent(
    role='Researcher',
    goal='Conduct research using Exa',
    tools=[exa_tool],
    backstory='A diligent researcher using Exa for detailed information.',
    llm = gpt
)

tweet_agent = Agent(
    role='Tweet Creator',   
    goal='Create and post tweets based on research, To increase engagement of the account and to teach users latest trends in AI',
    tools=[twitter_tool],
    backstory='A creative writer who can craft engaging tweets based on the latest research.',
    llm = gpt
)



# Research task
research_task = Task(
    description="""Use Exa to research the latest trends in AI. 
    Research should be latest (One day day), should be related to Companies, fundings, academic papers, influential personnels
    Research should be helpful for anyone who wants to stay updated and survive in this age of AI
    """,
    expected_output="A summary of the latest trends in AI.",
    agent=research_agent
)

# Tweet task
tweet_task = Task(
    description="""
    Create a tweet based on the research and post it on Twitter.
    You have acces to twitter tool which can post on twitter
    Ensure the character limit is 280 characters
    """,
    expected_output="""
    A tweet posted using the tool summarizing the latest trends in AI. 
    Ensure the character limit is 280 characters
    
    <Example>
    Expected formated:Top stories in AI today:
    -AI breakthrough improves Alzheimer's predictions
    -YouTube Music gets new AI features
    -Generate beautiful presentations with AI
    -Microsoft gives AI a spreadsheet boost
    -6 new AI tools & 4 new AI jobs
    </Example>
    """,
    agent=tweet_agent,
    context=[research_task]
)

# Forming the crew
crew = Crew(
    agents=[research_agent, tweet_agent],
    tasks=[research_task, tweet_task],
    process=Process.sequential  # Ensuring tasks are executed in sequence
)

# Kick off the crew with the input topic
import time

while True:
  # Execute the desired line
  result = crew.kickoff(inputs={'topic': 'latest technology trends'})
  
  # Wait for 2 hours (2 hours * 60 minutes/hour * 60 seconds/minute)
  time.sleep(2 * 60 * 60)
