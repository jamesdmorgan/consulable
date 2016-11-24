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

**/ansible/all/list_example**
```
  - a
  - b
  - c
```

```
TASK [debug] *******************************************************************
ok: [localhost] => {
    "list_example": [
        "a",
        "b",
        "c"
    ]
}

```
