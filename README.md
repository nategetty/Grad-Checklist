# Grad-Checklist
Developing an automated system for Western University to streamline the graduate checklist process. Empowering faculty with an efficient, user-friendly interface to enhance workflow efficiency. A proof of concept showcasing the feasibility and advantages of automation at the University of Western Ontario.

## How to install

### Clone repository
1. Open a terminal window at the directory where you want the repo to be cloned to.
2. Clone the repo: `git clone https://github.com/nategetty/Grad-Checklist.git`
3. Change to the newly created directory: `cd Grad-Checklist`

### Set up venv (or do it with PyCharm, just make sure the venv is in the `Grad-Checklist/` directory)
1. Make sure you are in the `Grad-Checklist/` directory.
2. Create a new virtual environment: `python3 -m venv .venv`
3. Activate the venv (Linux / Mac): `. .venv/bin/activate`
4. Activate the venv (Windows): `venv\Scripts\activate.bat` (cmd) or `venv\Scripts\Activate.ps1` (PowerShell)

### Install MySQL (Mac)
1. Install MySQL: `brew install mysql`
2. Start the MySQL server: `brew services start mysql`
- MySQL runs in the background and may slow down your computer, so remember to stop it after you are done using it: `brew services stop mysql`

### Install MySQL (Windows)
https://dev.mysql.com/doc/refman/8.3/en/windows-installation.html

### Install Python packages
1. Install the gradchecklist package in editing mode: `pip install -e .`
2. Install pytest: `pip install pytest`
3. Run tests to make sure everything is working: `pytest`

## How to integrate your code

- Put your Python files in the `Grad-Checklist/gradchecklist` directory.
- Import using relative imports. Example: `import .course`
- Main functions will not work inside the gradchecklist package. Instead, create a Python file outside of the package
(in the `Grad-Checklist/` directory) and move your main function there.
In that file, you can import from the package like this: `import gradchecklist.course`
- Put tests in the `tests/` directory.
- Run the development web server using: `flask --app gradchecklist --debug run -p 5001`
- Access the website at: `localhost:5001`
