from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import query
import os, os.path

ix = open_dir("indexdir")

searcher = ix.searcher()
#print(list(searcher.lexicon("content")))
parser = QueryParser("content", schema=ix.schema)
my_query = parser.parse(u"likes:[10 TO] AND 'javascript'")

# First, we need a query that matches all the documents in the "parent"
# level we want of the hierarchy
all_parents = query.Term("kind", "video")

# Then, we need a query that matches the children we want to find
wanted_kids = parser.parse(u'i have to learn html')

# Now we can make a query that will match documents where "name" is
# "close", but the query will return the "parent" documents of the matching
# children
q = query.NestedParent(all_parents, wanted_kids)

# results = Index, Calculator


results = searcher.search(q)

if len(results) == 0:
    print("Empty result!!")
else:
    for x in results:
        print(x)


