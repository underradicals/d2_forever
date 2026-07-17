import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "destiny2_docs",
  description: "Destiny2 Docs",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Docs", link: "/docs/index" },
    ],

    sidebar: [
      {
        text: "Examples",
        items: [
          { text: "Project Setup", link: "/docs/index" },
          { text: "Runtime API Examples", link: "/api-examples" },
        ],
      },
    ],

    socialLinks: [{ icon: "github", link: "https://github.com/underradicals" }],
  },
});
