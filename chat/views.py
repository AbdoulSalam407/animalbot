from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np


model = MobileNet()

class ChatImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        img_file = request.FILES.get('image')
        if not img_file:
            return Response({"result": "Aucune image reçue"}, status=400)

        temp_path = "media/temp.jpg"
        with open(temp_path, 'wb+') as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        img = image.load_img(temp_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        label = decode_predictions(preds, top=1)[0][0][1]

        return Response({"result": f"Cet animal ressemble à un(e) {label}"})
