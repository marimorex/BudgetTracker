# Development

1. **Prerequisites:**
- python3.12 or higher , pip3 and venv. here after some commands to install the prerequisits:
    - `sudo apt update`
    - `sudo apt install python3`
    - `sudo apt install python3-pip`
    - `sudo apt install python3-venv`

2. **Create a virtual environment**:
   `python3 -m venv name_of_your_venv`

3. **Activate the virtual environment**:
   - For Linux/macOS: `source name_of_your_venv/bin/activate`
        - To deactivate venv run: `deactivate`
            - to remove a venv run : `sudo rm -rf name_of_your_venv`
   - For Windows: `venv\Scripts\activate`

4. **Install the dependencies**:
   `pip3 install -r requirements.txt`

5. **Run tests**:
   `python3 -m unittest discover test`


# Run project
- docker compose up --build
