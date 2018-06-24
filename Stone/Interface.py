class ITwoSideStone(object):
    def flip(self):
        raise Exception("Not implemented")

    def get_side(self):
        raise Exception("Not implemented")

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        super(ITwoSideStone, self).__setattr__(key, value)
