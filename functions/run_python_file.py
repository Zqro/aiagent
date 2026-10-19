import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        act_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # checks for common path
        valid_file_path = os.path.commonpath([working_dir_abs, act_file_path]) == working_dir_abs

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(act_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", act_file_path]

        # checks if args is not None
        if isinstance(args, list):
            command.extend(args)

        i = subprocess.run(command, capture_output=True,text=True,timeout=30)  # noqa: PLW1510

        output_text = ""

        if i.returncode != 0:
            output_text += f"Process exited with code {i.returncode}\n"
        if len(i.stdout) == 0 and len(i.stderr) == 0:
            output_text += "No output produced\n"
        else:
            output_text += f"STDOUT: {i.stdout}\nSTDERR: {i.stderr}\n"

        return output_text



    except Exception as e:  # noqa: BLE001
         return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "runs a file from a specfied file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path used to run the specified file",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": [
                "file_path",
            ],
        },
    },
}
