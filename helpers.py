def save_html(html: bytes, path: str):
        '''
        Docstring for save_html
        
        :param html: bytes from requests.get().content
        :param path: where to save the html file
        :return: None
        '''
        with open(path, "wb") as f:
            f.write(html)