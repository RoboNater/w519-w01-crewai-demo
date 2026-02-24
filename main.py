import os
import time
import logging
from typing import Any

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler


# ============================================================
# CONFIGURATION
# ============================================================

LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MAX_MODEL_CALLS = int(os.getenv("MAX_MODEL_CALLS", "10"))
PAUSE_FILE = "pause-agents.txt"


# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("crewai-demo")


# ============================================================
# PAUSE / RESUME MECHANISM
# ============================================================

def wait_if_paused():
    while os.path.exists(PAUSE_FILE):
        logger.warning("Execution paused. Waiting for pause file to be removed...")
        time.sleep(5)


# ============================================================
# MODEL CALL TRACKER
# ============================================================

class ModelCallLimiter(BaseCallbackHandler):
    def __init__(self, max_calls: int):
        self.max_calls = max_calls
        self.call_count = 0

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs: Any):
        wait_if_paused()

        self.call_count += 1
        logger.info(f"\n🔵 MODEL CALL #{self.call_count}")
        logger.info("Prompt:")
        for p in prompts:
            logger.info(p)

        if self.call_count > self.max_calls:
            logger.error("❌ Max model call limit reached. Stopping execution.")
            raise RuntimeError("Maximum model calls exceeded.")

    def on_llm_end(self, response, **kwargs: Any):
        logger.info("🟢 MODEL RESPONSE:")
        logger.info(str(response.generations))


# ============================================================
# LLM INITIALIZATION
# ============================================================

callback_handler = ModelCallLimiter(MAX_MODEL_CALLS)

llm = ChatOpenAI(
    model=LLM_MODEL_NAME,
    base_url=LLM_API_BASE,
    api_key=OPENAI_API_KEY,
    temperature=0.7,
    callbacks=[callback_handler],
)


# ============================================================
# AGENTS
# ============================================================

manager = Agent(
    role="Project Manager",
    goal="Break down the objective and delegate work efficiently.",
    backstory="Experienced technical leader coordinating specialists.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
)

researcher = Agent(
    role="Senior Researcher",
    goal="Conduct structured research.",
    backstory="Analytical and detail-oriented expert.",
    verbose=True,
    llm=llm,
)

writer = Agent(
    role="Technical Writer",
    goal="Turn research into structured documentation.",
    backstory="Expert at simplifying complex ideas.",
    verbose=True,
    llm=llm,
)


# ============================================================
# TASK
# ============================================================

task = Task(
    description=(
        "Create a structured report about Multi-Agent AI Systems. "
        "Include architecture overview, benefits, and challenges."
    ),
    expected_output="A well-structured markdown report.",
)


# ============================================================
# CREW
# ============================================================

crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[task],
    process=Process.hierarchical,
    verbose=True,
)


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting hierarchical CrewAI demo...")
        result = crew.kickoff()
        logger.info("\n===== FINAL OUTPUT =====\n")
        print(result)

    except Exception as e:
        logger.error(f"Execution stopped: {e}")
        