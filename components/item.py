class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, targeting_area=None, level=1, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.level = level
        self.targeting_area = targeting_area
        self.function_kwargs = kwargs
