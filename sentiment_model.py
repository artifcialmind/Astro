from keras import models
model = models.load_model('Sentiment_model.h5', compile=False)
model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])
from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('bert-base-nli-mean-tokens')
import numpy as np


label_to_feelings = {0: 'neutral', 1:'positive', 2: 'negative'}
def prediction(text):
    tmp = model.predict(encoder.encode([text]))
    confidence = tmp[0][np.argmax(tmp)]
    return label_to_feelings[np.argmax(tmp)], confidence

#while True:
    # = input()
    #print(prediction(x))

