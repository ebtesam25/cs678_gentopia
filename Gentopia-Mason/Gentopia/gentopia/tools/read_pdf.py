from typing import AnyStr
import requests
from gentopia.tools.basetool import *
import io
from pypdf import PdfReader


class ReadPdfArgs(BaseModel):
    url: str = Field(..., description="a PDF file url (hence ends with .pdf). You must make sure that the url is real and correct and that the PDF can be accessed.")


class ReadPdf(BaseTool):
    """Tool that adds the capability to extract text from urls of PDF files."""

    name = "read_pdf"
    description = "A tool to retrieve pdf through url. Useful when you have a url for a pdf and need to find detailed information inside."

    args_schema: Optional[Type[BaseModel]] = ReadPdfArgs

    def _run(self, url: AnyStr) -> str:
        try:
            response = requests.get(url)
            pdf_stream = io.BytesIO(response.content)
            reader = PdfReader(pdf_stream)
            number_of_pages = len(reader.pages)
            text = ""
            for i in range(number_of_pages):
                page = reader.pages[i]
                text += page.extract_text()
            #soup = BeautifulSoup(response.content, 'html.parser')
            #for script in soup(["script", "style"]):
            #    script.extract()
            #text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            text = ' '.join(line for line in lines if line)[:4096] + '...'
            return text
        except Exception as e:
            return f"Error: {e}\n Probably it is an invalid URL/PDF."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = ReadPdf()._run("https://cs.gmu.edu/~johnsonb/docs/icse2013.pdf")
    print(ans)
