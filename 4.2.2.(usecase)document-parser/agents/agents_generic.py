import asyncio
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.github import GitHubProvider
from pydantic_ai.settings import ModelSettings
#from models.generic import ModelAnalysisOutput, OCROutput
from utils import list_all_files, pdf_to_jpg, save_results_to_json

load_dotenv()

class FileElement(BaseModel):
    """Represents a single element detected on a document page.

    Examples of elements:
    - A table with columns and rows
    - A paragraph of text
    - An image or logo description
    - A header or title
    - A list or bullet points
    """

    element_type: str = Field(description="Type of the element found on the page", default="")
    element_content: str = Field(description="Content of the element found on the page", default="")


class ModelAnalysisOutput(BaseModel):
    """Structured output from the LLM for document analysis.

    This is the schema that tells the LLM exactly what we want back.
    PydanticAI uses this to enforce type checking on LLM responses.
    """

    file_type: str = Field(
        description="Type name which can describe given file precisely, e.g.: invoice, internal_document, instruction, other",
        default="",
    )
    file_content_md: str = Field(description="Output of the OCR process, contents of the file in Markdown", default="")
    file_elements: list[FileElement] = Field(
        description="Elements the given page consists from: tables, images, paragraphs, graphs, flowcharts etc.", default_factory=list
    )


class OCROutput(BaseModel):
    """Final output combining the filename and structured analysis results."""

    filename: str = ""
    analysis_result: ModelAnalysisOutput = Field(default_factory=ModelAnalysisOutput)

model = OpenAIChatModel("openai/gpt-4o", provider=GitHubProvider(api_key=os.getenv("GITHUB_API_KEY")), settings=ModelSettings(temperature=0))

agent = Agent(
    model=model,
    instructions="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
    output_type=ModelAnalysisOutput,  
)

async def run_inference(image_path: Path) -> OCROutput:
        message_parts = ["Extract the structure from the provided document.", BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg")]

        try:
            analysis_result = await agent.run(message_parts)
            print(f"File analyzed: {image_path.stem}")
        except Exception as e:
            print(f"Unexpected error while inference: {e}")
            raise RuntimeError from e
        
        output = OCROutput(filename=image_path.stem, analysis_result=analysis_result.output)
        return output


async def analyze_each_page(image_paths: list[Path]) -> list[OCROutput]:
    tasks = [run_inference(path) for path in image_paths]
    results_objects = await asyncio.gather(*tasks)
    return results_objects