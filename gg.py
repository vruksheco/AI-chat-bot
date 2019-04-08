import xml.etree.ElementTree as ET
tree = ET.parse('eateries.xml')
root = tree.getroot()
for x in root.iter('cat') :
    gg = x.text.lower()
    x.text = gg
    print(x.text)
    x.set("updated","yes")
for x in root.iter('store') :
    gg = x.text.lower()
    x.text = gg
    print(x.text)
    x.set("updated","yes")
for x in root.iter('location') :
    gg = x.text.lower()
    x.text = gg
    print(x.text)
    x.set("updated","yes")

tree.write("eateries.xml")
