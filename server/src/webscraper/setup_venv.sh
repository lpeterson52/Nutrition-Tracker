#! /bin/bash

PYTHON_CMD="python3"
CYAN='\033[0;36m'
NC='\033[0m' # no color

# Check if Python is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${CYAN}Python is not installed. Install Python and try again.${NC}"
    exit 1
fi

# Create a virtual environment if it doesn't already exist.
VENV_DIR="server/src/webscraper/.venv"
if [ -d $VENV_DIR ]; then
    echo -e "${CYAN}Virtual environment already exists.${NC}"
else 
    echo -e "${CYAN}Creating a virtual environment...${NC}"
    $PYTHON_CMD -m venv $VENV_DIR
fi

# Activate the virtual environment
echo -e "${CYAN}Activating the virtual environment...${NC}"
source $VENV_DIR/bin/activate

# Upgrade pip
echo -e "${CYAN}Upgrading pip...${NC}"
pip3 install --upgrade pip

REQUIREMENTS_PATH="server/src/webscraper/requirements.txt"
# Install dependencies if requirements.txt exists
if [ -f $REQUIREMENTS_PATH ]; then  
    echo -e "${CYAN}Installing dependencies from requirements.txt${NC}"
    pip install -r $REQUIREMENTS_PATH
else
    echo -e "${CYAN}No requirements.txt found. Skipping dependency installation.${NC}"
fi

echo -e "${CYAN}Virtual environment setup complete. Run 'source $VENV_DIR/bin/activate' to activate it.${NC}"