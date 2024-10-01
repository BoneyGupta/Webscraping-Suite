import time

from fastapi import FastAPI, UploadFile, File, HTTPException, status
import uvicorn
from starlette.responses import FileResponse
import shutil
import os
from fastapi.responses import StreamingResponse
from io import BytesIO
import zipfile
from datetime import datetime

import subprocess

app = FastAPI()

# Get the root directory of your project (assuming it's the parent of `api`)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"path root dir is {root_dir}")

# Now do your import
excel_archives_path = root_dir + "\\excel archives"
reports_directory_path = root_dir + "\\Reports"
html_pages_path = "./..\\HTML Pages"
run_ats_bat_file_path = root_dir + "\\Automation Test Suite\\Run-ATS.bat"
create_new_chrome_for_logged_sessions_bat_file_path = root_dir + "\\Automation Test Suite\\Create-New-Chrome-for-Logged-Sessions.bat"
open_logged_in_chrome_bat_file_path = root_dir + "\\Automation Test Suite\\Open-Logged-in-Chrome.bat"


def copy_file_to_new_folder(source_file_path, destination_folder, new_filename="Test.xlsx"):
    try:
        shutil.copy(source_file_path, os.path.join(destination_folder, new_filename))
        print(f"File copied successfully to {destination_folder}\\{new_filename}")
    except Exception as e:
        print(f"Error copying file: {e}")


def run_bat_file(bat_file_path):
    try:
        subprocess.run(bat_file_path, shell=True, check=True)
        print(f"BAT file executed successfully: {bat_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing BAT file: {e}")


def get_latest_report_folder(directory):
    # Find the latest modified directory in the reports folder
    all_sub_dirs = [
        os.path.join(directory, d) for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]
    latest_subdir = max(all_sub_dirs, key=os.path.getmtime, default=None)
    return latest_subdir


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return StreamingResponse(
        BytesIO(b"Swagger Docs refreshed at: " + datetime.now().isoformat().encode()),
        media_type="text/plain"
    )


@app.get("/download-excel-archives")
async def download_excel_archives():
    if not os.path.exists(excel_archives_path):
        raise HTTPException(status_code=404, detail="Folder not found")

    # Create an in-memory buffer for the zip file
    zip_buffer = BytesIO()

    # Zip the folder contents into the in-memory buffer using zipfile
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(excel_archives_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, start=excel_archives_path)  # Relative path for ZIP
                zip_file.write(file_path, arc_name)

    # Set the pointer to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    # Use StreamingResponse to send the in-memory zip file as a downloadable file
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=excel-archives.zip"
        }
    )


@app.post("/upload-test-xlsx")
async def upload_document(file: UploadFile = File(...)):
    try:
        excel_archives_file_path = excel_archives_path + f"\\{file.filename}"
        excel_folder_file_path = root_dir + "\\excel"

        if not file.filename.endswith(".xlsx"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File extension should be .xlsx"
            )

        with open(excel_archives_file_path, "wb") as f:
            f.write(file.file.read())

        copy_file_to_new_folder(excel_archives_file_path, excel_folder_file_path)

        return {"message": "File saved successfully"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        # Catch all other exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/run-ats-and-download-report")
async def run_ats_and_download_report():
    try:
        try:
            run_bat_file(run_ats_bat_file_path)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            # Catch all other exceptions and return a 500 Internal Server Error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

        time.sleep(5)

        # Step 2: Find the latest reports folder
        latest_report_folder = get_latest_report_folder(reports_directory_path)
        if latest_report_folder is None:
            raise HTTPException(status_code=404, detail="No reports found.")

        # Step 3: Create a ZIP file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(latest_report_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, start=latest_report_folder)
                    zip_file.write(file_path, arc_name)

        zip_buffer.seek(0)  # Reset the pointer to the start of the buffer

        # Step 4: Send the ZIP file as a response
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return StreamingResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            headers={
                "Content-Disposition": f"attachment; filename=report_{timestamp}.zip"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/download-html-pages")
async def download_html_pages():
    if not os.path.exists(html_pages_path):
        raise HTTPException(status_code=404, detail="Folder not found")

    # Create an in-memory buffer for the zip file
    zip_buffer = BytesIO()

    # Zip the folder contents into the in-memory buffer using zipfile
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(html_pages_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, start=html_pages_path)  # Relative path for ZIP
                zip_file.write(file_path, arc_name)

    # Set the pointer to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    # Use StreamingResponse to send the in-memory zip file as a downloadable file
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=html-pages.zip"
        }
    )


@app.get("/run-ats")
async def run_ATS():
    try:
        run_bat_file(run_ats_bat_file_path)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Catch all other exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/download-all-reports")
async def download_all_reports():
    if not os.path.exists(reports_directory_path):
        raise HTTPException(status_code=404, detail="Folder not found")

    # Create an in-memory buffer for the zip file
    zip_buffer = BytesIO()

    # Zip the folder contents into the in-memory buffer using zipfile
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(excel_archives_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, start=excel_archives_path)  # Relative path for ZIP
                zip_file.write(file_path, arc_name)

    # Set the pointer to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    # Use StreamingResponse to send the in-memory zip file as a downloadable file
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=excel-archives.zip"
        }
    )


@app.get("/create-new-chrome-for-logged-sessions")
async def create_new_chrome_for_logged_sessions():
    try:
        run_bat_file(create_new_chrome_for_logged_sessions_bat_file_path)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Catch all other exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/open-logged-in-chrome")
async def open_logged_in_chrome():
    try:
        run_bat_file(open_logged_in_chrome_bat_file_path)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Catch all other exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


port = 8001
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=port)

print(f"Click this link to open FastAPI Swagger Docs http://127.0.0.1:{port}/docs")
