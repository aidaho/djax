# -*- coding: utf-8 -*-
"""
Django AJAX - Server-side companion for client-side ajax javascript.
              Provides custom view class designed to be drop-in replacement
              for TemplateView in Django 1.5 and higher.

Copyright (C) 2013 Sergey Frolov

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License v3
or BSD 2-clause license.

Here follows 'no warranty' rattle, you know the drill.
"""
from django.views.generic.base import TemplateView
try:
    from settings import AJAX_TEMPLATE_POSTFIX
except ImportError:
     AJAX_TEMPLATE_POSTFIX = "-ajax"
try:
    from settings import AJAX_HTTP_HEADER
except ImportError:
     AJAX_HTTP_HEADER = "HTTP_X_PJAX" # default header for jquery-pjax


class AjaxTemplateView(TemplateView):
    """
    Ajax-related template heuristic.

    In case of presence AJAX_HTTP_HEADER in request returns either
    self.ajax_template_name or tuple of guessed ajax template and
    template_name. Django will render the first one available so it's
    okay to use this class instead of TemplateView even if no ajax template
    available for this view.
    """
    ajax_template_name = None

    def get_template_names(self):
        names = super(AjaxTemplateView, self).get_template_names()
        if self.request.META.get(AJAX_HTTP_HEADER, False):
            if not self.ajax_template_name:
                def guess_template(name):
                    """
                    Appends postfix either before the template file extension
                    or after template file name if one lacks extension.

                    Example:
                    >>> AJAX_TEMPLATE_POSTFIX = "-ajax"
                    >>> guess_template('filename.ext')
                    'filename-ajax.ext'
                    >>> guess_template('filename')
                    'filename-ajax'
                    """
                    if "." in name:
                        splitname = name.split('.')
                        splitname[-2] += AJAX_TEMPLATE_POSTFIX
                        ajax_name = '.'.join(splitname)
                    else:
                        ajax_name = name + AJAX_TEMPLATE_POSTFIX
                    return ajax_name

                def roundrobin(*args):
                    """
                    Simple roundrobin. Truncates result at a length of the
                    shortest supplied list/tuple.

                    Example:
                    >>> roundrobin([1,2,3], [4,5,6,7,8], [9])
                    [1, 4, 9]
                    """
                    result = []
                    i = min([len(arg) for arg in args])
                    assert i > 0, "Zero-length iterable passed"
                    while i:
                        for arg in args:
                            result.append(arg[i-1])
                        i -= 1
                    return result

                ajax_names = map(guess_template, names)
                names = roundrobin(ajax_names, names)
            else: # ajax_template_name is set
                names = [self.ajax_template_name]
        return names


if __name__ == "__main__":
    import doctest
    doctest.testmod()
