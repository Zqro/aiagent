import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        act_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks for common path
        valid_file_path = os.path.commonpath([working_dir_abs, act_file_path]) == working_dir_abs

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(act_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(act_file_path, "r") as z:
            file_content_string = z.read(MAX_CHARS)

            if z.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string
    except Exception as e:  # noqa: BLE001
         return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads file contents from a specfied file path, truncates file content if content is too long",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path used to read the specified file",
                },
            },
            "required": [
                "file_path"
            ],
        },
    },
}
