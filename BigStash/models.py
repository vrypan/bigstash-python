import six


class ModelBase(object):
    def __init__(self, *args, **kwargs):
        self._slots = []
        for (key, value) in six.iteritems(kwargs):
            self._slots.append(key)
            setattr(self, key, value)

    def __repr__(self):
        s = ["{ " + super(ModelBase, self).__repr__()]
        for slot in self._slots:
            r = "\n\t".join(repr(getattr(self, slot)).split("\n"))
            s.append("\t{} = {}".format(slot, r))
        return "\n".join(s) + "}"


class APIRoot(ModelBase):
    pass


class URLObject(ModelBase):
    _href_attr = 'href'

    def __unicode__(self):
        return "{}: {}".format(
            self.__class__.__name__, getattr(self, self._href_attr, 'n/a'))


class ObjectList(object):
    def __init__(self, klass, objects=[], next=None):
        self.klass = klass
        self.objects = objects
        self.next = next

    def __iter__(self):
        return (self.klass(**data) for data in self.objects)

    def __repr__(self):
        s = []
        for obj in self:
            s.append("\t" + "\n\t".join(repr(obj).split("\n")))
        if self.next is not None:
            s.append("\t...")
        return ("{ " + super(ObjectList, self).__repr__() +
                " [\n" + ",\n".join(s) + "]}")


class Archive(URLObject):
    pass


class Upload(URLObject):
    def __init__(self, *args, **kwargs):
        super(Upload, self).__init__(*args, **kwargs)
        if hasattr(self, 's3') and self.s3 is not None:
            self.s3 = BucketToken(**self.s3)
        if hasattr(self, 'archive') and self.archive is not None:
            self.archive = Archive(**self.archive)


class BucketToken(URLObject):
    pass


class User(URLObject):

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if hasattr(self, 'archives') and self.archives is not None:
            self.archives = ObjectList(
                Archive, self.archives['results'], self.archives['next'])


class Notification(ModelBase):
    pass
