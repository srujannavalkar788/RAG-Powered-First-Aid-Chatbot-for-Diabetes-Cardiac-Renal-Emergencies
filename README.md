🚑 MediAssist: Medical First-Aid RAG Chatbot

*A Retrieval-Augmented Generation (RAG) system providing evidence-based first-aid guidance for diabetes, cardiac, and renal emergencies.*





## Features
- **Hybrid Retrieval**: 60+ verified medical snippets + real-time web evidence
- **Emergency Triage**: Flags critical symptoms (e.g., chest pain, hypoglycemia)
- **Actionable Guidance**: Step-by-step first-aid with citations
- **Safety Layers**: Dosage checks & clinical disclaimers

## 🛠️ Setup

### Prerequisites
- Python 3.9+
- OpenAI API key (for GPT-4/GPT-3.5)
- Serper.dev API key (optional for web search)

### Installation

git clone https://github.com/yourusername/MediAssist.git
cd MediAssist
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt


Configuration
Rename .env.example to .env

Add your API keys:

OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here  # Optional

🚀 Usage
bash
streamlit run src/app.py


Example Queries:

"My glucose is 50 and I'm shaking"

"Crushing chest pain radiating to left arm"

"No urine output for 12 hours with flank pain"

⚖️ Design Trade-offs

1. Retrieval System

Approach: Serper.dev (Web)

Pros : Real-time updates

Cons :  Slow (600ms), costs $50/month after 2,500 searches

2. Response Generation

Model : GPT-3.5

Accuracy :  82%	 

Cost/Query :  $0.0004   

Hardware Needs:  API only

