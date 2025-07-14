from dataclasses import asdict


class Vacancy:
    def __init__(self, id,site,title,company,location,url,description):
        self.id = id
        self.site = site
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.description = description
    
    def to_dict(self):
        """Преобразует объект Vacancy в словарь"""
        return {
            'id': self.id,
            'site':self.site,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'url': self.url,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Vacancy из словаря"""
        return cls(
            id=data.get('id'),
            site=data.get('site'),
            title=data.get('title'),
            company=data.get('company'),
            location=data.get('location'),
            url=data.get('url'),
            description=data.get('description')
        )
    