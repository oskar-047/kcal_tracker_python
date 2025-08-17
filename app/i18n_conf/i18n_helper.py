from fastapi import Request

def detect_lan(request: Request) -> str:
    # When the user enters the web, the browser automatically send a header on 
    # the http request, here the script reads that header

    # This line tries to get the header, if it can't it will save "" inside the var
    header = request.headers.get("accept-language", "")
    if not header:
        header = "en"

    lang_code = header.split(",")[0]
    return lang_code.split("-")[0]