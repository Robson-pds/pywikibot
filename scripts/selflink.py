#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot searches for selflinks and allows removing them.

These command line parameters can be used to specify which pages to work on:

&params;

-always           Unlink always but don't prompt you for each replacement.
                  ATTENTION: Use this with care!
"""
#
# (C) Pywikibot team, 2006-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, division, unicode_literals

import pywikibot

from pywikibot.bot import Choice, MultipleSitesBot
from pywikibot.pagegenerators import GeneratorFactory, parameterHelp
from pywikibot.specialbots import BaseUnlinkBot

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': parameterHelp,
}


class _BoldChoice(Choice):

    """A choice to make the title bold."""

    def __init__(self, page, replacer):
        super(_BoldChoice, self).__init__('make bold', 'b', replacer)
        self._page = page

    def handle(self):
        return "'''{0}'''".format(self._page.title(with_section=False))


class SelflinkBot(MultipleSitesBot, BaseUnlinkBot):

    """Self-link removal bot."""

    summary_key = 'selflink-remove'

    def __init__(self, generator, **kwargs):
        """Initializer."""
        super(SelflinkBot, self).__init__(**kwargs)
        self.generator = generator

    def _create_callback(self):
        """Create callback and add a choice to make the link bold."""
        callback = super(SelflinkBot, self)._create_callback()
        callback.additional_choices += [_BoldChoice(self.current_page,
                                                    callback)]
        return callback

    def treat_page(self):
        """Unlink all links pointing to the current page."""
        # Inside image maps, don't touch selflinks, as they're used
        # to create tooltip labels. See for example:
        # https://de.wikipedia.org/w/index.php?diff=next&oldid=35721641
        if '<imagemap>' in self.current_page.text:
            pywikibot.output(
                u'Skipping page %s because it contains an image map.'
                % self.current_page.title(as_link=True))
            return
        self.unlink(self.current_page)


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: unicode
    """
    # Process global args and prepare generator args parser
    local_args = pywikibot.handle_args(args)
    gen_factory = GeneratorFactory()
    bot_args = {}

    for arg in local_args:
        if arg == '-always':
            bot_args['always'] = True
        else:
            gen_factory.handleArg(arg)

    gen = gen_factory.getCombinedGenerator(preload=True)
    if not gen:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False

    bot = SelflinkBot(gen, **bot_args)
    bot.run()
    return True


if __name__ == "__main__":
    main()
