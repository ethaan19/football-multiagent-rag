# ⚽ Football RAG Multiagent

Multi-agent RAG system for European football analysis, built with LangGraph, FastAPI, and Azure OpenAI.

---

## 📋 General Description

**Football RAG Multiagent** is an intelligent system that combines:
- **RAG (Retrieval-Augmented Generation):** Retrieves relevant information from a knowledge base and uses it to generate precise responses.
- **Multi-agent Architecture:** 5 specialized agents working together to answer complex queries.
- **Semantic Search:** Uses vector embeddings to find relevant information.

The system allows queries in **natural language** about the 5 major European football leagues and provides detailed, contextualized, and updated answers.

---

## 🧠 How does a RAG work?

A RAG system has two phases:

### 1. **Retrieval Phase**
- Converts the question into a numerical vector (embedding).
- Searches ChromaDB for the most semantically similar documents.
- Retrieves the relevant context.

### 2. **Generation Phase**
- Sends the question + the retrieved context to the LLM (GPT-4o-mini).
- The LLM generates a coherent response based on real context.
- Does not rely solely on its training knowledge.

**Advantage:** Responses are based on real, up-to-date data, rather than old training information from the model.

---

## 💡 What is this system for?

1. **Performance Analysis:** "How is Real Madrid playing?"
2. **Tactical Analysis:** "How does Bayern Munich play?"
3. **Player Information:** "What players does Arsenal have?"
4. **Comparisons:** "What is the difference between Barça and Atlético?"
5. **General Information:** "Who is leading the Premier League?"

---

## 📚 What knowledge does the system have?

The system has access to **3 knowledge sources** regarding the 5 major leagues:

### 1. **Team Statistics (Standings)**
- Current position in the league.
- Matches played, wins, draws, losses.
- Goals for and against.
- Goal difference.
- Total points.
- **Source:** Free API Live Football Data (RapidAPI) - in real time.

### 2. **Player Information**
- Name, age, nationality.
- Position (goalkeeper, defender, midfielder, forward).
- Rating/qualification.
- Goals and assists.
- Current team and league.
- **Source:** Free API Live Football Data (RapidAPI) - real and updated data.

### 3. **Tactical Analysis**
- Typical team formation (4-3-3, 4-2-3-1, 5-3-2, etc.).
- Play style (possession-based, counter-attack, low block/closed defense).
- Characteristics (fluid attack, solid defense, leaders, consistent).
- Strengths and weaknesses.
- **Source:** Automatically generated from real statistics.

### Coverage:
> ⚠️ The system covers the **top 4 teams of each league** in the current season (20 teams in total).

| League | Country | Teams Covered |
|------|------|-------------------|
| 🇪🇸 La Liga | Spain | Top 4 |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | England | Top 4 |
| 🇩🇪 Bundesliga | Germany | Top 4 |
| 🇮🇹 Serie A | Italy | Top 4 |
| 🇫🇷 Ligue 1 | France | Top 4 |

---

## 🤖 Multi-agent Architecture

The system uses **5 specialized agents** orchestrated by LangGraph:

```
User Query
    ↓
[Router Agent]
Analyzes the intent and decides which agents to invoke
    ↓
┌────────────────────────────────────────────────┐
│ [Performance] → [Tactical] → [Players]         │
│ → [Comparative] (sequential)                   │
│ Only execute if selected by the router         │
└────────────────────────────────────────────────┘
    ↓
[Consolidator]
Merges all answers into a final response
    ↓
Coherent response to the user
```

### How each agent works:

#### **1. Router Agent**
- **Function:** Analyzes the question and decides which agents should answer it.
- **Process:**
  1. Receives the user's question.
  2. Sends it to GPT-4o-mini with a specific prompt.
  3. The LLM responds with JSON: `{"agents": ["performance", "tactical"]}`.
  4. Updates the state with the agents to invoke.
- **Example:** "How does Bayern play?" → router decides: `["tactical"]`

#### **2. Performance Agent**
- **Specialty:** Team statistics and performance.
- **Process:**
  1. Receives the question.
  2. Converts the question into an embedding (vector).
  3. Searches ChromaDB `teams` collection for the 10 most similar teams.
  4. Retrieves context (standings, points, goals).
  5. Sends the question + context to the LLM.
  6. The LLM generates the performance analysis.
- **Example:** "How many points does Madrid have?" → searches `teams` → responds with statistics.

#### **3. Tactical Agent**
- **Specialty:** Tactical analysis, formations, play styles.
- **Process:**
  1. Receives the question.
  2. Converts it into an embedding.
  3. Searches ChromaDB `tactical` collection for the 10 most similar profiles.
  4. Retrieves: formation, playstyle, characteristics, strengths/weaknesses.
  5. Sends the question + tactical context to the LLM.
  6. The LLM generates a detailed tactical analysis.
