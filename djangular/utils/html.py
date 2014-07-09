from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import force_text
from django.utils.functional import allow_lazy
from django.utils import six
from django.utils.text import normalize_newlines

def escape(text):
    """
    Returns the given text with ampersands, quotes and angle brackets encoded for use in HTML.
    """
    return mark_safe(force_text(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))
escape = allow_lazy(escape, six.text_type)

def conditional_escape(text):
    """
    Similar to escape(), except that it doesn't operate on pre-escaped strings.
    """
    if isinstance(text, SafeData):
        return text
    else:
        return escape(text)

def format_html(format_string, *args, **kwargs):
    """
    Similar to str.format, but passes all arguments through conditional_escape,
    and calls 'mark_safe' on the result. This function should be used instead
    of str.format or % interpolation to build up small HTML fragments.
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = dict([(k, conditional_escape(v)) for (k, v) in
                        six.iteritems(kwargs)])
    return mark_safe(format_string.format(*args_safe, **kwargs_safe))
