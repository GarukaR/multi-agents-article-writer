import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, LLM

# 1. Load the environment variables from your .env file
load_dotenv()

# 2. Define the Claude model configuration
llm = LLM(
    model="anthropic/claude-sonnet-4-6",  # <-- add the prefix
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=8192
)

# 2. Define Modern Agents (With Claude LLM attached)
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory=(
        "You're working on planning a blog article about the topic: {topic}. "
        "You collect information that helps the audience learn something "
        "and make informed decisions."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm 
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion pieces about the topic: {topic}",
    backstory=(
        "You're working on writing a new opinion piece about the topic: {topic}. "
        "You base your writing on the outline provided by the Content Planner."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm 
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory=(
        "You are an editor who receives a blog post from the Content Writer. "
        "Your goal is to ensure it follows journalistic best practices."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm 
)

# 3. Define Tasks
plan = Task(
    description=(
        "1. Prioritize the latest trends and noteworthy news on {topic}.\n"
        "2. Identify the target audience and their pain points.\n"
        "3. Develop a detailed content outline."
    ),
    expected_output="A comprehensive content plan document with an outline and audience analysis.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Ensure the post is structured beautifully in markdown format."
    ),
    expected_output="A well-written blog post in markdown format ready for publication.",
    agent=writer,
)

edit = Task(
    description="Proofread the given blog post for grammatical errors and brand alignment.",
    expected_output="A polished blog post in markdown format.",
    agent=editor
)

# 4. Form the Crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True 
)

# 5. Kickoff the modern workflow
result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})

print("\n\n########################")
print("## CRUISE EXECUTION COMPLETE ##")
print("########################\n")
print(result)

# Save the final article to a markdown file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\nArticle saved to output.md")