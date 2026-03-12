// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://thainights.net',
	integrations: [mdx(), sitemap()],
	i18n: {
		defaultLocale: 'zh-tw',
		locales: ['zh-tw', 'zh-cn', 'en'],
		routing: {
			prefixDefaultLocale: false,
		},
	},
});
