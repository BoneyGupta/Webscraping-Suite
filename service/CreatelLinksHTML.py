from service.Logger import Logs


def create_links_html(ref_dict: dict, string, filepath, logs: Logs):
    logs.log.info(f"CreateLinksHTML/create_links_html) {string}")

    links_list = list(filter(lambda item: string in item[0], ref_dict.items()))

    i = 1
    links_string = ""
    for value in links_list:
        links_string += f"<a id='{i}' href=\"{value[1]}\"> [Link #{i}: {value[1]}]</a>"
        i += 1
    print(links_string)

    html_code = (f"<!DOCTYPE html><html><head><title>Links HTML</title></head><body><p>Test Links:</p>"
                 f"{links_string}</body></html>")
    with open(f"Html Pages/{filepath}", "w") as html_file:
        html_file.write(html_code)

    send = {'html_code': html_code}
    return send

# ref = {'url1': "https://www.google.com", '2url': 'https://www.amazon.in'}
# print(create_links_html(ref, 'url', 'url22.html'))
