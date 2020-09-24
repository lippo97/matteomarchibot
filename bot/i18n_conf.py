import os
import i18n as _i18n

locales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../locales")

_i18n.load_path.append(locales_dir)
_i18n.set('locale', 'it')
_i18n.set('fallback', 'en')
_i18n.set('enable_memoization', True)

t = _i18n.t
