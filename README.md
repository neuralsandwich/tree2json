tree2json
=========

Converts out put from tree into a Json object

Usage
-----

    tree -S -n --charset ascii | python tree2json.py

Example
-------

    {
      "data": ".",
      "children": [
        {
          "data": "LICENSE",
          "children": []
        },
        {
          "data": "README.md",
          "children": []
        },
        {
          "data": "tree2json.py",
          "children": []
        }
      ]
    }