- **Example:** "How does Barcelona play?" → searches `tactical` → responds with formation and style analysis.

#### **4. Players Agent**
- **Specialty:** Player information and squads.
- **Process:**
  1. Receives the question.
  2. Converts it into an embedding.
  3. Searches ChromaDB `players` collection for the 10 most similar players.
  4. Retrieves: name, age, position, nationality, rating, goals, assists.
  5. Sends the question + player data to the LLM.
  6. The LLM organizes and presents the information.
- **Example:** "What players does Arsenal have?" → searches `players` → lists players organized by position.

#### **5. Comparative Agent**
- **Specialty:** Comparisons between teams or players.
- **Process:**
  1. Receives the question.
  2. Converts it into an embedding.
  3. Searches **all 3 collections** (teams, players, tactical) simultaneously.
  4. Retrieves data for both entities to be compared.
  5. Sends the question + data of both teams/players to the LLM.
  6. The LLM generates a structured comparative analysis.
- **Example:** "PSG vs Barcelona?" → searches the 3 collections → compares standings, tactics, players.

#### **6. Consolidator**
- **Function:** Merges the answers of all agents into a single coherent response.
- **Process:**
  1. If only 1 agent responded → returns its direct response.
  2. If multiple agents responded → sends all answers to the LLM.
  3. The LLM merges them, eliminating redundancies.
  4. Generates a final cohesive response.
- **Example:** If Performance + Tactical responded → consolidator merges them intelligently.

---

## 📊 Example Data Flow

**Question:** "How is Real Madrid playing this season?"

```
1. Router Agent
   ↓ Analyzes the question
   ↓ Decides: ["performance", "tactical"]
   
2. Performance Agent (parallel)
   ↓ Embeds the question
   ↓ Searches ChromaDB "teams"
   ↓ Retrieves: Madrid 86 points, 2nd place, 77 goals...
   ↓ LLM generates: "Real Madrid is in 2nd place with 86 points..."
   
3. Tactical Agent (parallel)
   ↓ Embeds the question
   ↓ Searches ChromaDB "tactical"
   ↓ Retrieves: 4-3-3 formation, possession-based, fluid attack...
   ↓ LLM generates: "Tactically plays in 4-3-3 with possession dominance..."
   
4. Consolidator
   ↓ Receives answers from Performance + Tactical
   ↓ LLM merges them intelligently
   ↓ Final response: "Real Madrid is in 2nd place... Tactically..."
   
5. API returns response to the user
```

---

## 🛠️ Technology Stack

| Component | Technology | Function |
|-----------|-----------|---------|
| **Orchestration** | LangGraph | Connects agents, handles flows |
| **REST API** | FastAPI | Exposes HTTP endpoints |
| **LLM** | GPT-4o-mini (Azure) | Generates intelligent responses |
| **Embeddings** | text-embedding-3-small (Azure) | Converts text to vectors |
| **Vector DB** | ChromaDB | Stores and searches embeddings |
| **Data** | Free API Live Football Data | Real-time API |
| **Language** | Python 3.11+ | Implementation |

---

## 📁 Project Structure

```
football-rag/
├── agents/                   # Specialized agents
│   ├── router_agent.py       # Decides which agents to invoke
│   ├── performance_agent.py  # Performance analysis
│   ├── tactical_agent.py     # Tactical analysis
│   ├── players_agent.py      # Player information
│   └── comparative_agent.py  # Comparisons
├── graph/
│   ├── state.py              # Shared state between agents
│   └── main_graph.py         # Orchestration with LangGraph
├── api/
│   └── main.py               # FastAPI endpoints
├── config/
│   └── constants.py          # Leagues, tactical data
├── data/                     # Knowledge base (auto-generated)
│   ├── teams_data.json
│   ├── players_data.json
│   └── tactical_data.json
├── chroma_db/                # Vector database (auto-generated)
├── fetch_football_data.py    # Script: fetches data from API
├── embed_and_upload.py       # Script: generates embeddings
├── index.html                # Web interface
├── .env.example              # Credentials template
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🚀 Installation and Usage (Local)

### 1. Clone the repository

```bash
git clone https://github.com/ethann-19/ia-gen
cd multiagent-rag
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env`:

```env
RAPIDAPI_KEY=your_rapidapi_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

### 4. Start the API

```bash
uvicorn api.main:app --reload
```

### 5. Open interface

Open `index.html` in your browser.

---

## 💬 Sample Questions

```
How is Real Madrid performing this season?
What players does Arsenal have?
How does Bayern Munich play tactically?
Compare PSG with Olympique de Marseille
What is the tactical difference between Barça and Atlético?
Which team is leading the Premier League?
```

---

## ⚠️ Limitations

- Covers only the **top 4 teams of each league** (20 teams)
- Tactical data is automatically generated (approximated)
- RapidAPI has daily request limits on the free plan

---
