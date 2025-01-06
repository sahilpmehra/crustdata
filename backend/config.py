from decouple import config

OPENAI_API_KEY = config('OPENAI_API_KEY')
MODEL_NAME = config('MODEL_NAME', default='gpt-4o-mini')
MAX_TOKENS = config('MAX_TOKENS', default=15000, cast=int)
PDF_PATHS = config('PDF_PATHS', default='./data/pdfs/Crustdata Dataset API Detailed Examples.pdf,./data/pdfs/Crustdata Discovery And Enrichment API.pdf').split(',') 
