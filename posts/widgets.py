from django import forms
from django.utils.safestring import mark_safe


class MarkdownRichTextWidget(forms.Textarea):
    """
    A custom widget that uses EasyMDE for markdown-based rich text editing.
    Stores content as markdown text, which is Facebook-compatible.
    """

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'markdown-editor-input',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Get the textarea HTML from parent
        textarea_html = super().render(name, value, attrs, renderer)

        # Get the input ID
        input_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'

        html = f'''
        <div class="markdown-editor-wrapper">
            {textarea_html}
            <small class="form-text text-muted d-block mt-2">
                <strong>Markdown formatting:</strong> Use *text* or **text** for <strong>bold</strong>,
                _text_ or __text__ for <em>italic</em>, ~text~ for <del>strikethrough</del>.
                This content is fully compatible with Facebook posts!
            </small>
        </div>
        '''
        return mark_safe(html)

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.js',
            'js/markdown-editor.js',
        )


# Keep the old Lexical widget for reference/archival
class LexicalRichTextWidget(forms.Textarea):
    """
    ARCHIVED: A custom widget that uses Lexical for rich text editing.
    Kept for reference. Use MarkdownRichTextWidget instead.
    """
    pass

