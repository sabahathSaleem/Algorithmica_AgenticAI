from pydantic import BaseModel, Field

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

