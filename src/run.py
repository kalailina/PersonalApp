from environment_app.flask_app import create_app  # Use absolute import

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)