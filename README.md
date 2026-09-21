# Security Command Lab

Security Command Lab is a developing Flask web application that turns cybersecurity knowledge into short, practical command-line challenges.

> Knowing what a security tool does is different from recognising when to use it, constructing the command and understanding the result.

The project is intended to help bridge the gap between guided, learn-by-doing platforms such as Boot.dev and the practical training currently available across the cybersecurity pathway. It provides a focused place to practise recalling commands and applying concepts without immediately relying on hints, walkthroughs or a live target.

**Project status:** Version 1 prototype  
**Current coverage:** 40 scenarios  
**Available levels:** Basic and Standard

## How It Works

A training session can be configured around three choices:

1. Select one or more cybersecurity topics.
2. Choose the difficulty level.
3. Set a time limit for the session.

The application then presents practical questions in a simulated terminal. The learner enters the command they believe fits the scenario, receives immediate validation feedback and works through the selected question set before receiving a final score.

For example, a scenario might provide a target network and ask the learner to choose an appropriate discovery or enumeration command. The task is not simply to recognise the name of a tool—it is to recall the relevant syntax, flags and target format under light time pressure.

Commands entered into the application are **not executed**. Version 1 compares the supplied answer with validation rules stored alongside each scenario.

## Training Topics

The current scenario library is divided into four selectable pathways:

| Topic | Current focus |
| --- | --- |
| Security+ | Foundational security concepts and practical command awareness |
| Offensive Security | Early offensive-security methodology and command selection |
| Pentesting | Reconnaissance, enumeration and penetration-testing fundamentals |
| Ethical Hacker | Broader practical security and ethical-hacking knowledge |

These pathways describe the direction of the training content. They are not official course material and the project is not affiliated with CompTIA, CREST, OffSec or Boot.dev.

## Current Scenario Coverage

Version 1 contains 40 scenarios:

| Difficulty | Security+ | Offensive Security | Pentesting | Ethical Hacker | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Basic | 5 | 5 | 5 | 5 | 20 |
| Standard | 5 | 5 | 5 | 5 | 20 |
| Professional | Planned | Planned | Planned | Planned | 0 |

The Professional tier represents a future CREST/OSCP-oriented stage. It is not populated in the current scenario library.

## Session Timers

Sessions can currently be set to:

- 5 minutes
- 10 minutes
- 20 minutes
- 30 minutes
- 1 hour
- 1 hour 30 minutes
- 2 hours

The shorter options support quick recall practice, while the longer sessions allow several topics to be combined into a broader knowledge check.

## Getting Started

### Requirements

- Python 3.10 or later
- Flask 3
- PyCharm is optional but is the current development environment

### Clone and Run

```bash
git clone https://github.com/g5live/security-command-lab.git
cd security-command-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python sec-command.py
```

Open `http://127.0.0.1:5000` in a browser.

The application generates a temporary session secret when it starts. To keep browser sessions valid across application restarts, provide your own secret:

```bash
SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" python sec-command.py
```

Debug mode is disabled by default. It can be enabled for local development with `FLASK_DEBUG=1`; do not expose the development server to an untrusted network.

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### Run in PyCharm

1. Open the `security-command-lab` directory as a project.
2. Select the Python interpreter inside `.venv`, or allow PyCharm to create a new virtual environment.
3. Install Flask into that interpreter.
4. Run `sec-command.py`.
5. Open the local address shown in the Run window.

## Run the Tests

The regression tests use Python's built-in `unittest` framework, so no additional test package is required:

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```text
security-command-lab/
├── core/
│   └── engine.py          # Loads scenarios and validates submitted commands
├── data/
│   ├── ethical_hacker.json
│   ├── offensive_security.json
│   ├── pentesting.json
│   └── security_plus.json
├── templates/
│   ├── index.html         # Scenario and simulated terminal view
│   ├── menu.html          # Training-session configuration
│   └── results.html       # Final score and session result
├── tests/
│   ├── test_app.py        # Flask route and session regression tests
│   └── test_engine.py     # Scenario loading and validation tests
├── requirements.txt       # Reproducible Python dependency versions
└── sec-command.py         # Flask application and routes
```

## Current Limitations

- Only the Basic and Standard scenario tiers currently contain questions.
- Validation checks for required or forbidden command components; it is not yet a full command parser.
- Each scenario currently expects a single command rather than a connected investigation workflow.
- Commands are simulated and are never passed to a system shell or external target.
- Progress is stored only for the current browser session.
- There are no user accounts, saved results or long-term progress statistics yet.
- The application is currently intended for local development and learning use.

## Development Roadmap

### Expand the Scenario Library

Increase the library from 40 to 100 scenarios, with broader coverage across all four training topics and a more gradual progression in difficulty.

### Add Multi-Stage Challenges

Develop connected scenarios in which several actions form one overall investigation. A future challenge might require the learner to:

1. Scan the target.
2. Interpret the exposed services.
3. Choose an enumeration route.
4. Select the next command or tool.
5. Work through a controlled exploitation or Meterpreter-style stage.

This would reinforce methodology and decision-making rather than testing isolated command recall.

### Introduce Different Environments

Add visual and contextual variety to scenario presentation, including:

- Linux terminals
- Windows shells
- Web pages and browser-based tasks
- Tool-specific or application-specific interfaces
- Investigation views that include output, logs or other evidence

### Build a More Informative Application

Develop the website beyond the current basic Flask interface with:

- Clearer guidance and explanations
- More detailed feedback after each answer
- Scenario filters and session summaries
- Progress and performance information
- Improved navigation, accessibility and responsive presentation
- Expanded test coverage, CSRF protection and deployment-ready configuration

## Responsible Use

Security Command Lab is designed for education and authorised practice. Any future exercises involving real tools or systems should only be performed against environments you own or have explicit permission to test.

The aim is to build understanding—not just memorise commands—and to make the transition from theory to structured practical work less abrupt.
