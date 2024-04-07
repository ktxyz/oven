from urllib.parse import urlparse
import xml.etree.ElementTree as etree

from markdown import Markdown, Extension
from markdown.treeprocessors import Treeprocessor


class OvenURLsProcessor(Treeprocessor):
    def run(self, root: etree):
        self.__update_hrefs(root)

    def __update_hrefs(self, node: etree.Element):
        if node.attrib.get('href'):
            url = urlparse(node.attrib['href'])
            if not url.netloc:
                node.attrib['href'] = '{{ ' + f'\'{node.attrib["href"]}\' | geturl(lang)' + ' }}'
        for child in node:
            self.__update_hrefs(child)


class OvenURLsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(OvenURLsProcessor(md), EXTENSION_NAME, 1)


def makeExtension(**kwargs):
    return OvenURLsExtension(**kwargs)


EXTENSION_NAME = "oven_urls"
EXTENSION_CLASS = OvenURLsExtension
