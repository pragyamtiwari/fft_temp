class Headline:
    def __init__(self, title, source, snippet, date):
        self.title = title
        self.source = source
        self.snippet = snippet
        self.date = date
        self.research = []

    def __str__(self):
        return f"Title: {self.title}\nSource: {self.source}\nDate: {self.date}\nSnippet: {self.snippet}"

class Interest:
    def __init__(self, name, previously_selected_headline_titles=set()):
        self.name = name
        self.headlines = []
        self.selected_headline_index = None
        self.previously_selected_headline_titles = previously_selected_headline_titles
    
    @property
    def selected_headline(self):
        if self.selected_headline_index is not None:
            return self.headlines[self.selected_headline_index]
        return None

    def __str__(self):
        res = []

        for index, headline in enumerate(self.headlines):
            res.append(f"{index + 1}. {headline}")

        return '\n'.join(res)

class User:
    def __init__(self, name, zip_code, interest_names):
        self.name = name
        self.zip_code = zip_code
        self.interests = [Interest(name) for name in interest_names]
        self.interest_index = 0

    @property
    def interest(self):
        return list(self.interests)[self.interest_index]
