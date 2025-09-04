# Greeting Agent

A simple greeting agent built with Google's Agent Development Kit (ADK) that asks for the user's name and location.

## Quick Start

To get started quickly, run these commands:

```bash
git clone https://github.com/DivyanshNarayan01/greeting_agent_proper.git
cd greeting_agent_proper
chmod +x setup.sh
./setup.sh
source ~/.bashrc
adk run greeting_agent
```

## Setup for GitHub Codespaces

### Quick Setup (Recommended)
Run the setup script to install dependencies and configure the environment:

```bash
chmod +x setup.sh
./setup.sh
source ~/.bashrc
```

The setup script will:
- Install all Python dependencies
- Create a custom `adk` wrapper command
- Configure your PATH automatically

### Manual Setup
If you prefer to set up manually:

```bash
# Install dependencies (including the missing 'deprecated' module)
pip install --user -r requirements.txt

# Create adk wrapper script
mkdir -p ~/.local/bin
cat > ~/.local/bin/adk << 'EOF'
#!/bin/bash
python -m google.adk.cli "$@"
EOF
chmod +x ~/.local/bin/adk

# Add local bin to PATH
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

## Running the Agent

After setup, you can run the agent using:

```bash
adk run greeting_agent
```

If you encounter any issues, you can always run directly with:

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