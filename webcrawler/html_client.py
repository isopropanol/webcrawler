async def get_page_async(session, url):
    headers = {"content-type": "text/html"}
    try:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            return html
    except Exception:
        # if we run into trouble trying to query a link, lets just move on
        return ""
