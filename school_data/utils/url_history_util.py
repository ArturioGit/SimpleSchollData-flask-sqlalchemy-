from flask import request, url_for, session


def save_response(response):
    if request.method == 'POST':
        return response

    if request.endpoint == 'static':
        return response

    history = session.get('history', [])

    if history:
        if (history[-1][0] == request.endpoint and
                history[-1][1] == request.view_args):
            return response

    history.append([
        request.endpoint,
        request.view_args,
        response.status_code
    ])

    session['history'] = history[-5:]
    return response


def url_back(fallback, *args, **kwargs):
    for step in session.get('history', [])[::-1]:
        if (step[0] == request.endpoint and
                step[1] == request.view_args):
            continue

        if 200 <= step[2] < 300:
            return url_for(step[0], **step[1])

    return url_for(fallback, *args, **kwargs)



