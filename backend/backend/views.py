import pandas as pd
from PyPDF2 import PdfReader
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def process_file(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file uploaded'}, status=400)
    
    contacts = []
    if file.name.endswith('.xlsx') or file.name.endswith('.csv'):
        try:
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            contacts = df.to_dict(orient='records')
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    elif file.name.endswith('.pdf'):
        try:
            reader = PdfReader(file)
            for page in reader.pages:
                contacts.append({'value': page.extract_text()})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        return Response({'error': 'Unsupported file type'}, status=400)

    return Response({'contacts': contacts})
