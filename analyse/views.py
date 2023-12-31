import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import *
import uuid
from django.db.models import Count
from django.db.models import Q
def upload_data(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_file = request.FILES['myfile']
        titre_name=uploaded_file.name.split('.')[0]
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

        # Detect file format and read data
        if file_name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif file_name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            return HttpResponse("Unsupported file format. Please upload a CSV or XLSX file.")

        # Convert data to a list of dictionaries
        records = data.to_dict('records')

        UUID = uuid.uuid4()
        
        # add data in database 
        for record in records:
            data=Data(titre=titre_name,paragraph=record['paragraph'],predicted_pabel=record['Predicted Label'],sentiment=record['Sentiment'],scores=float(record['Scores']),uuid=UUID)
            data.save()
            
        return render(request, 'home.html', {'records': records})
    
    return render(request, 'home.html')

def filter_data(request):
    if request.method == 'GET':
        # Récupérer les paramètres de requête (si présents)
        predicted_pabel = request.GET.get('predicted_pabel', '')
        sentiment = request.GET.get('sentiment', '')
        uuid = request.GET.get('uuid', '')
        created_at = request.GET.get('created_at', '')
        scores = request.GET.get('scores', '')

        # Filtrer les données en fonction des paramètres de requête
        filtered_data = Data.objects.all()

        if predicted_pabel:
            filtered_data = filtered_data.filter(predicted_pabel=predicted_pabel)

        if sentiment:
            filtered_data = filtered_data.filter(sentiment=sentiment)

        if uuid:
            filtered_data = filtered_data.filter(uuid=uuid)

        if created_at:
            filtered_data = filtered_data.filter(created_at=created_at)

        if scores:
            filtered_data = filtered_data.filter(scores=scores)


        context = {
            'filtered_data': filtered_data
        }

        return render(request, 'filter_data.html', context)


def display_data(request):
    grouped_data = Data.objects.values('titre') \
        .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                  fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                  positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                  negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                  neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
        .values('titre', 'real_count', 'fake_count', 'positive_count', 'negative_count', 'neutral_count') \
        .order_by('titre')
    context = {'grouped_data': grouped_data}
    return render(request, 'display_data.html', context)


