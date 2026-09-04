import os
import httpx

class FlaskClient:
    BASE_URL = os.environ.get("FLASK_BASE_URL", "http://localhost:5000/api/v1")

    async def get_publications(self, name=None):
        async with httpx.AsyncClient() as client:
            params = {}
            
            if name:
                params["name"] = name
                
            res = await client.get(f"{self.BASE_URL}/publications", params=params)
            res.raise_for_status()
            return res.json()

    async def get_publication(self, publication_id):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/publications/{publication_id}")
            res.raise_for_status()
            return res.json()

    async def get_articles(self, publication_id, title=None, tag=None):
        params = {}

        if title:
            params["title"] = title
        if tag:
            params["tag"] = tag
            
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/publications/{publication_id}/articles", params=params)
            res.raise_for_status()
            return res.json()

    async def get_article(self, publication_id, article_id):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/publications/{publication_id}/articles/{article_id}")
            res.raise_for_status()
            return res.json()
    
    async def get_trending_entities(self, publication_id):
        async with httpx.AsyncClient() as client: 
            res = await client.get(f"{self.BASE_URL}/publications/{publication_id}/trending-entities")
            res.raise_for_status()
            return res.json()


flask_client = FlaskClient()