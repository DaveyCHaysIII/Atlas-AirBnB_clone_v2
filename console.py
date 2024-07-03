#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
import shlex
import models
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update', 'create']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float,
             'name': str, 'state_id': str, 'city_id': str,
             'user_id': str, 'email': str, 'password': str,
             'first_name': str, 'last_name': str,
             'description': str, 'text': str, 'place_id': str
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """Create an object of any class."""
        if not args:
            print("** class name missing **")
            return

        # validade class name
        c_name = args.split()[0]
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Extracting parameters after the class name
        params = args.split()[0:]
        if not params:
            print(f"** {c_name} name missing **")
            return
        # Initialize the new instance with the class
        new_instance = HBNBCommand.classes[c_name]()

        # Process each parameter
        for param in params:
            try:
                # Check if the parameter follows the key=value format
                key, value = param.split('=')
                # Remove leading/trailing whitespaces and escape quotes
                key = key.strip()
                value = value.replace('_', ' ').strip('"').replace('\\"', '"')
                # Convert value to the appropriate type
                if re.match(r'^-?\d+\.\d+$', value):
                    value = float(value)
                elif value.isdigit():
                    value = int(value)
                else:
                    value = value

                # Set the attribute on the new instance
                setattr(new_instance, key, value)
            except ValueError:
                # Skip parameters that don't match the expected format
                continue

        # Save the new instance to storage
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        cls = HBNBCommand.classes.get(c_name)
        objs = storage.all(cls)
        key = f"{c_name}.{c_id}"

        try:
            storage.delete(objs[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            else:
                cls = HBNBCommand.classes[args]
                obj_dict = models.storage.all(cls)
        else:
            obj_dict = models.storage.all()

        for key, obj in obj_dict.items():
            print(f"{key}: {obj.to_dict()}")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        # Assuming 'args' is the class name as a string, e.g., 'Place'
        count = 0
        all_objects = storage.all()
        for obj in all_objects.values():
            if type(obj).__name__ == args:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Update an object based on class name, id, attribute & value."""
        args = shlex.split(args)

        if len(args) < 4:
            print("Usage: update <class> <id> <attribute> <value>")
            return

        c_name, obj_id, att_name, att_value = args[:4]

        # validate class name
        if c_name not in HBNBCommand.classes:
            print(f"** class does not exist {c_name}**")
            return
        else:
            cls = HBNBCommand.classes[c_name]

        # validate object
        obj_key = f"{c_name}.{obj_id}"
        if obj_key not in storage.all(cls).keys():
            print(f"** no instance found {obj_key} **")
            return
        else:
            obj = storage.all(cls)[obj_key]

        # validate attribute name and type
        if att_name not in HBNBCommand.types:
            print(f"** attribute does not exist: {att_name} **")
            return
        else:
            att_type = HBNBCommand.types[att_name]
            try:
                new_value = att_type(att_value)
            except ValueError:
                print(f"** {att_name} must be of type: "
                      f"{HBNBCommand.types[att_name].__name__} **")
                return

        # update the attribute and save
        setattr(obj, att_name, new_value)
        storage.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
