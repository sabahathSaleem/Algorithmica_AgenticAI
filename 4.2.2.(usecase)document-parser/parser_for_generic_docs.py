import asyncio
import time
from pathlib import Path
from utils import list_all_files, pdf_to_jpg, save_results_to_json
from agents.agents_generic import analyze_each_page

async def workflow():
    base_dir = Path(__file__).parent.resolve() / "data2"
    pdf_dir = base_dir / "samples"
    temp_dir = base_dir / "temp_files"
    results_dir = base_dir / "results"

    pdf_paths = list_all_files(pdf_dir)
    for pdf_path in pdf_paths:
        image_paths = pdf_to_jpg(pdf_path, temp_dir)
        results = await analyze_each_page(image_paths)
        save_results_to_json(pdf_path.stem, results, results_dir)


if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        asyncio.run(workflow())
    except Exception as e:
        print(e)
    end_time = time.perf_counter() - start_time
    print(f"Analysis took: {end_time:.1f} seconds")