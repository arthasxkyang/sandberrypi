# unicoding: utf-8
import www

app = www.create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)