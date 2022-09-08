from django.http import HttpResponse


def download_file_response(ingredients_list):
    buy_list = []
    for item in ingredients_list:
        buy_list.append(f'{item["ingredient__name"]} - {item["amount"]} '
                        f'{item["ingredient__measurement_unit"]} \n')

    response = HttpResponse(buy_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="buylist.txt"')
    return response
