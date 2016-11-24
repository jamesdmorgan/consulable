# consulable
Ansible dynamic inventory for consul kv

## Installation

Add the consul-kv.py and consul.ini to the Ansible *inventory* directory.

If you are using ec2.py it should live alongside.

> Ensure that the python script is executable


## Configuration

All configuration is defined in the consul.ini config file.

By default it will talk to the local *consul* agent and look for keys prefix with **/ansible**

```
[consul]
host=127.0.0.1
port=8500
key_prefix=ansible
```

## Consul Keys

All keys prefixed by **key_prefix** (/ansible) will get added to the Ansible inventory

The first layer of the hierarchy (after the index) is the group you want the key to apply to.

```
/ansible/all/some_key
```

Adds the *some_key* variable to the group *all*

All levels under group are considered part of the variable name.

You can set *dicts* and *lists* as well as normal *strings*. These should be defined in YAML as you would in Ansible.

> An additional variable **consul_kv** is added to the *all* group that details all keys, values and paths in consul

**/ansible/all/list_example**
```
- a
- b
- c
```

**/ansible/all/dict_example**
```
foo: bah
test: dict
```

```
PLAY [local] *******************************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "string_example": "I'm a string!!"
}

TASK [debug] *******************************************************************
ok: [localhost] => {
    "list_example": [
        "a",
        "b",
        "c"
    ]
}

TASK [debug] *******************************************************************
ok: [localhost] => {
    "dict_example": {
        "foo": "bah",
        "test": "dict"
    }
}

TASK [debug] *******************************************************************
ok: [localhost] => {
    "consul_kv": [
        {
            "key": "dict_example",
            "path": "ansible/all/dict_example",
            "value": {
                "foo": "bah",
                "test": "dict"
            }
        },
        {
            "key": "list_example",
            "path": "ansible/all/list_example",
            "value": [
                "a",
                "b",
                "c"
            ]
        },
        {
            "key": "string_example",
            "path": "ansible/all/string_example",
            "value": "I'm a string!!"
        }
    ]
}


```
