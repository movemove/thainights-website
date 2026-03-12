import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL) {
  const pathname = url.pathname;
  const parts = pathname.split('/').filter(Boolean); // Remove empty strings
  
  // Check the first segment of the path
  if (parts.length > 0 && parts[0] in ui) {
    return parts[0] as keyof typeof ui;
  }
  
  return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
  return function t(key: keyof typeof ui[typeof defaultLang]) {
    return ui[lang][key] || ui[defaultLang][key];
  }
}
