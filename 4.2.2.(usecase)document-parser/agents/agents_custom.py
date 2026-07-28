import asyncio
import os
from pathlib import Path
import time
from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent
from models.invoice import Invoice
from models.payslip import Payslip
from models.drivers_license import DriversLicense
from models.category import DocumentCategory
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.github import GitHubProvider
from pydantic_ai.settings import ModelSettings
from utils import list_all_files, pdf_to_jpg, save_results_to_json

load_dotenv(override=True)

model = OpenAIChatModel("openai/gpt-4.1", provider=GitHubProvider(api_key=os.getenv("GITHUB_API_KEY")), settings=ModelSettings(temperature=0))

classifier_agent = Agent(
    model,
    instructions="You are a helpful assistant.",
    output_type=DocumentCategory
)

extraction_agent = Agent(
    model,
    instructions="You are a helpful assistant."
)

# Map classification types to schemas
classification_to_schema = {
    "invoice": Invoice,
    "payslip": Payslip,
    "driver_license": DriversLicense,
}

async def run_inference(image_path: Path) -> Invoice | Payslip | DriversLicense:
        classifier_message_parts = ["Classify the type of the following document based on its content and structure.", BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg")]
        extractor_message_parts = ["Extract the structure from the provided document.", BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg")]

        try:
            print(f"##File analyzed: {image_path.stem}")
            classifier_response = await classifier_agent.run(classifier_message_parts)
            category = classifier_response.output.category
            print(f"\n##Detected category: {category}")
            output_type = classification_to_schema.get(category)
            extraction_response = await extraction_agent.run(extractor_message_parts, output_type=output_type)
            print(f"\n##Extracted data: \n{extraction_response.output}")
        except Exception as e:
            print(f"Unexpected error while inference: {e}")
            raise RuntimeError from e
        return extraction_response.output


async def extract_structured_data(image_paths: list[Path]) -> list[Invoice | Payslip | DriversLicense]:
    tasks = [run_inference(path) for path in image_paths]
    results_objects = await asyncio.gather(*tasks)
    return results_objects

async def workflow():
    pdf_dir = Path(__file__).parent.resolve() / "data1"
    temp_dir = pdf_dir / "temp_files"
    results_dir = pdf_dir / "results"

    pdf_paths = list_all_files(pdf_dir)
    for pdf_path in pdf_paths:
        image_paths = pdf_to_jpg(pdf_path, temp_dir)
        results = await extract_structured_data(image_paths)
        save_results_to_json(pdf_path.stem, results, results_dir)


if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        asyncio.run(workflow())
    except Exception as e:
        print(e)
    end_time = time.perf_counter() - start_time
    print(f"Analysis took: {end_time:.1f} seconds")