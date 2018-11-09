from ruamel import yaml
from collections import OrderedDict
from ofcourse import serializers


def person_list_yaml_dumper(f, person_list, use_omap=False):
    y = yaml.YAML()
    if not use_omap:
        y.representer.add_representer(
            OrderedDict, yaml.representer.RoundTripRepresenter.represent_dict
        )
    p_list = serializers.person_list_serializer(person_list)
    for name, person in p_list.items():
        y.dump({name: person}, f)
        print("", file=f)
