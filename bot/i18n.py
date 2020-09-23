import i18n

i18n.load_path.append('locales')
i18n.set('locale', 'it')
i18n.set('fallback', 'en')
i18n.set('enable_memoization', True)

t = i18n.t
