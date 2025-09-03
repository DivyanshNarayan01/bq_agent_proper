#!/bin/bash

# Setup script for GitHub Codespaces
echo "Setting up greeting_agent_proper..."

# Install requirements
echo "Installing Python dependencies..."
pip install --user -r requirements.txt

# Create a wrapper script for adk command since the executable isn't created properly
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
echo "To run the agent:"
echo "  source ~/.bashrc"
echo "  adk run greeting_agent"
echo ""
echo "Or run directly with:"
echo "  python -m google.adk.cli run greeting_agent"