from lxml import etree
doc = etree.parse("2.xml")

memoryElem = doc.find('memory')
print(memoryElem.text)       # element text
print(memoryElem.get('unit')) # attribute
