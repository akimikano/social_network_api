from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    custom_response = {'data': None}
    error_list = []
    if response is not None:
        if 'detail' in response.data:
            error = {
                'field': 'general',
                'message': response.data['detail']
            }
            error_list.append(error)
        else:
            if isinstance(response.data, dict):
                for key, value in response.data.items():
                    if isinstance(value, list):
                        for el in value:
                            error_list.append({
                                'field': key,
                                'message': el
                            })
                    else:
                        error_list.append({
                            'field': key,
                            'message': value
                        })

        custom_response['errors'] = error_list
        response.data = custom_response
    return response
