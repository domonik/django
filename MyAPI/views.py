import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # needs to be set to prevent using the gpu
from django.shortcuts import render, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import sparse_categorical_crossentropy
import pickle
import tensorflow as tf
from .models import Lyrics
from django.contrib import messages

# loading the pre-trained model that is used for German Rap Song prediction
# the model was trained using a slightly different version of the scipt that can be found at:
# colab.research.google.com\/drive\/1ZZXnCjFEOkp_KdNcNabd14yok0BAIuwS#forceEdit=true\\u0026sandboxMode=true
model = load_model("./model/model.h5")
# dict that returns an number for each character. The dict is the same that was used for training
char2idx = pickle.load(open("./model/char2idx.p", "rb"))
# list with the corresponding character at the index so the numbers that are predicted by the model 
# can get tranformed to the corresponding character 
idx2char = pickle.load(open("./model/idx2char.p", "rb"))


# function that generates text from a start string.
# the function was copied from:
# colab.research.google.com\/drive\/1ZZXnCjFEOkp_KdNcNabd14yok0BAIuwS#forceEdit=true\\u0026sandboxMode=true
def generate_text(model, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 800

    # Converting our start string to numbers (vectorizing)
    try:
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
    except KeyError:
        return None


def home(request):
    context = {}
    return render(request, "home.html", context)

# renders the homepage without predicted lyrics
def index(request):
    context = {"predicted_text": None}
    return render(request, "index.html", context)

# renders the homepage and shows predicted lyrics
def predictText(request):
    request_text = request.POST["text"]
    predicted_text = generate_text(model, request_text)
    if predicted_text is not None:
        context = {"predicted_text": predicted_text,}
        return render(request, "index.html", context)
    else:
        messages.info(request, "Query contains non valid characters")
        return redirect("homepage")

# saves predicted lyrics as a model to the database
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