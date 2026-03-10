# Telegram Bot

An LLM-powered Telegram chatbot that leverages personal context to provide tailored conversational experiences.

## Overview
This bot interacts with users by processing messages through Large Language Models, utilizing either local inference or cloud-based providers. It is designed to maintain a specific persona or context provided during setup.

## Features
* **Context-Aware Chat:** Uses provided background data to inform LLM responses.
* **Flexible Backend:** Supports multiple LLM execution paths:
    * **Cloud:** Provider-based inference via [AWS Bedrock](https://aws.amazon.com/bedrock/).
    * **Local:** Integration with [Ollama](https://ollama.com/) (Legacy).
* **Reliable Hosting:** Configured for seamless deployment on [Railway](https://railway.app/).

## Deployment
This project uses **Continuous Deployment** via Railway. 
* Every push to the `main` branch triggers a new build.
* **To skip deployment:** Include `[skip cd]` in your commit message if you are pushing changes that do not require a live update (e.g., documentation or README edits).

## Example
![alt text](figures/example.png)

> **Note:** More advanced versions of this bot, including agentic workflows and specialized tool-calling, are hosted in private repositories.

## Tech Stack
* **Infrastructure:** Railway
* **Interface:** Telegram Bot API
* **AI Orchestration:** AWS Bedrock / Ollama

---

## Author
**Ulises Rey**