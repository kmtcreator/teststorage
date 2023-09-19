from flask import Flask, render_template, request, redirect, url_for
from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid
import os

app = Flask(__name__)

# Replace with the path to your Google Drive API credentials JSON file

SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "aerobic-cyclist-351707",
  "private_key_id": "eb67fc1857891f7937fbd915a1e21511e891efba",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7g6eRj6XSzLPC\nrwhsJw2UqzWwuPHTQDjShAW3jXyBNXmgIzt/Q9n4oqlMkZkWH3zCE+SY/+auDavZ\n9w6dC49/1eDz6SxxJZNR73GcK7hOLGVmlYFM9Wfm8CVTBxXsFdmRpIppAtoXYX61\nEvusPyS4g1AEtKEEcCl89j2eTdlxr5ImWFSKeu6eoXcPAr6dQ6XEGv5AUK49Bfmd\nYj0/GaZHmtLJ5SIXp+kZAteccjcttz6gobNoLGF9K9/YMlwIusNe8iHXgekAh6Jv\nPb5GzthTamBxfV+Rsn8MDVTJvjZxxu+XinMCru5cx76CWO2LaHkVisIk8jVAUFab\n/mr8YL0RAgMBAAECggEAIDlnTiIIBrpr9/x5b5CkilSD5Qtbb4jdWvwaOWmEqHXG\noYj8fAnuhwZ5HrH0w3MEzxt5EPwFKgsqacpFxiJK9laMko4TN5yT/SQve32d7j09\n7cuqjU2tHehOGb8hetFkct16dcJqNVNpYXfSLU8qodTbJvvdofQehR2SCEbro9gT\ncMYArG5MJqLJIZsdTktJTsEU0625QHGmIRHPMRk8NYjly/5KzeHu7xcJgFczJff8\nlJizC04l0LD0RKWPXLB+DVsyTOMAcpiFiE3JntpXejAzuTJ7EsRyPsg0pgjx8zEg\nMqy5fmFy1zgF1ccgzzxV7nZgHQuolS9F0Lqp4fOm8wKBgQDcfEA7WrKZscgfFELn\nlEJgsms9xCugf/JWBlsifzd9HVzpb8bM5LzRET4v6lzdQShDWPFrowuWiI8PhpTk\nHrbBMy5WONNSv/DNP0/NRwV0yRAHoHek9VfEN4/L/b0yBBN10McV1ok6tDExTS8H\n1oL9yoHki60Cq121V0F/jyJpAwKBgQDZt9X9DzXvdWoBLMjX2wT74GjmUzHow5GH\ndMwdCTlzE+sTJOejDrzXhW7s+BC/plGeuGnEjEOOWU05em5nto68xHYZg8MvMN8z\n/9BB4boJ0sGXCBffeUIljhKxMcyrdYHYubTS+EctsZenHQZhFBOEnftcsm0zMvjb\nqaB7Qu4jWwKBgQDLe3RAEuVPiM57OFTCqoZT/XWRjHEC7/HzyGvlO2k3c5ji60Ca\nqeNEQ1iUGgPYQiDpfrVXtCKmq6L0Hi1dFqdtSFHUSx9keDXBBlQczBXSARllIIgq\n2i5ErU5tYeBwv2hCTArgMZ12awQXTvc/kY5UsMcN6IYkN4kFKeEN20hThwKBgE7R\nvQimbxJH4Z6XRgbPZdiB/7gSumjYFGGDqTmB02iT93Cw1aM0fK1RwzzK+dVIMxhR\nDwl29iYcslZyunGVp8szHMZT61+0Q7ohjJWtUJqp0CgLaAkhbw8FhkLcEoqoOd/q\nK0qNU8d5GbwIR/zxNbe3Mf73IY19kJaFrHGzY18tAoGAKAa4PxWCbKLi3JVmzvhB\njvMvZfv9JEA/vHqYZkP2OvGpmRyQrR5slg+Z2pZ0oxPQbMh/2YrDzHcBaopRvzJP\nZ7GoNCtjUa1PMjjE/sB7MDz1I9qpbMJohCw+bFTDLBsOrKseaoj+xusGuwvBwA9J\nM2RZ+0IbCDl2L5s8qaSrUu8=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-yr37z@aerobic-cyclist-351707.iam.gserviceaccount.com",
  "client_id": "107636331051643185798",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yr37z%40aerobic-cyclist-351707.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

SCOPES = ['https://www.googleapis.com/auth/drive']
ALLOWED_EXTENSIONS = {'png', 'jpg'}


# Create a service object for the Google Drive API
def create_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# Create a unique file name for uploaded files
def generate_unique_filename(filename):
    unique_id = uuid.uuid4().hex
    _, extension = os.path.splitext(filename)
    return f"{unique_id}{extension}"

# Route to render the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']

        if not file:
            return "No file uploaded."

        drive_service = create_drive_service()
        unique_filename = generate_unique_filename(file.filename)

        file_metadata = {
            'name': unique_filename
        }

        media = drive_service.files().create(
            media_body=file,
            body=file_metadata
        ).execute()

        file_link = media.get('webViewLink')

        return f"File uploaded successfully. Link: <a href='{file_link}' target='_blank'>{file_link}</a>"
    except Exception as e:
        print(str(e))
        return "An error occurred."

if __name__ == '__main__':
    app.run(debug=True)
