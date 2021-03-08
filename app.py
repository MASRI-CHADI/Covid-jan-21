import streamlit as st
import numpy as np
import functions_covid
from PIL import Image

# App Title
st.title("Détecteur de COVID")

# Introduction text
st.markdown(unsafe_allow_html=True, body="<p>Bienvenue sur le détecteur de COVID-19 et pneumonie.</p>"
                                         "<p>C'est une app basic sur Streamlit. "
                                         "Avec cette app, vous pouvez uploader une radio de la poitrine et prédire si le patient "
                                         "est atteint du COVID, d'une pneumonie ou sain.</p>"
                                         "<p>Le modèle est un réseau de neurone de convolution basé sur VGG16 "
                                         "il a pour le moment une précision test de "
                                         "<strong>85.6%.</strong></p>")

st.markdown("Commencez par charger une image radio des poumons.")

# uploader une image
image_name = st.file_uploader(label="Charger l'image", type=['jpeg', 'jpg', 'png'], key="xray")

if image_name is not None:
    # chargement de l'image
    img = np.array(Image.open(image_name))

    # preprocess de l'image
    img_pp = functions_covid.preprocess_image(img)
    
    if st.checkbox('Avec preprocessing'):
        st.image((img_pp[0]*255).astype(np.uint8))

    else:
        st.image(img)

        
    # chargement du modèle
    loading_msg = st.empty()
    loading_msg.text("En cours de prédiction..")
    model = functions_covid.load_model()

    # Prédiction
    prob, prediction = functions_covid.predict(model, img_pp)

    loading_msg.text('')

    if prediction == 'normal':
        st.markdown(unsafe_allow_html=True, body="<span style='color:green; font-size: 50px'><strong><h3>Normal! :smile:</h3></strong></span>")
    elif prediction == 'covid':
        st.markdown(unsafe_allow_html=True, body="<span style='color:red; font-size: 50px'><strong><h3>COVID! :slightly_frowning_face: </h3></strong></span>")
    elif prediction == 'pneumo':
        st.markdown(unsafe_allow_html=True, body="<span style='color:red; font-size: 50px'><strong><h3>Pneumonie! :slightly_frowning_face: </h3></strong></span>")

    st.text(f"*Probabilité associée à la prédiction : {round(prob * 100, 2)}%")
    
    last_conv_layer_name = "block5_conv3"
    classifier_layer_names = [
        'block5_pool',
        'global_average_pooling2d_3',
        'dense_9',
        'dropout_7',
        'dense_10',
        'dropout_8',
        'dense_11',
        'dropout_9',
        'dense_12',
        'dropout_10',
        'dense_13',
        'dropout_11',
        'dense_14']
    heatmap = functions_covid.make_gradcam_heatmap(
        img_pp, model, last_conv_layer_name, classifier_layer_names)
    st.markdown(unsafe_allow_html=True, body="<h3>Zone d'intérêt du réseau de neurone dans l'image pour prendre sa décision</h3>")
    st.image(heatmap, use_column_width=True)
    

