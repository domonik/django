import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import sparse_categorical_crossentropy
import pickle
import tensorflow as tf
from .models import Lyrics

def loss(labels, logits):
    return sparse_categorical_crossentropy(labels, logits, from_logits=True)


def generate_text(model, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 800

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension

        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # We pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))

model = load_model("./model/model.h5")
model.compile(optimizer='adam', loss=loss)
char2idx = pickle.load(open("./model/char2idx.p", "rb"))
idx2char = pickle.load(open("./model/idx2char.p", "rb"))
def index(request):
    context = {"predicted_text": None}
    return render(request, "index.html", context)

def predictText(request):
    request_text = request.POST["text"]
    predicted_text = generate_text(model, request_text)
    context = {"predicted_text": predicted_text,}
    return render(request, "index.html", context)


def saveLyrics(request):
    lyricsTitle = request.POST["title"]
    lyrics =  request.POST["lyrics"]
    name = request.user
    print(name)
    if request.user.is_authenticated:
        saved_lyrics = Lyrics(title=lyricsTitle, lyrics=lyrics, author=name)
        saved_lyrics.save()
    context = {"predicted_text": lyrics}
    return render(request, "index.html", context)