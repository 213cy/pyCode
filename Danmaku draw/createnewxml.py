import xml.etree.ElementTree as ET
import time


def parse_xml_text(text):
    tree = ET.fromstring(text)

    data = []
    # for d_elem in tree.findall('d'):
    for d_elem in tree.iter('d'):
        p_values = d_elem.get('p').split(',')
        # p_attr = f"{stime},{mode},{size},{color},
        #           {date},{pool},{author},{dbid}"
        stime = p_values[0]
        date = p_values[4]
        author_mid = p_values[6]
        text_content = d_elem.text

        data.append([stime, date, author_mid, text_content])

    return data




def save_data_to_xml(data, fileinfo, filename):
    # tree = ET.ElementTree()
    root = ET.Element('i')
    for key,value in fileinfo.items():
        ET.SubElement(root, key).text = value

    for stime, date, author_mid, text_content in data:
        d = ET.SubElement(root, 'd')
        p_attr = f"{stime},{date},{author_mid}"
        d.set('p', p_attr)
        d.text = text_content

    # 将ElementTree对象转换为字符串（XML格式）
    # tree_new_str = ET.tostring(root, encoding='unicode')

    tree_new = ET.ElementTree(root)
    tree_new.write(filename, encoding='utf-8',  xml_declaration=True)
    # with open('output2.xml', 'wb', encoding='utf-8') as xml_file:
    #     tree_new.write(xml_file, encoding='utf-8', xml_declaration=True)
    # with open('output2.xml', 'w') as xml_file:
    #     tree_new.write(xml_file, xml_declaration=True)
    # with open(filename, "wb") as f:
    #     tree_new.write(f, encoding='utf-8', xml_declaration=True)

def open_xml_file(filename='output.xml'):
    with open(filename, 'wb') as f:
        content = f.read()
        f.write(content)

def create_new_xml(text, fileinfo={}, filename='output.xml'):
    data = parse_xml_text(text)

    sorted_data = sorted(data, key=lambda x: float(x[0]))
    print("total entries :",len(sorted_data))
    s = set()
    sanitized_data = []
    for x in sorted_data:
        if x[2] not in s:
            s.add(x[2])
            sanitized_data.append(x)
    print("logged entries :",len(sanitized_data))
    # sanitized_data

    fileinfo.update({"createtime": str(int(time.time())),
    "entrycount": str(len(sanitized_data))})
    save_data_to_xml(sanitized_data, fileinfo, filename)
