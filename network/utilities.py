def get_previous_page(page):
    if page.has_previous():
        previous_page_url = f'?page={page.previous_page_number()}'
    else:
        previous_page_url = ''
    return previous_page_url

def get_next_page(page):
    if page.has_next():
        next_page_url = f'?page={page.next_page_number()}'
    else:
        next_page_url = ''
    return next_page_url