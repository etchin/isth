''' Converts the ISTH dataset in Zye format to Mirador 1.1 project format 
'''

import sys, csv, codecs
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

def fix_var_name(name):
    return name.replace('(', '_').replace(')', '').replace('-', '_')

def write_xml_line(line):
    ascii_line = ''.join(char for char in line if ord(char) < 128)
    if len(ascii_line) < len(line):
        print "  Warning: non-ASCII character found in line: '" + line.encode('ascii', 'ignore') + "'"
    xml_file.write(ascii_line + '\n')
    xml_strings.append(ascii_line + '\n')

def get_variables(xml, var_names, var_aliases, var_types, var_ranges):
    vname = ""
    valias = ""    
    vtype = ""
    vrange = ""
    
    for child in xml:
        if child.tag == "short":
            vname = child.text
        if child.tag == "full":
            valias = child.text
        if child.tag == "type":        
            vtype = child.text
            if vtype == "integer": vtype = "int"
        if child.tag == "range":
            vrange = child.text

    if vname != "":
        var_names.append(vname)
        var_aliases[vname] = valias
        var_types[vname] = vtype
        var_ranges[vname] = vrange
        return fix_var_name(vname)
        
metadata = ["zye/demographics.xml", "zye/clinical.xml", "zye/laboratory.xml", "zye/treatment.xml"]
        
data = []
with open("zye/LASSA-data.tsv") as tsv:
    for row in csv.reader(tsv.read().splitlines(), dialect="excel-tab"):        
        data.append(row)
titles = data[0]
titles1 = [''] * len(titles) 
for i in range(0, len(titles)):
  titles1[i] = fix_var_name(titles[i])
        
var_names = []
var_aliases = {}
var_types = {}  
var_ranges = {}

# Writing file in utf-8 because the input html files from
# NHANES website sometimes have characters output the ASCII range.
xml_file = codecs.open("mirador/groups.xml", "w", "utf-8")
xml_strings = []

write_xml_line('<?xml version="1.0"?>')

print "Creating groups file..."
write_xml_line('<data>')
for meta in metadata:
    tree = ET.parse(meta)
    root = tree.getroot()
    write_xml_line(' <group name="' + root.attrib["name"] + '">')
    for el in root:
        if (el.tag == "table"):
          if el.attrib["include"] != "yes": continue          
          write_xml_line('  <table name="' + el.attrib["name"] + '">')          
          for child in el: 
              if child.tag == "var":
                  if child.attrib["include"] == "yes":
                      name = get_variables(child, var_names, var_aliases, var_types, var_ranges)
                      write_xml_line('   <variable name="' + name + '"/>')
          write_xml_line('  </table>')          
    write_xml_line(' </group>')
write_xml_line('</data>')    
xml_file.close()

# For XML validation.
try:
    doc = parseString(''.join(xml_strings))
    doc.toxml()
    print "Done."    
except:
    sys.stderr.write("XML validation error:\n")
    raise

print "Creating data file..."
with open("mirador/data.tsv", "w") as tsv:
    writer = csv.writer(tsv, dialect="excel-tab")
    writer.writerow(titles1)
    for i in range(1, len(data)):
        writer.writerow(data[i])
print "Done."

print "Creating dictionary file..."
dfile = open("mirador/dictionary.tsv", 'w')
for name in titles:
    line = var_aliases[name] + '\t' + var_types[name] + '\t' + var_ranges[name] + '\n'
    dfile.write(line)  
dfile.close()
print "Done."
