from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def get_error_respose(request, message, error_box="#errors"):
    response = templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": 404,
            "detail": message,
        },
    )

    # Add error header (specify different target elements)
    response.headers["HX-Retarget"] = error_box

    return response


def get_success_respose(request, message, url_title, url_path):
    response = templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "status_code": 404,
            "message": message,
            "url_title": url_title,
            "url_path": url_path,
        },
    )

    return response
