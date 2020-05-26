import xml.etree.ElementTree as ElementTree
import sys

def print_elem(element):
    return "<%s>" % element.tag

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: %s filename" % sys.argv[0]
    sys.exit(1)
filename = sys.argv[1]    
tree = ElementTree.parse(filename)
root = tree.getroot()
chunks = {}
iter = root.findall('.//*')
for element in iter:
    if element.text in chunks:
        chunks[element.text].append(element)
    else:
        chunks[element.text] = [element,]
for text in chunks:
    if len(chunks[text]) > 1:
        print "\"%s\" is a duplicate: found in %s" % \
              (text, map(print_elem, chunks[text]))
