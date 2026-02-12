from botocore.errorfactory import ClientError


def get_error_code(client_error: ClientError) -> str:
    error = client_error.response.get("Error")
    if error is None:
        return "(Error=None)"

    code = error.get("Code")

    if code is None:
        return "(Code=None)"

    return code
