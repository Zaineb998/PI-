import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import *
import uuid
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import TruncMonth

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
        
    grouped_data = Data.objects.values('titre') \
        .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
        .values('titre', 'real_count', 'fake_count', 'positive_count', 'negative_count', 'neutral_count') \
        .order_by('titre')

    context = {'grouped_data': grouped_data}
        
    return render(request, 'titles_list.html', context)

def display_titles(request):
    if request.method == 'POST':
        # Get the start and end dates from the form submission
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Convert start_date and end_date to datetime objects (you may need to adjust the format)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter data based on release_date
        filtered_data = Data.objects.filter(release_date__range=[start_date, end_date])

        grouped_data = filtered_data.values('titre') \
            .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                      fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                      positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                      negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                      neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
            .values('titre', 'real_count', 'fake_count', 'positive_count', 'negative_count', 'neutral_count') \
            .order_by('titre')

    else:
        # If the form is not submitted, display all data
        grouped_data = Data.objects.values('titre') \
            .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                      fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                      positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                      negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                      neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
            .values('titre', 'real_count', 'fake_count', 'positive_count', 'negative_count', 'neutral_count') \
            .order_by('titre')

    context = {'grouped_data': grouped_data}
    return render(request, 'titles_list.html', context)

def display_chart(request, titre):

    # Fetch data for the first and second charts
    grouped_data = Data.objects.values('titre') \
        .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                  fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                  positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                  negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                  neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
        .filter(titre=titre) \
        .order_by('titre')

    # Fetch data for the third chart, grouped by month
    line_chart_data = Data.objects.annotate(month=TruncMonth('release_date')) \
        .values('month') \
        .annotate(real_count=Count('predicted_pabel', filter=Q(predicted_pabel='Real')),
                  fake_count=Count('predicted_pabel', filter=Q(predicted_pabel='Fake')),
                  positive_count=Count('sentiment', filter=Q(sentiment='Positive')),
                  negative_count=Count('sentiment', filter=Q(sentiment='Negative')),
                  neutral_count=Count('sentiment', filter=Q(sentiment='Neutral'))) \
        .filter(titre=titre) \
        .order_by('month')
    bar_chart_data = []
    doughnut_chart_data =[]
    # Prepare data for the charts
    bar_chart_labels = ['Fake', 'Real']
    if grouped_data:
        bar_chart_data = [grouped_data[0]['fake_count'], grouped_data[0]['real_count']]
        doughnut_chart_data = [grouped_data[0]['positive_count'], grouped_data[0]['negative_count'], grouped_data[0]['neutral_count']]

    doughnut_chart_labels = ['Positive', 'Negative', 'Neutral']
    

    line_chart_labels = [data['month'].strftime('%B %Y') for data in line_chart_data]
    fake_sentiment_data = [data['fake_count'] for data in line_chart_data]
    real_sentiment_data = [data['real_count'] for data in line_chart_data]
    positive_data = [data['positive_count'] for data in line_chart_data]
    negative_data = [data['negative_count'] for data in line_chart_data]
    neutral_data = [data['neutral_count'] for data in line_chart_data]

    context = {
        'titre_filter': titre,
        'bar_chart_labels': bar_chart_labels,
        'bar_chart_data': bar_chart_data,
        'doughnut_chart_labels': doughnut_chart_labels,
        'doughnut_chart_data': doughnut_chart_data,
        'line_chart_labels': line_chart_labels,
        'fake_sentiment_data': fake_sentiment_data,
        'real_sentiment_data': real_sentiment_data,
        'positive_data': positive_data,
        'negative_data': negative_data,
        'neutral_data': neutral_data,
    }

    return render(request, 'chart_page.html', context)

def delete_all_data(request):
    datas=Data.objects.all()
    for data in datas:
        data.delete()
    return HttpResponse("deletes")

