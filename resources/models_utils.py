
class GalleryItem(object):

    def __init__(self, index, src):
        self.index = index
        self.src = src


class GalleryGroup(object):

    def __init__(self, index, max_size=3):
        self.index = index
        self.items = []
        self.max_size = max_size

    @property
    def is_full(self):
        return len(self.items) >= self.max_size

    def add(self, item):
        self.items.append(item)


class GalleryFactory(object):

    @staticmethod
    def create(urls):
        groups = list()
        groups.append(GalleryGroup(len(groups)))
        for index, url in enumerate(urls):
            item = GalleryItem(index, url)
            if groups[-1].is_full:
                groups.append(GalleryGroup(len(groups)))
            groups[-1].add(item)
        return groups

