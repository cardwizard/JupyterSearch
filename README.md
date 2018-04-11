# JupyterSearch
Utility to help search within a set of jupyter notebooks
I worked on creating a simple magic function to help us make this search easy and search across notebooks present in the current directory. It uses whoosh in the back-end to speed up the search. The code iterates through every cell in every notebook in your current directory. 
 
 
How to use it?
 
1. Download the search_magic.py file and keep it in your current directory. Follow these steps 
2. pip install whoosh
3. Run the magic commands as follows in your Jupyter notebook. In the example shown below, I am trying to search for keyword tesseract.

```python

In [1]: from search_magic import SearchMagic
In [2]: get_ipython().register_magics(SearchMagic)

In [3]: %create_index

In [4]: %search tesseract
Out[4]: Cell Number -> 2
        Notebook -> similarity.ipynb
        Notebook Execution Number -> 2
```
