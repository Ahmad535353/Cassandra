# Cassandra - Your Personal AI Oracle

Cassandra is an advanced AI voice assistant that answers your spoken queries. Named after the prophetic figure from Greek mythology, Cassandra offers clear, insightful answers, harnessing the power of modern machine learning and voice processing technologies. From everyday inquiries to complex questions, Cassandra is engineered to assist with remarkable precision and efficiency.

## Features

- **Voice Recognition**: Leverages Deepgram API's cutting-edge voice recognition capabilities to understand spoken language with high accuracy.
- **Language Processing**: Employs both the GPT API and a quantized, efficient LLama 2 model for local processing, delivering swift and accurate responses to a wide array of questions.
- **Speech Synthesis**: Integrates with Amazon Polly to provide natural and expressive spoken responses, completing the intuitive communication experience.

## Technical Overview

- **Deepgram API**: Provides real-time speech recognition and transcribes audio with state-of-the-art accuracy.
- **GPT and LLama 2**: Two options for language processing to fit the user's needs, whether it's cloud-based GPT API with its vast knowledge base or the locally hosted, lightweight LLama 2 model for privacy and efficiency.
- **Amazon Polly**: Turns text into lifelike speech using deep learning to produce speech that sounds like a human voice.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Access to Deepgram API and OpenAI GPT API with valid credentials.
- Amazon Web Services (AWS) account with access to Amazon Polly.

### Installation

Clone the repository and install the dependencies to set up your local development environment:

```bash
git clone https://github.com/yourusername/cassandra-ai-assistant.git
cd cassandra-ai-assistant
```

### Configuration
Fill in your API credentials in API_KEYS.py.

### Running Cassandra
Run the following command to start Cassandra:

```bash
python Cassandra_main.py
```

When it's listening, ask Cassandra a question. For example:

```
What is the meaning of life?
```

## License
Distributed under the MIT License. See LICENSE for more information.