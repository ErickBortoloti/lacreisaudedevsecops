from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)

def home():
    return """
        <body style="font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <div style="text-align: center;">
                <h1>API Status Checker</h1>
                <p>Clique no botão abaixo para verificar o status:</p>
                <a href="/status">
                    <button style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
                        Ver Status
                    </button>
                </a>
            </div>
        </body>
    </html>
            


    """



@app.get("/status", response_class=HTMLResponse)
def status():
    return """
    <html>
        <body style="font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <div style="text-align: center;">
                <h1>Status: OK</h1>
                <p>Tudo funcionando!</p>
                <a href="/">
                    <button style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
                        Voltar
                    </button>
                </a>
            </div>
        </body>
    </html>
    """