# BlogAgent ✍️

An AI agent that researches, plans, and writes complete blog posts on any topic using LangGraph + Groq.

---

## What it does

You drop a topic. BlogAgent takes care of everything else:

1. **Router** — decides if the topic needs web research or can be written from model knowledge
2. **Research** — searches the web via Tavily and gathers real evidence
3. **Planner** — structures the blog into sections with goals, bullets, and word targets
4. **Writers** — writes all sections in parallel (one LangGraph worker per section)
5. **Assembler** — stitches sections into a final blog and exports a `.docx` file

---

## Tech Stack

| Layer | Tools |
|---|---|
| Orchestration | LangGraph |
| LLMs | Groq (Llama 3.1 8B, Llama 3.3 70B) |
| Web Search | Tavily |
| Validation | Pydantic v2 |
| UI | Streamlit |
| Export | python-docx |

---

## Pipeline Architecture

```
START
  └── Router
        ├── (needs research) → Research → Orchestrator
        └── (no research)   → Orchestrator
                                  └── Fan-out → [Worker] [Worker] [Worker] ...
                                                        └── Reducer → END
```

The fan-out is the core idea — each blog section is written by a separate LangGraph `Send()` worker running in parallel, then reduced into one final document.

---

## Project Structure

```
BlogAgent/
├── bwa_backend.py      # LangGraph graph, nodes, state, Pydantic models
├── bwa_frontend.py     # Streamlit UI
├── blogs/              # Generated .docx files saved here
├── .env                # API keys (not committed)
└── requirements.txt
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/parmarjaimin3884/BlogAgent.git
cd BlogAgent
```

**2. Create and activate a virtual environment**
```bash
python -m venv myenv
myenv\Scripts\activate        # Windows
source myenv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API keys**

Create a `.env` file in the root:
```
GROQ_API=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**5. Run the app**
```bash
python -m streamlit run bwa_frontend.py
```

---

## Requirements

```
langchain
langchain-groq
langchain-community
langgraph
tavily-python
streamlit
pydantic
python-docx
python-dotenv
json-repair
```

---

## Key Concepts Demonstrated

- **LangGraph `Send()` API** for dynamic parallel fan-out
- **Pydantic v2** for structured LLM output validation and auto-repair
- **Conditional routing** with `add_conditional_edges`
- **State schema design** with `Annotated` reducers
- **Multi-model pipeline** — routing on a small fast model, planning and writing on a larger one
