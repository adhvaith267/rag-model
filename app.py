from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 
from rag import retriever, ask
from select_docs import select_all_docs

app = Flask(__name__)
CORS(app)

def format_text_as_html(text):
    paragraphs = text.strip().split('\n')
    html_paragraphs = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
    return html_paragraphs

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')

    if question.lower() == 'exit' or not question.strip():
        return jsonify({'response': 'Session ended or invalid input.'})

    results = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in results])

    prompt = f"[INST] Answer the question from the given context:\n\nContext: {context}\n\nQuestion: {question}\n\n[END]"
    response = ask(prompt)
    response = format_text_as_html(response)
    return jsonify({'response': response})

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", selected_documents=[doc.split("/")[-1] for doc in select_all_docs()])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

