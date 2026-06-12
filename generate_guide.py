import os

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini Me: How We Built It</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; text-align: center; }
        h2 { color: #2980b9; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }
        h3 { color: #16a085; margin-top: 20px; }
        p { margin-bottom: 15px; }
        ul, ol { margin-bottom: 15px; padding-left: 25px; }
        li { margin-bottom: 8px; }
        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
        blockquote { background: #f9f9f9; border-left: 5px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px; font-style: italic; }
        .highlight { background-color: #fff3cd; padding: 2px 5px; border-radius: 3px; }
        hr { border: 0; border-top: 1px solid #eee; margin: 40px 0; }
    </style>
</head>
<body>

    <h1>🎓 The Complete Story: How We Built Mini Me</h1>
    <p style="text-align: center; color: #7f8c8d;">A plain-English guide to building your local AI Agile Assistant</p>
    <hr>

    <h2>📖 Chapter 1: The Big Picture</h2>
    <p><strong>What we built:</strong> A tiny AI brain (Mini Me) that runs entirely on your computer, trained specifically to be an Agile Project Management assistant.</p>
    <p><strong>The journey in 5 steps:</strong></p>
    <ol>
        <li>Got a pre-trained AI brain (TinyLlama)</li>
        <li>Taught it new skills using your custom data (Fine-tuning)</li>
        <li>Made it faster and lighter (Quantization)</li>
        <li>Built a chat interface to talk to it (Inference)</li>
        <li>Added a learning loop so it improves over time (Feedback)</li>
    </ol>

    <h2>🧠 Chapter 2: TinyLlama - The Base Model</h2>
    <p><strong>What is it?</strong> TinyLlama is a small AI language model with 1.1 billion parameters. Think of it as a brain that has already read millions of books, websites, and conversations.</p>
    <p><strong>Why "tiny"?</strong> GPT-4 has ~1.8 TRILLION parameters. TinyLlama has 1.1 BILLION (1,600x smaller!). It's small enough to run on a regular CPU with 32GB RAM. It's like comparing a bicycle to a Ferrari - both get you there, but one fits in your garage.</p>
    <p><strong>The catch:</strong> TinyLlama knows <em>general</em> knowledge, but it doesn't know <em>your</em> specific needs. It's like hiring a smart college graduate - they're intelligent but don't know your company's processes yet.</p>

    <h2> Chapter 3: Fine-Tuning - Teaching New Tricks</h2>
    <p><strong>What is fine-tuning?</strong> Fine-tuning is like sending that smart graduate to a specialized training program. We take the pre-trained brain and expose it to specific examples so it learns your domain.</p>
    <p><strong>Analogy:</strong> Pre-trained model = Someone who knows how to cook (general skill). Fine-tuning = Teaching them to cook Italian food specifically (specialized skill).</p>
    <p><strong>Why not train from scratch?</strong> Training from scratch requires millions of dollars and months of time. Fine-tuning takes a few hours on your CPU, a few hundred examples, and almost no cost.</p>

    <h2>🔧 Chapter 4: LoRA - The Smart Shortcut</h2>
    <p><strong>What is LoRA?</strong> LoRA stands for <strong>Lo</strong>w-<strong>R</strong>ank <strong>A</strong>daptation. It's a technique that lets us fine-tune a model without changing all 1.1 billion parameters.</p>
    <p><strong>How LoRA works:</strong> Instead of changing the whole brain, LoRA adds tiny "adapter" layers on top. Think of it like: Original model = A locked encyclopedia (can't change it). LoRA adapters = Sticky notes you add to the pages (easy to add/remove).</p>
    <p><strong>The numbers:</strong> Full fine-tuning updates 1.1 billion parameters. LoRA updates only 1.1 MILLION parameters (0.1%!). This is why it works on your CPU.</p>

    <h2>📊 Chapter 5: Training Data - The Fuel</h2>
    <p><strong>What we created:</strong> 551 Q&A pairs covering Identity, Agile fundamentals, Scrum framework, Kanban, Estimation techniques, and Common challenges.</p>
    <p><strong>Format:</strong> Each example has an <code>Instruction</code> (the question), an <code>Input</code> (context, usually empty), and an <code>Output</code> (the correct answer).</p>
    <p><strong>Why 551 examples?</strong> 20 examples = Model barely learns. 100-200 = Basic understanding. 500+ = Solid knowledge base. We went with 551 as a sweet spot.</p>

    <h2>🔄 Chapter 6: Epochs - Practice Makes Perfect</h2>
    <p><strong>What is an epoch?</strong> An epoch is one complete pass through ALL your training data. Imagine studying for an exam: 1 epoch = Reading the textbook once. 5 epochs = Reading it 5 times.</p>
    <p><strong>Why multiple epochs?</strong> 1 epoch: Model sees each example once - barely remembers. 3-5 epochs: Model solidifies the knowledge and recognizes patterns.</p>
    <p><strong>Why not 100 epochs?</strong> Overfitting! If you study the same 551 questions 100 times, you'll memorize the exact answers but fail on new questions. The model becomes too specialized.</p>

    <h2>⚙️ Chapter 7: The Training Process</h2>
    <p><strong>What happens during training:</strong></p>
    <ol>
        <li><strong>Forward pass:</strong> Model reads a question and guesses an answer.</li>
        <li><strong>Loss calculation:</strong> Compare guess to correct answer (how wrong was it?).</li>
        <li><strong>Backward pass:</strong> Adjust the LoRA adapters to reduce the error.</li>
        <li><strong>Repeat:</strong> Do this for every example, 5 times.</li>
    </ol>

    <h2>🔗 Chapter 8: Merging - Combining the Brains</h2>
    <p><strong>What we did:</strong> After training, we combined the Base model (general knowledge) and the LoRA adapters (Agile knowledge) into a single model file. Now Mini Me has both baked in.</p>
    <p><strong>Analogy:</strong> Before merge: Student with a notebook full of Agile notes. After merge: Student who has memorized the notes and doesn't need them anymore.</p>

    <h2>⚡ Chapter 9: Quantization - Making It Fast</h2>
    <p><strong>What is quantization?</strong> Quantization reduces the precision of the model's numbers to make it smaller and faster. Float32 (32 bits) is super precise. Int8 (8 bits) is rounded, but good enough.</p>
    <p><strong>Results:</strong> Model size dropped from 2.2 GB to ~600 MB. Speed increased 2-3x. RAM usage dropped from 4 GB to ~1.5 GB. CPU is great at integer math (8-bit), making it perfect for this.</p>

    <h2>💬 Chapter 10: Inference - Talking to Mini Me</h2>
    <p><strong>What is inference?</strong> Inference is when you actually USE the trained model to generate responses. You type a question, the tokenizer converts it to numbers, the model predicts the next numbers, and the detokenizer turns them back into text.</p>

    <h2>🎓 Chapter 11: Continuous Learning - The Feedback Loop</h2>
    <p><strong>How it works:</strong> You ask a question, Mini Me answers, and you give feedback (👍 Good, 👎 Bad, or ✏️ Correct it). Good examples are saved and used in future prompts (in-context learning). After collecting 50+ examples, we retrain the model permanently (fine-tuning).</p>

    <hr>
    <h2> You Did It!</h2>
    <p>You went from zero to a fully functional, locally-running AI assistant. You understand the concepts, you built the system, and you have a working product. Mini Me might be small, but it's mighty - and it's all yours! 🤖✨</p>

</body>
</html>
"""

# Save the HTML file
file_path = "MiniMe_Guide.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Success! '{file_path}' has been created.")
print(" Open this file in your web browser (Chrome, Edge, etc.).")
print(" Press Ctrl + P (or Cmd + P on Mac).")
print("👉 Change the destination to 'Save as PDF' and click Save!")