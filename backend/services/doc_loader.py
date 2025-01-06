import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DocSection:
    content: str
    url: str
    title: str
    section: str

class DocumentationLoader:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_documentation(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_sections(self, html_content: str) -> List[DocSection]:
        soup = BeautifulSoup(html_content, 'html.parser')
        sections = []
        
        # Find all heading elements (h1, h2, h3)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        
        for i, heading in enumerate(headings):
            # Get the section title
            section_title = heading.get_text().strip()
            
            # Get content until next heading
            content = []
            current = heading.next_sibling
            while current and current not in headings:
                if current.string:
                    content.append(current.string.strip())
                current = current.next_sibling
            
            if content:
                sections.append(DocSection(
                    content=' '.join(content),
                    url=self.base_url,
                    title=section_title,
                    section=f"Section {i+1}"
                ))
        
        return sections
