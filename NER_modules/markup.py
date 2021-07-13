# coding: utf-8
from __future__ import unicode_literals, print_function


def assert_ipymarkup():
    try:
        import ipymarkup
    except ImportError:
        raise ImportError('pip install ipymarkup')


def get_markup_notebook(text, spans):
    assert_ipymarkup()
    from ipymarkup import BoxMarkup, Span
    from IPython.display import display

    spans = [Span(start, stop) for start, stop in spans]
    return BoxMarkup(text, spans)


def show_markup_notebook(text, spans):
    markup = get_markup_notebook(text, spans)
    display(markup)


def show_markup(text, spans):
    assert_ipymarkup()
    from ipymarkup import show_span_box_markup
    show_markup(text, spans)
    

def format_json(data):
    import json

    return json.dumps(data, indent=2, ensure_ascii=False)


def show_json(data):
    print(format_json(data))

def markup_text(text, spans):
    from ipymarkup import format_span_box_markup
    html = list(format_span_box_markup(text, spans))
    html_str = ' '.join(html)
    style = "<style>mark.entity { display: inline-block }</style>"
    return style + html_str