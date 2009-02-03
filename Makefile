# SpamFighter, Copyright 2008, 2009 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# This file is part of SpamFighter.
#
# SpamFighter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpamFighter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpamFighter.  If not, see <http://www.gnu.org/licenses/>.
#

PYDOCTOR?=pydoctor
TRIAL?=trial
TRACKER?=http://spam-fighter.ru/

all: unittest 

docs: manual apidocs

clean: clean-admin clean-manual clean-apidocs

dist: clean manual apidocs admin package

unittest:
	$(TRIAL) spamfighter

admin:
	cd admin/ && ./generate.py build

debug-admin:
	cd admin/ && ./generate.py source

clean-admin:
	cd admin/ && ./generate.py clean

apidocs:
	mkdir -p docs/api/
	$(PYDOCTOR) --add-package=spamfighter/ --make-html  --project-name="SpamFighter" --html-viewsource-base=$(TRACKER)browser/ --html-output=docs/api/

clean-apidocs:
	rm -rf docs/api/

manual:
	$(MAKE) -C docs/manual/ html

clean-manual:
	$(MAKE) -C docs/manual/ clean

package:
	rm -rf dist/
	./setup.py clean
	./setup.py sdist
	./setup.py bdist_dumb
