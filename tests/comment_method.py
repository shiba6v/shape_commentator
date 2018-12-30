import shape_commentator
import sys
In = ["",""]
src = open(sys.argv[1]).read()
shape_commentator.comment(src, globals())
