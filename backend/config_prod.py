import os

# Use os.environ instead of python-decouple for Render
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = os.environ.get('MODEL_NAME', 'gpt-4o-mini')
MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '15000'))
PDF_PATHS = os.environ.get('PDF_PATHS', './data/pdfs/Crustdata Dataset API Detailed Examples.pdf,./data/pdfs/Crustdata Discovery And Enrichment API.pdf').split(',')

# Add production-specific configurations
VECTOR_STORE_PATH = os.environ.get('VECTOR_STORE_PATH', '/opt/render/project/src/data/chroma') 