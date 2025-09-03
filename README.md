# Greeting Agent

A simple greeting agent built with Google's Agent Development Kit (ADK) that asks for the user's name and location.

## Setup for GitHub Codespaces

### Quick Setup
Run the setup script to install dependencies and configure PATH:

```bash
chmod +x setup.sh
./setup.sh
source ~/.bashrc
```

### Manual Setup
If you prefer to set up manually:

```bash
# Install dependencies
pip install --user -r requirements.txt

# Add local bin to PATH
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

## Running the Agent

After setup, you can run the agent using:

```bash
adk run greeting_agent
```

If the `adk` command is still not found, use the Python module directly:

```bash
python -m google.adk.cli run greeting_agent
```

## Usage

Once the agent starts, you'll see a `user:` prompt. Type your messages and press Enter to interact with the agent. The agent will:

1. Greet you
2. Ask for your name
3. Ask where you're from

To exit the conversation, type `exit`.

## Example Interaction

```
user: Hello
agent: Hi there! What's your name?
user: My name is John
agent: Nice to meet you, John! Where are you from?
user: I'm from New York
agent: That's great! It's wonderful to meet someone from New York!
user: exit
```

## Project Structure

- `greeting_agent/agent.py` - Main agent configuration
- `requirements.txt` - Python dependencies
- `setup.sh` - Automated setup script for Codespaces
- `.gitignore` - Git ignore rules (excludes virtual environments)

## Requirements

- Python 3.8+
- Google ADK package and dependencies (see requirements.txt)