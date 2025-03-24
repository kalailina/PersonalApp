[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18614806)
# COMP0035 Coursework 02 starter repository

1. Clone the project in VS Code, PyCharm or other Python IDE from GitHub
2. The coursework code has the following structure:

    ```text
     my_project/
     ├── .gitignore             # Git ignore file
     ├── README.md              # Project description and instructions
     ├── requirements.txt       # List of dependencies
     ├── pyproject.toml         # Installation and package details
     ├── src/                   # Main code directory
     │   ├── starter/           # App package directory, RENAME THIS TO SUIT YOUR APP!
     │      ├── __init__.py     # Has the code to configure the Flask app
     │      ├── static/         # e.g. CSS
     │      ├── templates/      # Jinja page templates saved as .html files
     │          ├── index.html  # Home page templates
     │      ├── routes.py       # Route definiton for the home page
     │      ├── run.py          # Alternative option for running the Flask app instead of command line
     ├── tests/                 # Test suite
     │   ├── conftest.py        # e.g. test fixtures
     │   ├── test_starter.py    # Example test, RENAME THIS TO SUIT YOUR APP!
     └── ...                    # Add module for your tests

      ```
3. Create and activate a virtual environment e.g. `.venv`
4. Install the project code using `pip install -e .`.

   If you use this command you should not also need to use the `requirements.txt` file. If this step fails, then install
   the required packages by entering `pip install -r requirements.txt` in the IDE's terminal window.

5. Run the test in `test_starter.py`. These should pass if your project files are structured as above and you completed
   `pip install -e .`

6. Run the Flask app from the terminal using `flask --app flaskstarter run --debug`.

   You’ll see output similar to this:

    ```text
   * Serving Flask app "flaskstarter"
   * Debug mode: on
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   * Restarting with stat
   * Debugger is active!
   * Debugger PIN: nnn-nnn-nnn
   ```

   Visit http://127.0.0.1:5000/ in a browser, and you should see the “Hello, Flask!” message.

   If another program is already using port 5000, you’ll see OSError: `[Errno 98]` or OSError: `[WinError 10013]` when
   the server tries to start.
   You can specify a different port using `--port` e.g.  `flask --app flaskstarter run --debug --port 5001`

You can also run the Flask app using `run.py` using the green run button in your IDE, or `python src/flaskstarter/run.py`.

7. Please change the app name to your own and not 'flaskstarter'. Use the IDE and Refactor > Rename so that all associated imports etc are changed to reflect the new name.
