<!-- <p align="center">
  <img src="https://raw.githubusercontent.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery/main/assets/banner.png" alt="OpenAI Agents SDK Mastery Banner" width="800"/>
</p> -->
```markdown

# OpenAI Agents SDK Mastery

[![GitHub License](https://img.shields.io/github/license/Moh-Tayyab/OpenAI-Agents-SDK-Mastery)](https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-%3E%3D%203.8-blue)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/Moh-Tayyab/OpenAI-Agents-SDK-Mastery)](https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Moh-Tayyab/OpenAI-Agents-SDK-Mastery)](https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery/pulls)

A comprehensive, evolving guide and collection of practical examples for mastering the OpenAI Agents SDK.

## Table of Contents

## 🧩 Examples Showcase

| Example                | Description                                   | File/Folder |
|-------------------------|-----------------------------------------------|-------------|
| Basic Agent            | Minimal working agent setup                  | [`basic_agent/`](basic_agent/) |
| Tools & Functions      | Using tools with agents                      | [`function_tools/`](function_tools/) |
| Context Management     | Memory & state handling                      | [`context_management/`](context_management/) |
| Streaming              | Real-time response streaming                 | [`streaming/`](streaming/) |
| Guardrails             | Input/output validation & safety              | [`guardrails/`](guardrails/) |
| Advanced Handoffs      | Passing control between multiple agents       | [`advanced_handoff/`](advanced_handoff/) |


## Introduction

This repository serves as a living document of my journey learning and experimenting with the OpenAI Agents SDK. It aims to provide clear examples, practical implementations, and evolving insights into building powerful agent-based applications. Whether you're new to the SDK or looking to deepen your understanding, you'll find resources here to help guide your mastery.

## Features & Concepts Covered

This repository is continuously updated with new learnings. Key areas explored include:

- Fundamentals of the OpenAI Agent architecture
- Creating and configuring different Agent types
- Defining and using Tools (Functions) with Agents
- Implementing custom instructions and memory patterns
- Handling Agent responses and streaming
- Advanced Agent interactions and workflows
- Best practices for development and deployment

*(As new concepts are learned, they will be added to this list and the relevant examples will be included.)*

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

- **Python:** Version 3.11 or higher.
- **OpenAI API Key:** Obtain an API key from [OpenAI Platform](https://platform.openai.com/).
- **Git:** Installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery.git
   cd OpenAI-Agents-SDK-Mastery
   ```
2. **(Recommended) Create a virtual environment:**
   ```bash
   uv venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   uv add dependency name
   uv add openai-agents
   ```
4. **Set up your OpenAI API Key:**
   You can set it as an environment variable:
   ```bash
   # On Linux/macOS
   export OPENAI_API_KEY='your-api-key-here'
   # On Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   *Alternatively, configure it according to the SDK's documentation.*

## Usage / Examples

Explore the `examples/` directory for hands-on demonstrations of various concepts.

**Example: Running a Basic Agent Script**

```bash
uv run examples/basic_agent_example.py
```

Detailed walkthroughs and explanations for each example can be found within their respective directories or files.

*(Add links or descriptions to specific examples as you create them.)*

## Project Structure

```
OpenAI-Agents-SDK-Mastery/

├── advanced_handoff/
├── advanced_tools/
├── agent_as_tools/
├── basic_agent/
├── cloning
├── context_management/
├── dynamic_instructions
├── function_tools
├── guardrails
├── handoffs
├── hosted_tools
├── ModelSettings
├── output_type
├── RunnerHook
├── streaming
├── Tools
├── tracing
├── web_search
├── ReadMe.md
```

## Contributing

This is primarily a personal learning repository, but suggestions, corrections, or discussions via Issues are welcome! If you have ideas for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources & Acknowledgements

- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [OpenAI Agents SDK](https://github.com/openai/openai-python)

## Contact

Muhammad Tayyab - [LinkedIn](https://www.linkedin.com/in/ch-muhammad-tayyab/)

Project Link: [https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery](https://github.com/Moh-Tayyab/OpenAI-Agents-SDK-Mastery)
``