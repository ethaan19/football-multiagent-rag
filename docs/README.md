# ⚽ Football RAG Multiagent (Español)

Este documento es una traducción del [README.md](../README.md) original en inglés.

---

Multi-agent RAG system para análisis de fútbol europeo, desarrollado con LangGraph, FastAPI y Azure OpenAI.

---

### **APP:** https://football-multiagent-rag.vercel.app/

---

## 📋 Descripción General

**Football RAG Multiagent** es un sistema inteligente que combina:
- **RAG (Retrieval-Augmented Generation):** Recupera información relevante de una base de conocimiento y la utiliza para generar respuestas precisas.
- **Arquitectura Multi-agente:** 5 agentes especializados que trabajan juntos para responder consultas complejas.
- **Búsqueda Semántica:** Utiliza embeddings vectoriales para encontrar información relevante.

El sistema permite realizar consultas en **lenguaje natural** sobre las 5 grandes ligas de fútbol europeo y proporciona respuestas detalladas, contextualizadas y actualizadas.

---

## 🧠 ¿Cómo funciona un RAG?

Un sistema RAG consta de dos fases:

### 1. **Fase de Recuperación (Retrieval)**
- Convierte la pregunta en un vector numérico (embedding).
- Busca en ChromaDB los documentos semánticamente más similares.
- Recupera el contexto relevante.

### 2. **Fase de Generación (Generation)**
- Envía la pregunta + el contexto recuperado al LLM (GPT-4o-mini).
- El LLM genera una respuesta coherente basada en el contexto real.
- No depende únicamente de su conocimiento de entrenamiento.

**Ventaja:** Las respuestas se basan en datos reales y actualizados, en lugar de información de entrenamiento obsoleta del modelo.

---

## 💡 ¿Para qué sirve este sistema?

1. **Análisis de Rendimiento:** "¿Cómo está jugando el Real Madrid?"
2. **Análisis Táctico:** "¿Cómo juega el Bayern de Múnich?"
3. **Información de Jugadores:** "¿Qué jugadores tiene el Arsenal?"
4. **Comparaciones:** "¿Cuál es la diferencia entre el Barça y el Atlético?"
5. **Información General:** "¿Quién lidera la Premier League?"

---

## 📚 ¿Qué conocimientos tiene el sistema?

El sistema tiene acceso a **3 fuentes de conocimiento** relativas a las 5 grandes ligas:

### 1. **Estadísticas de Equipos (Clasificaciones)**
- Posición actual en la liga.
- Partidos jugados, victorias, empates, derrotas.
- Goles a favor y en contra.
- Diferencia de goles.
- Puntos totales.
- **Fuente:** API gratuita Live Football Data (RapidAPI) - en tiempo real.

### 2. **Información de Jugadores**
- Nombre, edad, nacionalidad.
- Posición (portero, defensa, centrocampista, delantero).
- Calificación/valoración.
- Goles y asistencias.
- Equipo y liga actuales.
- **Fuente:** API gratuita Live Football Data (RapidAPI) - datos reales y actualizados.

### 3. **Análisis Táctico**
- Formación típica del equipo (4-3-3, 4-2-3-1, 5-3-2, etc.).
- Estilo de juego (basado en la posesión, contraataque, bloque bajo/defensa cerrada).
- Características (ataque fluido, defensa sólida, líderes, consistentes).
- Fortalezas y debilidades.
- **Fuente:** Generado automáticamente a partir de estadísticas reales.

### Cobertura:
> ⚠️ El sistema cubre a los **4 mejores equipos de cada liga** en la temporada actual (20 equipos en total).

| Liga | País | Equipos Cubiertos |
|------|------|-------------------|
| 🇪🇸 La Liga | España | Top 4 |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | Inglaterra | Top 4 |
| 🇩🇪 Bundesliga | Alemania | Top 4 |
| 🇮🇹 Serie A | Italia | Top 4 |
| 🇫🇷 Ligue 1 | Francia | Top 4 |

---

## 🤖 Arquitectura Multi-agente

El sistema utiliza **5 agentes especializados** orquestados por LangGraph:

