# Required imports. You need to install whoosh to run this!

import nbformat
import json

from pathlib import Path
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

from whoosh.filedb.filestore import FileStorage
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)

# The main class.

@magics_class
class SearchMagic(Magics):
    """
    Outer class to define the Search Magic!
    """
    @staticmethod
    def index_notebooks():
        """
        Indexing IPython Notebook
        """
        # Defining the Schema
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True), cell_number=ID(stored=True))

        # Whoosh needs a new directory to create and store the index files. In case it is not present, we create it.
        if not Path("indexdir").exists():
            Path("indexdir").mkdir()

        ix = create_in("indexdir", schema)

        ipynb_notebooks = []
        
        # Supports just IPython books for now. If you are reading this, you probably want to extend this to support more files!
        for doc in Path(".").iterdir():
            if doc.suffix == ".ipynb":
                ipynb_notebooks.append(doc)
        
        # Process the books one by one, cell by cell and treat them as different documents. Add them to the index accordingly
        for note_num, notebook_path in enumerate(ipynb_notebooks):
            notebook = str(notebook_path)

            with open(notebook) as f:
                response = f.read()

            response_json = json.loads(response)["cells"]

            for counter, data in enumerate(response_json):
                writer = ix.writer()
                writer.add_document(title=notebook, path="{}.{}".format(note_num, notebook), 
                                    content=json.dumps(data), cell_number=str(counter))
                writer.commit()
    
    @staticmethod
    def search_in_notebooks(query):
        # Load the index. Keeping the indexer and the searcher separate removes state between the two.
        storage = FileStorage("indexdir")
        ix = storage.open_index()

        with ix.searcher() as searcher:
            display_answer = []
            
            query = QueryParser('content', ix.schema).parse(query)
            results = searcher.search(query, terms=True)

            for item in results:
                content = json.loads(item["content"])
                
                # Because we need to prettify everything before we print
                element = {"Notebook": item["title"], 
                           "Cell Number": int(item["cell_number"]) + 1, "Notebook Execution Number": content["execution_count"]}
                
                display_answer.append(element)

        ix.close()

        return display_answer
    
    @line_magic
    def create_index(self, line):
        """
        Line magic definition for creating the index file
        """
        self.index_notebooks()
    
    @line_magic
    def search(self, line):
        """
        Line magic definition to search
        """
        results = self.search_in_notebooks(line)
        for hits in results:
            for key, value in hits.items():
                print("{} -> {}".format(key, value))
                
            print("-------")