# Cassandra - Your Personal AI Oracle

Cassandra is an advanced AI voice assistant that answers your spoken queries. Named after the prophetic figure from Greek mythology, Cassandra offers clear, insightful answers, harnessing the power of modern machine learning and voice processing technologies. From everyday inquiries to complex questions, Cassandra is engineered to assist with remarkable precision and efficiency. [^1]

[^1]: In Greek mythology, Cassandra was bestowed with the gift of prophecy by Apollo. However, when she did not return his love, he placed a curse on her so that her prophecies, though true, would never be believed. Somehow like LLMs :D

## Features

- **Voice Recognition**: Leverages Deepgram API's cutting-edge voice recognition capabilities to understand spoken language with high accuracy.
- **Language Processing**: Employs both the GPT API and a quantized, [efficient version of LLama 2 ](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF) model for local processing, delivering swift and accurate responses to a wide array of questions.
- **Speech Synthesis**: Integrates with Amazon Polly to provide natural and expressive spoken responses, completing the intuitive communication experience.

## Technical Overview

- **Deepgram API**: Provides real-time speech recognition and transcribes audio with state-of-the-art accuracy.
- **GPT and LLama 2**: Two options for language processing to fit the user's needs, whether it's cloud-based GPT API with its vast knowledge base or the locally hosted, lightweight LLama 2 [^1] model for privacy and efficiency.
- **Amazon Polly**: Turns text into lifelike speech using deep learning to produce speech that sounds like a human voice.


## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Access to Deepgram API and OpenAI GPT API with valid credentials.
- Amazon Web Services (AWS) account with access to Amazon Polly.

install the following dependencies:

```bash
deepgram-sdk
openai<1.0.0
boto3
pyaudio
sounddevice
numpy
ctransformers
```

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
Tell me about the Roman empire.
```

## License
Distributed under the MIT License. See LICENSE for more information.


## Roadmap

Our roadmap serves as a guide for the planned development trajectory of Cassandra, outlining current objectives and future enhancements to make Cassandra even more robust and user-friendly.

### Current Objectives

- **Local Model Integration**: To support fully offline functionality, we are working on incorporating local models for both speech-to-text and text-to-speech processes. This will ensure users can maintain privacy and independence from cloud services when desired.

- **Prompt Optimization**: Improving the prompts used for interacting with LLMs is on our agenda. By enhancing the prompts, Cassandra can generate more precise and contextually relevant responses.

- **Speech Recognition Refinement**: We aim to evolve Cassandra's speech recognition capabilities to enable more natural and human-like conversations, reducing the robotic feel and increasing the intuitive interaction experience.

### Future Enhancements

- **Multilingual Support**: Expanding Cassandra to understand and interact in multiple languages, making it a global assistant.

- **Voice Customization**: Allowing users to personalize Cassandra's voice to their preference, making the experience more individualized and engaging.

- **Emotion Recognition**: Integrating emotion recognition to read the sentiment of the user's speech, allowing for empathetic responses and a more dynamic interaction.

- **Continuous Learning**: Implementing a feedback loop where Cassandra learns from interactions to improve over time, providing a tailored experience to repeat users.

- **Customizable Wake Words**: Users can set their own wake word for activating Cassandra, offering a more personalized and branded experience.

- **Offline Cache**: Developing a system for Cassandra to cache certain data offline, enabling it to provide faster responses and reduce dependence on internet connectivity.

- **API Extensions**: Creating extensions for Cassandra to interact with other APIs and services, increasing its utility as a multipurpose tool.

Your feedback and suggestions are invaluable to our progress. If you have ideas or want to contribute to any of the roadmap items, please reach out or contribute directly via GitHub.
