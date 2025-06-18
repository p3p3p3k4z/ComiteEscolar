from app.web import crear_app_web
app_flask = crear_app_web()

if __name__ == '__main__':
    app_flask.run(debug=True, port=5000)