```
Consulta del Usuario
    ↓
[Router Agent]
Analiza la intención y decide qué agentes invocar
    ↓
┌────────────────────────────────────────────────┐
│ [Performance] → [Tactical] → [Players]         │
│ → [Comparative] (secuencial)                   │
│ Solo se ejecutan si son seleccionados por el   │
│ router                                         │
└────────────────────────────────────────────────┘
    ↓
[Consolidator]
Combina todas las respuestas en una respuesta final
    ↓
Respuesta coherente al usuario
```

### Cómo funciona cada agente:

#### **1. Router Agent**
- **Función:** Analiza la pregunta y decide qué agentes deben responderla.
- **Proceso:**
  1. Recibe la pregunta del usuario.
  2. La envía a GPT-4o-mini con un prompt específico.
  3. El LLM responde con un JSON: `{"agents": ["performance", "tactical"]}`.
  4. Actualiza el estado con los agentes a invocar.
- **Ejemplo:** "¿Cómo juega el Bayern?" → el router decide: `["tactical"]`

#### **2. Performance Agent**
- **Especialidad:** Estadísticas de rendimiento y del equipo.
- **Proceso:**
  1. Recibe la pregunta.
  2. Convierte la pregunta en un embedding (vector).
  3. Busca en la colección `teams` de ChromaDB los 10 equipos más similares.
  4. Recupera el contexto (clasificación, puntos, goles).
  5. Envía la pregunta + contexto al LLM.
  6. El LLM genera el análisis de rendimiento.
- **Ejemplo:** "¿Cuántos puntos tiene el Madrid?" → busca en `teams` → responde con estadísticas.

#### **3. Tactical Agent**
- **Especialidad:** Análisis táctico, formaciones y estilos de juego.
- **Proceso:**
  1. Recibe la pregunta.
  2. La convierte en un embedding.
  3. Busca en la colección `tactical` de ChromaDB los 10 perfiles más similares.
  4. Recupera: formación, estilo de juego, características, fortalezas/debilidades.
  5. Envía la pregunta + contexto táctico al LLM.
  6. El LLM genera un análisis táctico detallado.
- **Ejemplo:** "¿Cómo juega el Barcelona?" → busca en `tactical` → responde con análisis de formación y estilo.

#### **4. Players Agent**
- **Especialidad:** Información de jugadores y plantillas.
- **Proceso:**
  1. Recibe la pregunta.
  2. La convierte en un embedding.
  3. Busca en la colección `players` de ChromaDB los 10 jugadores más similares.
  4. Recupera: nombre, edad, posición, nacionalidad, valoración, goles, asistencias.
  5. Envía la pregunta + datos de jugadores al LLM.
  6. El LLM organiza y presenta la información.
- **Ejemplo:** "¿Qué jugadores tiene el Arsenal?" → busca en `players` → enumera los jugadores organizados por posición.

#### **5. Comparative Agent**
- **Especialidad:** Comparaciones entre equipos o jugadores.
- **Proceso:**
  1. Recibe la pregunta.
  2. La convierte en un embedding.
  3. Busca en **las 3 colecciones** (teams, players, tactical) simultáneamente.
  4. Recupera los datos de ambas entidades a comparar.
  5. Envía la pregunta + datos de ambos equipos/jugadores al LLM.
  6. El LLM genera un análisis comparativo estructurado.
- **Ejemplo:** "¿PSG vs Barcelona?" → busca en las 3 colecciones → compara clasificaciones, tácticas y jugadores.

#### **6. Consolidator**
- **Función:** Combina las respuestas de todos los agentes en una única respuesta coherente.
- **Proceso:**
  1. Si solo respondió 1 agente → devuelve su respuesta directa.
  2. Si respondieron múltiples agentes → envía todas las respuestas al LLM.
  3. El LLM las combina, eliminando redundancias.
  4. Genera una respuesta final unificada.
- **Ejemplo:** Si respondieron Performance + Tactical → el consolidator las combina de forma inteligente.

---

## 📊 Ejemplo de Flujo de Datos

**Pregunta:** "¿Cómo está jugando el Real Madrid esta temporada?"

