# MatrixAI Bot

A Matrix Bot for chatting with AI and generating pictures

## Usage

1. Invite `@ai:projectsegfau.lt` to your room
2. Chat with AI by doing `!ask Who are you ?`
3. Generate a picture by doing `!img A cat style=REALISTIC`
4. Do `!help` for getting more help

## Setup

``` shell
git clone https://git.projectsegfau.lt/0xMRTT/matrixai.git && cd matrixai
pip install -r requirements.txt
cp run.sh.example run.sh
mkdir -p ~/.local/share/systemd/user/
cp matrixai.service ~/.local/share/systemd/user/
```

And after 

- Customize `run.sh` with your settings
- Fix the path to `run.sh` in the service file (`~/.local/share/systemd/user/matrixai.service`)

## Thanks

- [Baichat-py](https://bavarder.codeberg.page/code/baichat)
- [Simple Matrix Bot](https://simple-matrix-bot-lib.readthedocs.io/en/latest/examples.html)
- [Discord AI](https://github.com/mishalhossin/Discord-AI-Chatbot/tree/main)