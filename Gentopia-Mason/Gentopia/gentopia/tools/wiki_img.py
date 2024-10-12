from typing import AnyStr, Union, List, Dict, Optional, Any
from gentopia.tools.utils.docstore import DocstoreExplorer, Docstore, Document
from gentopia.tools.basetool import *
import requests
import re
from pydantic import BaseModel, Field

class WikimediaImageStore(Docstore):
    """Wrapper around Wikimedia Commons API for image search."""

    def __init__(self) -> None:
        """Initialize the Wikimedia image store."""
        self.api_endpoint = "https://commons.wikimedia.org/w/api.php"

    def sanitize_query(self, query: str) -> str:
        return query.strip().strip('"\'').strip()

    def search(self, search: str, num_results: int = 5) -> Union[str, List[Document]]:
        """
        Search for images on Wikimedia Commons.
        If images are found, return a list of Documents with image info.
        If no images are found, return a string with similar search terms.
        """
        search = self.sanitize_query(search)
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"File:{search}",
            "gsrlimit": num_results,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "format": "json"
        }

        try:
            response = requests.get(self.api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            if 'query' in data and 'pages' in data['query']:
                for page in data['query']['pages'].values():
                    if 'imageinfo' in page:
                        image_info = page['imageinfo'][0]
                        description = image_info['extmetadata'].get('ImageDescription', {}).get('value', 'No description available')
                        doc = Document(
                            page_content=description,
                            metadata={"url": image_info['url'], "title": page.get('title', 'Unknown')}
                        )
                        results.append(doc)

            if results:
                return results
            else:
                # If no results, try a more general search without "File:" prefix
                params["gsrsearch"] = search
                response = requests.get(self.api_endpoint, params=params)
                response.raise_for_status()
                data = response.json()

                if 'query' in data and 'pages' in data['query']:
                    for page in data['query']['pages'].values():
                        if 'imageinfo' in page:
                            image_info = page['imageinfo'][0]
                            description = image_info['extmetadata'].get('ImageDescription', {}).get('value', 'No description available')
                            doc = Document(
                                page_content=description,
                                metadata={"url": image_info['url'], "title": page.get('title', 'Unknown')}
                            )
                            results.append(doc)

                if results:
                    return results
                else:
                    return f"No images found for [{search}]. Try different search terms."

        except requests.RequestException as e:
            return f"Error occurred while searching for images: {e}"

class WikimediaImageArgs(BaseModel):
    query: str = Field(..., description="a search query for images on Wikimedia Commons")

class WikimediaImage(BaseTool):
    """Tool that adds the capability to search for images relevant to a query."""

    name = "wikimedia_image"
    description = "Search engine for images from Wikimedia Commons. Useful when you need to find " \
                  "relevant images for topics, people, places, or concepts to enhance visual presentations."
    args_schema: Optional[Type[BaseModel]] = WikimediaImageArgs
    doc_store: Any = None

    def _run(self, query: AnyStr) -> AnyStr:
        # Clean up query using regex
        query = re.sub(r'[^a-zA-Z0-9_ ]', '', query)
        if not self.doc_store:
            self.doc_store = DocstoreExplorer(WikimediaImageStore())
        tool = self.doc_store
        evidence = tool.search(query)
        
        if isinstance(evidence, list):
            return "\n".join([f"Title: {doc.metadata['title']}\nURL: {doc.metadata['url']}\nDescription: {doc.page_content}" for doc in evidence])
        else:
            return evidence

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = WikimediaImage()._run("The Beatles")
    print(ans)