```
1. Router Agent
   ↓ Analiza la pregunta
   ↓ Decide: ["performance", "tactical"]
   
2. Performance Agent (en paralelo)
   ↓ Convierte la pregunta en vector (embedding)
   ↓ Busca en ChromaDB "teams"
   ↓ Recupera: Madrid 86 puntos, 2º puesto, 77 goles...
   ↓ El LLM genera: "El Real Madrid está en 2º lugar con 86 puntos..."
   
3. Tactical Agent (en paralelo)
   ↓ Convierte la pregunta en vector (embedding)
   ↓ Busca en ChromaDB "tactical"
   ↓ Recupera: formación 4-3-3, basado en posesión, ataque fluido...
   ↓ El LLM genera: "Tácticamente juega con un 4-3-3 con dominio de la posesión..."
   
4. Consolidator
   ↓ Recibe respuestas de Performance + Tactical
   ↓ El LLM las combina de forma inteligente
   ↓ Respuesta final: "El Real Madrid está en 2º lugar... Tácticamente..."
   
5. La API devuelve la respuesta al usuario
```

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Función |
|-----------|-----------|---------|
| **Orquestación** | LangGraph | Conecta agentes, maneja los flujos |
| **API REST** | FastAPI | Expone los endpoints HTTP |
| **LLM** | GPT-4o-mini (Azure) | Genera respuestas inteligentes |
| **Embeddings** | text-embedding-3-small (Azure) | Convierte texto en vectores |
| **Base de Datos Vectorial** | ChromaDB | Almacena y busca embeddings |
| **Datos** | API gratuita Live Football Data | API en tiempo real |
| **Lenguaje** | Python 3.11+ | Implementación |

---

## 📁 Estructura del Proyecto

```
football-rag/
├── agents/                   # Agentes especializados
│   ├── router_agent.py       # Decide qué agentes invocar
│   ├── performance_agent.py  # Análisis de rendimiento
│   ├── tactical_agent.py     # Análisis táctico
│   ├── players_agent.py      # Información de jugadores
│   └── comparative_agent.py  # Comparativas
├── documentation/            # Documentación del proyecto (incluye traducciones)
│   └── README.md             # Esta traducción al español
├── graph/
│   ├── state.py              # Estado compartido entre agentes
│   └── main_graph.py         # Orquestación con LangGraph
├── api/
│   └── main.py               # Endpoints de FastAPI
├── config/
│   └── constants.py          # Ligas, datos tácticos
├── data/                     # Base de conocimiento (auto-generada)
│   ├── teams_data.json
│   ├── players_data.json
│   └── tactical_data.json
├── chroma_db/                # Base de datos vectorial (auto-generada)
├── fetch_football_data.py    # Script: obtiene datos de la API
├── embed_and_upload.py       # Script: genera embeddings
├── index.html                # Interfaz web
├── .env.example              # Plantilla de credenciales
├── requirements.txt          # Dependencias de Python
└── README.md
```

---

## 🚀 Instalación y Uso (Local)

### 1. Clonar el repositorio

```bash
git clone https://github.com/ethann-19/ia-gen
cd multiagent-rag
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env`:

```env
RAPIDAPI_KEY=tu_clave_de_rapidapi
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_API_KEY=tu_clave_de_azure
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

### 4. Iniciar la API

```bash
uvicorn api.main:app --reload
```

### 5. Abrir la interfaz

Abre `index.html` en tu navegador.

---

## 💬 Preguntas de Ejemplo

```
¿Cómo está rindiendo el Real Madrid esta temporada?
¿Qué jugadores tiene el Arsenal?
¿Cómo juega el Bayern de Múnich tácticamente?
Compara el PSG con el Olympique de Marsella
¿Cuál es la diferencia táctica entre el Barça y el Atlético?
¿Qué equipo lidera la Premier League?
```

---

## ⚠️ Limitaciones

- Cubre únicamente a los **4 mejores equipos de cada liga** (20 equipos)
- Los datos tácticos son generados automáticamente (aproximaciones)
- RapidAPI tiene límites de solicitudes diarias en el plan gratuito
