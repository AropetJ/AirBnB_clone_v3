#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_objs = {}
            for clsid, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    new_objs[clsid] = obj
            return new_objs
        else:
            return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        fname = FileStorage.__file_path
        storage_d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            storage_d[bm_id] = bm_obj.to_json(saving_file_storage=True)
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(storage_d, f_io)

    def reload(self):
        """deserializes the JSON file to __objects"""
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except Exception as e:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """delete obj from __objects if its inside"""
        if obj:
            obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(obj_ref):
                del FileStorage.__objects[obj_ref]
            self.save()

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """A method to retrieve an object based on class name and id"""
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """A method to count the number of objects in storage"""
        return (len(self.all(cls)))
