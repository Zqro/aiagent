import os


def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        act_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks for common path
        valid_file_path = os.path.commonpath([working_dir_abs, act_file_path]) == working_dir_abs

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(act_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(act_file_path),exist_ok=True)

        with open(act_file_path, "w") as z:
            z.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:  # noqa: BLE001
         return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes or overwrites specified content to a file specified from a file path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path used to write/overwrite the specified file",
                },
                "content": {
                    "type": "string",
                    "description": "content used to write/overwrite within the specified file",
                }
            },
            "required": [
                "file_path", "content"
            ],
        },
    },
}
