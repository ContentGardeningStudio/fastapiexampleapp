from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def get_error_respose(request, message, error_box="#errors"):
    response = templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "detail": message,
        },
        headers={"HX-Retarget": error_box},
    )

    return response


def get_success_respose(request, message, url_title, url_path):
    response = templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "message": message,
            "url_title": url_title,
            "url_path": url_path,
        },
    )

    return response


def get_404_page(request):
    response = templates.TemplateResponse(
        "404.html",
        {
            "request": request,
        },
        status_code=404,
    )

    return response
