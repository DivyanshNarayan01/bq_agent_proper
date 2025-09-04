#!/bin/bash

# Setup script for BigQuery Notebook environment
echo "Setting up BigQuery Data Agent..."

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create a wrapper script for adk command
mkdir -p ~/.local/bin
cat > ~/.local/bin/adk << 'EOF'
#!/bin/bash
python -m google.adk.cli "$@"
EOF
chmod +x ~/.local/bin/adk

# Add local bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding ~/.local/bin to PATH..."
    echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
    export PATH=$PATH:$HOME/.local/bin
fi

# Make the script executable for future runs
chmod +x setup.sh

echo "Setup complete!"
echo ""
echo "BigQuery Data Agent is ready to use!"
echo ""
echo "To run the agent in BigQuery notebook:"
echo "  1. Clone this repo: git clone <your-repo-url>"
echo "  2. Run: cd bq_agent_proper && ./setup.sh"
echo "  3. Run: adk run greeting_agent"
echo ""
echo "Or run directly with:"
echo "  python -m google.adk.cli run greeting_agent"
echo ""
echo "The agent will automatically authenticate using notebook credentials."