from tokenize import String
from django.db import models
from core import models as core_models
from report.services import run_stored_proc_report
from location.models import Location, HealthFacility
from policy.models import Policy
from insuree.models import Insuree
from collections import defaultdict
from django.db.models import Count
from django.db.models import F
from insuree.models import Insuree
from insuree.models import InsureePolicy
import datetime
import qrcode
import base64
from io import BytesIO
import os

# def beneficiary_card_query(user, **kwargs):

#     # Create qr code instance
#     qr = qrcode.QRCode()

#     insureeObj = Insuree.objects.filter(
#             chf_id="070707070",
#             validity_to__isnull=True
#             ).first()

#     # The data that you want to store
#     data = {
#         'chf_id': insureeObj.chf_id,
#         'last_name': insureeObj.last_name,      
#         'other_names': insureeObj.other_names
#     }

#     # Add data
#     qr.add_data(data)

#     # Generate the QR Code
#     qr.make()

#     # Create an image from the QR Code instance
#     img = qr.make_image()

#     # Create a BytesIO object
#     buffered = BytesIO()

#     # Save the image to the BytesIO object
#     img.save(buffered, format="png")

#     # Get the byte data
#     img_str = base64.b64encode(buffered.getvalue())
#     #img_encoded = base64.b64encode(img.getvalue())

#     filename = "openIMISphone/"+insureeObj.photo.folder+"/"+insureeObj.photo.filename
#     print(filename)
#     if os.path.exists(filename):
#         with open(filename, "rb") as image_file:
#             encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
#     else :
#         with open("default-img.png", "rb") as image_file:
#             encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
#         print("File not found")


#     dictBase =  {
#         "QrCode": "data:image/PNG;base64,"+img_str.decode("utf-8"),
#         "PhotoInsuree": "data:image/PNG;base64,"+encoded_img,
#         "Prenom" : insureeObj.other_names,
#         "Nom" : insureeObj.last_name,
#         "DateNaissance" : insureeObj.dob,
#         "DateExpiration" : insureeObj.dob,
#         "idInsuree" : insureeObj.chf_id
#         }

#     print(dictBase)
#     return dictBase

def beneficiaries_list_card_query(user, **kwargs):
    print("kwargs ", kwargs)
    ids = kwargs.get("insureeids", [])
    insurees_ids = []
    if ids:
        ids = ids.split(',')
        insurees_ids = [eval(i) for i in ids]
    # Create qr code instance
    qr = qrcode.QRCode()
    
    insuree_list = Insuree.objects.filter(
            id__in=insurees_ids,
            validity_to__isnull=True
            )

    insurees_data = []
    for insureeObj in insuree_list:
        # The data that you want to store
        data = {
            'chf_id': insureeObj.chf_id,
            'last_name': insureeObj.last_name,      
            'other_names': insureeObj.other_names
        }

        # Add data
        qr.add_data(data)

        # Generate the QR Code
        qr.make()

        # Create an image from the QR Code instance
        img = qr.make_image()

        # Create a BytesIO object
        buffered = BytesIO()

        # Save the image to the BytesIO object
        img.save(buffered, format="png")

        # Get the byte data
        img_str = base64.b64encode(buffered.getvalue())
        #img_encoded = base64.b64encode(img.getvalue())

        filename = "openIMISphone/"+insureeObj.photo.folder+"/"+insureeObj.photo.filename
        print(filename)
        if os.path.exists(filename):
            with open(filename, "rb") as image_file:
                encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        else :
            with open("default-img.png", "rb") as image_file:
                encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
            print("File not found")

        insurees_data.append({
            "QrCode": "data:image/PNG;base64,"+img_str.decode("utf-8"),
            "PhotoInsuree": "data:image/PNG;base64,"+encoded_img,
            "Prenom" : insureeObj.other_names,
            "Nom" : insureeObj.last_name,
            "DateNaissance" : insureeObj.dob,
            "DateExpiration" : insureeObj.dob,
            "idInsuree" : insureeObj.chf_id
            }
        )
        
    dictBase =  {
        "InsureeList" : insurees_data
        }

    print(dictBase)
    return dictBase
