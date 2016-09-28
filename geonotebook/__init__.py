import os
import sys
from jinja2 import ChoiceLoader, FileSystemLoader, PrefixLoader

def _jupyter_server_extension_paths():
    return [{
        "module": "geonotebook"
    }]

def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="static",
        # directory in the `nbextension/` namespace
        dest="geonotebook",
        # _also_ in the `nbextension/` namespace
        require="geonotebook/index")]



def load_jupyter_server_extension(nbapp):
    nbapp.log.info("geonotebook module enabled!")

    """
    This is out right confusing, but is necessary to meet the following criteria:
    - Templates in geonotebook/templates will override those in core notebook templates
    - Core notebook templates can still be referred to/extended by referring to them as core@template.html

    The ChoiceLoader tries each of the loaders in turn until one of them provides the right template.
    The PrefixLoader allows us to refer to core templates using the core@ prefix, this is necessary
    because we want to extend templates of the same name while referring to templates in a different loader (core).
    The PackageLoader lets us put our templates ahead in priority of the notebooks templates.
    The core_loader is last which falls back to the original loader the notebook uses.

    This implementation is weird, but should be compatible/composable with other notebook extensions
    and fairly future proof.
    """
    nbapp.web_app.settings['jinja2_env'].loader = ChoiceLoader([
        PrefixLoader({'core': nbapp.web_app.settings['jinja2_env'].loader}, delimiter='@'),
        FileSystemLoader(os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'templates')),
        nbapp.web_app.settings['jinja2_env'].loader])

### Note:  How to add custom web handlers
#     webapp = nbapp.web_app
#     base_url = webapp.settings['base_url']
#
#     webapp.add_handlers(".*$", [
#         (ujoin(base_url, r"/nbextensions"), NBExtensionHandler),
#         (ujoin(base_url, r"/nbextensions/"), NBExtensionHandler),
#         (ujoin(base_url, r"/nbextensions/config/rendermd/(.*)"),
#          RenderExtensionHandler),
#     ])

###   Note: Ugly hack to add geonotebook template to jinja2 search path
#     nbapp.web_app.settings['jinja2_env'].loader.searchpath = [u"/home/kotfic/src/jupyter/geonotebook/geonotebook/templates"] + nbapp.web_app.settings['jinja2_env'].loader.searchpath
