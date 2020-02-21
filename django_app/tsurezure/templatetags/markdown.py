from django import template
from django.utils.safestring import mark_safe
import markdown
from markdownx.settings import MARKDOWNX_MARKDOWN_EXTENSIONS, MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
from markdown.extensions import Extension

register = template.Library()

class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')

@register.filter
def markdown_to_html(text):
    """
    マークダウンで記述された引数.テキストをhtmlに変換する。
    HTMLやCSS、JavaScript等のコードはエスケープされる。

    :param text: テキスト
    :return: html
    """
    extensions = MARKDOWNX_MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions, extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
    return mark_safe(html)