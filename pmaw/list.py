class BaseList(PMAWBase):
    """An abstract class to coerce a list into a PMAWBase."""

    CHILD_ATTRIBUTE = None

    def __init__(self, messari, _data):
        super().__init__(messari, _data=_data)

        if self.CHILD_ATTRIBUTE is None:
            raise NotImplementedError("BaseList must be extended.")

        child_list = getattr(self, self.CHILD_ATTRIBUTE)
        for index, item in enumerate(child_list):
            child_list[index] = messari.parser.parse(item)

    def __contains__(self, item):
        """Test if item exists in the list."""
        return item in getattr(self, self.CHILD_ATTRIBUTE)

    def __getitem__(self, index):
        """Return the item at position index in the list."""
        return getattr(self, self.CHILD_ATTRIBUTE)[index]

    def __iter__(self):
        """Return an iterator to the list."""
        return getattr(self, self.CHILD_ATTRIBUTE).__iter__()

    def __len__(self):
        """Return the number of items in the list."""
        return len(getattr(self, self.CHILD_ATTRIBUTE))

    def __str__(self):
        """Return a string representation of the list."""
        return str(getattr(self, self.CHILD_ATTRIBUTE))


class OfficialLinksList(BaseList):
    """A list of official links for an asset."""

    CHILD_ATTRIBUTE = "official_links"
